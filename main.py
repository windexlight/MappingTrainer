import asyncio
import bisect
import configparser
import os
import random
import time
import re
import sys
from pathlib import Path
import hid
import ctypes
import hashlib
import math

import qasync
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QTimer, Signal, QEvent, QObject, QByteArray, QCoreApplication
from PySide6.QtGui import (QColor, QKeyEvent, QIcon, QFontMetricsF, QFont, QTextOption,
                         QTextCursor, QTextCharFormat, QFontDatabase, QSyntaxHighlighter, QGuiApplication, QActionGroup)
from PySide6.QtWidgets import (QDialog, QFileDialog, QHeaderView, QInputDialog, QLabel, QApplication, QLineEdit, QPlainTextEdit,
                             QLabel, QMessageBox, QTableWidgetItem, QAbstractButton, QCheckBox)

from ui_mainWindow import Ui_MainWindow
from scancodes import *
from keycodes import *
from keynames import keynames
from char_translations import *
import combos
from words_no_swears import words
from ngrams import ngrams
from rawhid import RawHid
from highlighter import Highlighter, make_ngram_lexer
from detect_code_info import detect_code_info, CodeInfo, IndentType
from settings import Settings, ModeValue
from ngrams import ngrams


QT_MODS = [Qt.KeyboardModifier.ControlModifier, Qt.KeyboardModifier.ShiftModifier, Qt.KeyboardModifier.AltModifier, Qt.KeyboardModifier.MetaModifier]

class mainWindow(QtWidgets.QMainWindow):
    attemptAdvance = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.attemptAdvance.connect(self.attemptPromptAdvance)

        QCoreApplication.setOrganizationName("windexlight")
        QCoreApplication.setApplicationName("MappingTrainer")

        self.settings = Settings()

        self._goemetry_initialized = False

        self.modeActionGroup = QActionGroup(self)
        self.modeActionGroup.addAction(self.ui.actionKey_Practice)
        self.modeActionGroup.addAction(self.ui.actionTyping_Practice)
        self.modeActionGroup.addAction(self.ui.actionWords_Top_10)
        self.modeActionGroup.addAction(self.ui.actionWords_Top_100)
        self.modeActionGroup.addAction(self.ui.actionWords_Top_1000)
        self.modeActionGroup.addAction(self.ui.actionWords_All)
        self.modeActionGroup.addAction(self.ui.actionN_Grams)
        self.modeActionGroup.addAction(self.ui.actionWords_w_N_Grams)
        self.ui.lineEdit.setVisible(False)
        self.ui.pushButton_Back.setVisible(False)
        self.ui.label_line.setVisible(False)
        self.ui.textedit_keyPrompt.setVisible(False)
        self.keysPressed = []
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.lastKeyTime = None
        self.keyCombos = []
        self.updating_key_prompt = False
        self.changing_line_edit_text = False
        self.processing_line_edit_enter_pressed = False
        self.match = False
        self.last_indent = ""


        self.ui.lineEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.lineEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.ui.lineEdit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.ui.lineEdit.enterPressed.connect(self.lineEditEnterPressed)
        self.ui.lineEdit.backPressed.connect(self.backButton)
        self.ui.lineEdit.forwardPressed.connect(self.nextButton)
        self.ui.lineEdit.setNoDrawReturn()


        self.basePromptStyle = self.ui.label_keyPrompt.styleSheet()
        self.greenPromptStyle = re.sub(R"(?<!-)(color:\s*#[0-9a-fA-F]{3,6};)", "color: rgb(0, 170, 0);", self.basePromptStyle)

        self.baseLineEditStyle = self.ui.lineEdit.styleSheet()
        self.redLineEditStyle = re.sub(R"background-color:\s*#[0-9a-fA-F]{3,6};", "background-color: #ffbbbb;", self.baseLineEditStyle)
        self.greenLineEditStyle = re.sub(R"background-color:\s*#[0-9a-fA-F]{3,6};", "background-color: #bbffbb;", self.baseLineEditStyle)

        self.ui.textedit_keyPrompt.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.ui.textedit_keyPrompt.setWordWrapMode(QTextOption.WrapMode.NoWrap)

        self.promptLines = []
        self.promptLinesIndex = 0
        self.word_count = 0
        self.last_mode = self.ui.actionKey_Practice

        self.rawhid = RawHid()
        self.rawhid.keyEvent.connect(self.rawHidUpdate)
        self.rawhid.statusChanged.connect(self.rawHidStatusChanged)

        self.blocker = AltBlocker(self)
        self.menuBar().installEventFilter(self.blocker)

        self.translator = CharTranslator(self.ui.textedit_keyPrompt)
        self.ui.lineEdit.installEventFilter(self.translator)

        self.setWindowIcon(QIcon('icon-esc.svg'))

        self.status_label = QLabel("Standard Mode")
        self.statusBar().addPermanentWidget(self.status_label)

        QFontDatabase.addApplicationFont("NotoSerif-Regular.ttf")
        QFontDatabase.addApplicationFont("Lexend-Regular.ttf")
        QFontDatabase.addApplicationFont("FiraCode-Regular.ttf")

        self.typing_font_sizes = [6, 7, 8, 9, 10, 11, 12, 14, 16, 18]
        self.key_practice_font_sizes = [11, 12, 14, 16, 18, 20, 22, 24, 26, 28]
        def closest(target, values):
            return min(values, key=lambda x: abs(x - target))
        self.settings.typing.FontSize = closest(self.settings.typing.FontSize, self.typing_font_sizes)
        self.settings.code.FontSize = closest(self.settings.code.FontSize, self.typing_font_sizes)
        self.settings.words.FontSize = closest(self.settings.words.FontSize, self.key_practice_font_sizes)
        self.settings.key_practice.FontSize = closest(self.settings.key_practice.FontSize, self.key_practice_font_sizes)

        self.serif_font = QFont("Noto Serif", self.settings.typing.FontSize)
        self.serif_font.setKerning(False)
        self.sans_font = QFont("Lexend", self.settings.typing.FontSize)
        self.sans_font.setKerning(False)
        self.mono_font = QFont("Fira Code", self.settings.typing.FontSize)
        self.mono_font.setKerning(False)
        self.key_practice_font = QFont("Fira Code", self.settings.key_practice.FontSize)

        if self.settings.serif_font:
            self.text_font = self.serif_font
        else:
            self.text_font = self.sans_font
        self.setTypingFont(self.text_font)
        self.setKeyPracticeFont(self.key_practice_font)

        if self.settings.file.Filename:
            self._loadTypingPromptFile(filename=self.settings.file.Filename)

        lexer = self.settings.code_info.lexer
        self.highlighter = Highlighter(self.ui.textedit_keyPrompt.document())
        self.edit_highlighter = Highlighter(self.ui.lineEdit.document(), invert=True)
        self.highlighter.set_lexer(lexer or make_ngram_lexer(ngrams))
        self.edit_highlighter.set_lexer(lexer)

        self.initializing_key_flags = True
        self.ui.actionCombos.setChecked(self.settings.key_practice.Combos)
        self.ui.actionFunction.setChecked(self.settings.key_practice.Function)
        self.ui.actionLowercase.setChecked(self.settings.key_practice.Lowercase)
        self.ui.actionModifiers.setChecked(self.settings.key_practice.Modifiers)
        self.ui.actionNumbers.setChecked(self.settings.key_practice.Numbers)
        self.ui.actionSpecials.setChecked(self.settings.key_practice.Specials)
        self.ui.actionSymbols.setChecked(self.settings.key_practice.Symbols)
        self.ui.actionUppercase.setChecked(self.settings.key_practice.Uppercase)
        self.initializing_key_flags = False
        self.setKeyTypes()

        mode = self.settings.file.Mode
        if mode == ModeValue.Key_Practice:
            self.ui.actionKey_Practice.setChecked(True)
        elif mode == ModeValue.Typing_Practice:
            self.ui.actionTyping_Practice.setChecked(True)
        elif mode == ModeValue.Words_Top_10:
            self.ui.actionWords_Top_10.setChecked(True)
        elif mode == ModeValue.Words_Top_100:
            self.ui.actionWords_Top_100.setChecked(True)
        elif mode == ModeValue.Words_Top_1000:
            self.ui.actionWords_Top_1000.setChecked(True)
        elif mode == ModeValue.Words_All:
            self.ui.actionWords_All.setChecked(True)
        elif mode == ModeValue.Words_Ngrams:
            self.ui.actionN_Grams.setChecked(True)
        elif mode == ModeValue.Words_Containing_Ngrams:
            self.ui.actionWords_w_N_Grams.setChecked(True)

        self._load_mode_settings()

        if mode == ModeValue.Typing_Practice:
            QTimer.singleShot(0, self.updateNumPromptLines) # run after font and size are initialized
        self.ui.textedit_keyPrompt.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)


    def _load_mode_settings(self):
        self._restore_geometry()
        if (sf := self.settings.serif_font) is not None:
            self.ui.actionSerif_Font.setVisible(True)
            self.ui.actionSerif_Font.blockSignals(True)
            self.ui.actionSerif_Font.setChecked(sf)
            self.ui.actionSerif_Font.blockSignals(False)
            self.ui.actionSerif_Font.toggled.emit(sf)
        else:
            self.ui.actionSerif_Font.setVisible(False)
        if kp := (self.settings.file.Mode == ModeValue.Key_Practice):
            self.setKeyPracticeFontSize(self.settings.key_practice.FontSize)
            self.rawhid.start()
        elif self.settings.file.Mode == ModeValue.Typing_Practice:
            if self.settings.file_settings.IsCode:
                self.setCodeFontSize(self.settings.code.FontSize)
            else:
                self.setTypingFontSize(self.settings.typing.FontSize)
        else:
            self.setWordsFontSize(self.settings.words.FontSize)
        self.ui.actionAdvance_On_Enter.setVisible(not kp)
        self.ui.actionAdvance_On_Space.setVisible(not kp)
        if not kp:
            self.rawhid.stop()
            ms = self.settings.mode_settings
            self.ui.actionAdvance_On_Enter.setChecked(ms.AdvanceOnEnter)
            self.ui.actionAdvance_On_Space.setChecked(ms.AdvanceOnSpace)
        for x in (self.ui.actionCombos, self.ui.actionFunction, self.ui.actionLowercase,
                  self.ui.actionUppercase, self.ui.actionModifiers, self.ui.actionNumbers,
                  self.ui.actionSpecials, self.ui.actionSymbols):
            x.setVisible(kp)

    @qasync.asyncClose
    async def focusOutEvent(self, event):
        self.keysPressed.clear()
        await self.updateKeysPressed()

    def actionModeKey(self, state: bool):
        if state:
            self.ui.textedit_keyPrompt.setVisible(False)
            self.ui.label_keyPrompt.setVisible(True)
            self.ui.label_keysPressed.setText("")
            self.generateNewKeyPrompt()
            self.ui.lineEdit.setVisible(False)
            self.ui.label_keysPressed.setVisible(True)
            self.ui.pushButton_Back.setVisible(False)
            self.ui.label_line.setVisible(False)
            self.last_mode = self.ui.actionKey_Practice
            self.saveGeometry()
            self.settings.file.Mode = ModeValue.Key_Practice
            self._load_mode_settings()

    def actionModeTyping(self, state: bool):
        if state:
            if self.ui.actionTyping_Practice.isChecked():
                if len(self.promptLines) == 0 or self.word_count > 0:
                    if not self._ensure_file_loaded():
                        self.last_mode.setChecked(True)
                        return

            self.ui.label_keyPrompt.setVisible(False)
            self.ui.textedit_keyPrompt.setVisible(True)
            self.ui.lineEdit.setVisible(True)
            self.ui.label_keysPressed.setVisible(False)
            self.ui.lineEdit.setFocus()
            self.saveGeometry()
            if self.ui.actionKey_Practice.isChecked():
                self.settings.file.Mode = ModeValue.Key_Practice
            elif self.ui.actionTyping_Practice.isChecked():
                self.settings.file.Mode = ModeValue.Typing_Practice
            elif self.ui.actionWords_Top_10.isChecked():
                self.settings.file.Mode = ModeValue.Words_Top_10
            elif self.ui.actionWords_Top_100.isChecked():
                self.settings.file.Mode = ModeValue.Words_Top_100
            elif self.ui.actionWords_Top_1000.isChecked():
                self.settings.file.Mode = ModeValue.Words_Top_1000
            elif self.ui.actionWords_All.isChecked():
                self.settings.file.Mode = ModeValue.Words_All
            elif self.ui.actionN_Grams.isChecked():
                self.settings.file.Mode = ModeValue.Words_Ngrams
            elif self.ui.actionWords_w_N_Grams.isChecked():
                self.settings.file.Mode = ModeValue.Words_Containing_Ngrams

            if self.ui.actionTyping_Practice.isChecked():
                self.ui.label_line.setVisible(True)
                if not (len(self.promptLines) == 0 or self.word_count > 0):
                    self.ui.textedit_keyPrompt.setPlainText(self.typingPromptText)
                self.word_count = 0
                self.last_mode = self.ui.actionTyping_Practice
                lexer = self.settings.code_info.lexer
            else:
                self.ui.label_line.setVisible(False)
                if self.ui.actionN_Grams.isChecked():
                    self.promptLines = ngrams
                    self.word_count = len(self.promptLines)
                elif self.ui.actionWords_w_N_Grams.isChecked():
                    spc_words = [" " + word for word in words]
                    com_words = [", " + word for word in words]
                    spc_ngrams = [ngram for ngram in ngrams if ngram.startswith(" ")]
                    com_ngrams = [ngram for ngram in ngrams if ngram.startswith(", ")]
                    self.promptLines = [word for word in words if any(ngram in word for ngram in ngrams)]
                    self.promptLines.extend(word for word in spc_words if any(word.startswith(ngram) for ngram in spc_ngrams))
                    self.promptLines.extend(word for word in com_words if any(word.startswith(ngram) for ngram in com_ngrams))
                    self.word_count = len(self.promptLines)
                else:
                    _words = [x for x in words if len(x) > 1]
                    if self.ui.actionWords_Top_10.isChecked():
                        self.last_mode = self.ui.actionWords_Top_10
                        self.word_count = 10
                    elif self.ui.actionWords_Top_100.isChecked():
                        self.last_mode = self.ui.actionWords_Top_100
                        self.word_count = 100
                    elif self.ui.actionWords_Top_1000.isChecked():
                        self.last_mode = self.ui.actionWords_Top_1000
                        self.word_count = 1000
                    elif self.ui.actionWords_All.isChecked():
                        self.last_mode = self.ui.actionWords_All
                        self.word_count = len(_words)
                    self.promptLines = _words[:self.word_count]
                self.initTypingPrompt(rand=True)
                lexer = None
            if hasattr(self, "highlighter"):
                self.highlighter.set_lexer(lexer or make_ngram_lexer(ngrams))
                self.highlighter.rehighlight()
            if hasattr(self, "edit_highlighter"):
                self.edit_highlighter.set_lexer(lexer)
                self.edit_highlighter.rehighlight()
            self.initTypingFont()
            self._load_mode_settings()

    def _ensure_file_loaded(self):
        ret = False
        if self._loadTypingPromptFile(filename=self.settings.file.Filename):
            ret = True
        elif self.settings.file.Filename:
            if self._loadTypingPromptFile():
                ret = True
        return ret

    def setTypingFont(self, font):
        self.ui.textedit_keyPrompt.document().setDefaultFont(font)
        self.ui.textedit_keyPrompt.setFont(font)
        self.ui.lineEdit.document().setDefaultFont(font)
        self.ui.lineEdit.setFont(font)
        self.initTypingFont()

    def setKeyPracticeFont(self, font):
        self.ui.label_keyPrompt.setFont(font)
        self.ui.label_keysPressed.setFont(font)

    def keyPracticeFontSizeUp(self):
        size = self.ui.label_keyPrompt.font().pointSize()
        idx = min(len(self.key_practice_font_sizes)-1, bisect.bisect(self.key_practice_font_sizes, size))
        self.setKeyPracticeFontSize(self.key_practice_font_sizes[idx])

    def keyPracticeFontSizeDown(self):
        size = self.ui.label_keyPrompt.font().pointSize()
        idx = max(0, bisect.bisect_left(self.key_practice_font_sizes, size) - 1)
        self.setKeyPracticeFontSize(self.key_practice_font_sizes[idx])

    def setKeyPracticeFontSize(self, size):
        self.key_practice_font.setPointSize(size)
        self.setKeyPracticeFont(self.key_practice_font)
        self.settings.key_practice.FontSize = size

    def typingFontSizeUp(self):
        size = self.ui.lineEdit.font().pointSize()
        idx = min(len(self.typing_font_sizes)-1, bisect.bisect(self.typing_font_sizes, size))
        self.setTypingFontSize(self.typing_font_sizes[idx])

    def typingFontSizeDown(self):
        size = self.ui.lineEdit.font().pointSize()
        idx = max(0, bisect.bisect_left(self.typing_font_sizes, size) - 1)
        self.setTypingFontSize(self.typing_font_sizes[idx])

    def wordsFontSizeUp(self):
        size = self.ui.lineEdit.font().pointSize()
        idx = min(len(self.key_practice_font_sizes)-1, bisect.bisect(self.key_practice_font_sizes, size))
        self.setWordsFontSize(self.key_practice_font_sizes[idx])

    def wordsFontSizeDown(self):
        size = self.ui.lineEdit.font().pointSize()
        idx = max(0, bisect.bisect_left(self.key_practice_font_sizes, size) - 1)
        self.setWordsFontSize(self.key_practice_font_sizes[idx])

    def codeFontSizeUp(self):
        size = self.ui.lineEdit.font().pointSize()
        idx = min(len(self.typing_font_sizes)-1, bisect.bisect(self.typing_font_sizes, size))
        self.setCodeFontSize(self.typing_font_sizes[idx])

    def codeFontSizeDown(self):
        size = self.ui.lineEdit.font().pointSize()
        idx = max(0, bisect.bisect_left(self.typing_font_sizes, size) - 1)
        self.setCodeFontSize(self.typing_font_sizes[idx])

    def setTypingFontSize(self, size):
        self.serif_font.setPointSize(size)
        self.sans_font.setPointSize(size)
        if not self.settings.file_settings.IsCode:
            self.setTypingFont(self.text_font)
            self.initTypingFont()
        self.settings.typing.FontSize = size

    def setWordsFontSize(self, size):
        self.serif_font.setPointSize(size)
        self.sans_font.setPointSize(size)
        self.setTypingFont(self.text_font)
        self.initTypingFont()
        self.settings.words.FontSize = size

    def setCodeFontSize(self, size):
        self.mono_font.setPointSize(size)
        if self.settings.file_settings.IsCode:
            self.setTypingFont(self.mono_font)
            self.initTypingFont()
        self.settings.code.FontSize = size

    def plusButton(self):
        if self.settings.file.Mode == ModeValue.Key_Practice:
            self.keyPracticeFontSizeUp()
        elif self.settings.file.Mode == ModeValue.Typing_Practice:
            if self.settings.file_settings.IsCode:
                self.codeFontSizeUp()
            else:
                self.typingFontSizeUp()
        else:
            self.wordsFontSizeUp()

    def minusButton(self):
        if self.settings.file.Mode == ModeValue.Key_Practice:
            self.keyPracticeFontSizeDown()
        elif self.settings.file.Mode == ModeValue.Typing_Practice:
            if self.settings.file_settings.IsCode:
                self.codeFontSizeDown()
            else:
                self.typingFontSizeDown()
        else:
            self.wordsFontSizeDown()

    def initTypingFont(self):
        font_metrics = QFontMetricsF(self.ui.textedit_keyPrompt.font())
        line_height = font_metrics.lineSpacing()
        self.ui.lineEdit.setFixedHeight(int(line_height + self.ui.lineEdit.frameWidth() * 2 + 6))
        tab_stop_distance = font_metrics.horizontalAdvance(' ') * 4
        self.ui.textedit_keyPrompt.setTabStopDistance(tab_stop_distance)
        self.ui.lineEdit.setTabStopDistance(tab_stop_distance)
        if self.settings.file.Mode == ModeValue.Typing_Practice:
            self.updateNumPromptLines()

    def getNumberOfPromptLines(self):
        font_metrics = QFontMetricsF(self.ui.textedit_keyPrompt.font())
        line_height = font_metrics.lineSpacing()
        return math.ceil(self.ui.textedit_keyPrompt.height() / line_height)


    def loadTypingPromptFile(self):
        file = self.settings.file.Filename
        self.settings.file.Filename = None
        if self.settings.file.Mode != ModeValue.Typing_Practice:
            self.ui.actionTyping_Practice.setChecked(True)
        else:
            if self._loadTypingPromptFile():
                self._load_mode_settings()
        if not self.settings.file.Filename:
            self.settings.file.Filename = file


    def _loadTypingPromptFile(self, *, filename=None) -> bool:
        if not filename:
            inputFile = QFileDialog.getOpenFileName(self,
                "Open Text File",
                "",
                "Text and Code Files (*.txt *.md *.rtf *.ini *.cfg *.conf *.log *.csv *.json *.xml *.yaml *.yml "
                "*.py *.c *.cpp *.h *.hpp *.ino *.java *.js *.ts *.html *.htm *.css *.scss *.bat *.sh *.ps1 *.ahk "
                "*.php *.rb *.go *.rs *.swift *.lua *.pl *.sql *.asm *.s *.vhd *.vhdl *.verilog);;"
                "All Files (*)"
            )
            if not (filename := inputFile[0]):
                return False
        elif not (filename := self.settings.file.Filename):
            return False
        try:
            inputText = Path(filename).read_text(encoding="utf-8-sig")
            if not inputText:
                return False
        except:
            return False

        sha256 = hashlib.sha256(inputText.encode("utf-8")).hexdigest()
        self.settings.file.Filename = filename
        self.settings.file.Sha256 = sha256
        if self.settings.have_file(filename, sha256):
            code_info = self.settings.code_info
        else:
            code_info = detect_code_info(filename, inputText)
            self.settings.set_code_info(code_info)

        if hasattr(self, "highlighter"):
            self.highlighter.set_lexer(code_info.lexer or make_ngram_lexer(ngrams))
        if hasattr(self, "edit_highlighter"):
            self.edit_highlighter.set_lexer(code_info.lexer)
        if code_info.is_code:
            self.setCodeFontSize(self.settings.code.FontSize)
            if code_info.indent_type == IndentType.space:
                self.ui.lineEdit.setIndentWithSpaces(code_info.indent_size)
            else:
                self.ui.lineEdit.setIndentWithTabs()
        else:
            self.setTypingFontSize(self.settings.typing.FontSize)
            self.ui.lineEdit.setIndentWithTabs()
        self.promptLines = inputText.split("\n")
        self.initTypingPrompt(line=self.settings.file_settings.Line)
        return True

    def initTypingPrompt(self, *, line=0, rand=False):
        self.startTime = None
        if rand:
            self.setTypingPromptLine(random.randrange(len(self.promptLines)), typingMode=False)
        else:
            self.setTypingPromptLine(line)
        if self.settings.file.Mode != ModeValue.Key_Practice:
            self.ui.lineEdit.setFocus()

    def nextButton(self):
        if self.settings.file.Mode == ModeValue.Key_Practice:
            self.generateNewKeyPrompt(doTime=False)
        else:
            self.nextTypingPromptLine(doTime=False)
            self.ui.lineEdit.setFocus()

    def backButton(self):
        self.setTypingPromptLine(self.promptLinesIndex - 1, doTime=False)
        self.ui.lineEdit.setFocus()

    def actionAdvanceOnEnter(self, state: bool):
        self.settings.mode_settings.AdvanceOnEnter = state

    def actionAdvanceOnSpace(self, state: bool):
        self.settings.mode_settings.AdvanceOnSpace = state

    def actionSerifFont(self, state: bool):
        if state:
            self.text_font = self.serif_font
        else:
            self.text_font = self.sans_font
        self.settings.serif_font = state
        if not self.settings.file_settings.IsCode:
            self.setTypingFont(self.text_font)

    def nextTypingPromptLine(self, *, doTime=True):
        if self.settings.file.Mode == ModeValue.Typing_Practice:
            self.setTypingPromptLine(self.promptLinesIndex + 1, doTime=doTime)
        else: # Word mode
            if len(self.promptLines) <= 1:
                i = 0
            else:
                i = random.randrange(len(self.promptLines)-1)
                if i >= self.promptLinesIndex:
                    i += 1
            self.setTypingPromptLine(i, doTime=doTime, typingMode=False)

    def WPM(self, text, secs):
        if text:
            return (text/5.0) / (secs/60.0)


    def setTypingPromptLine(self, line: int, *, doTime=True, typingMode=True):
        if line < 0:
            return
        t = time.time()
        if doTime and self.startTime and (t - self.startTime) > 0:
            chars_typed = len(self.typingPromptText.split("\n")[0])
            if (wpm := self.WPM(chars_typed, t - self.startTime)):
                self.ui.label_keysPerSecond.setText(F"WPM: {wpm:0.2f}")
            else:
                self.ui.label_keysPerSecond.setText(F"WPM: --")
        else:
            self.ui.label_keysPerSecond.setText(F"WPM: --")
        self.startTime = t
        if line > 0 and typingMode:
            self.ui.pushButton_Back.setVisible(True)
        else:
            self.ui.pushButton_Back.setVisible(False)
        if typingMode:
            lines = self.getNumberOfPromptLines()
        else:
            lines = 1
        self.promptLinesIndex = line
        if typingMode:
            self.settings.file_settings.Line = line
        self.ui.label_line.setText(F"{line+1} / {len(self.promptLines)}")
        line %= len(self.promptLines)
        self.typingPromptText = '\n'.join(self.promptLines[line : line + lines])
        self.ui.textedit_keyPrompt.setTypedChars(0)
        self.ui.textedit_keyPrompt.setPlainText(self.typingPromptText)
        self.ui.lineEdit.setTypedChars(0, invert=True)
        self.changing_line_edit_text = False
        if len(self.ui.lineEdit.toPlainText()) > 0:
            self.ui.lineEdit.clear()
        else:
            self.lineEditTextChanged()
        if self.settings.file.Mode == ModeValue.Typing_Practice and self.settings.file_settings.IsCode and len(self.promptLines[line]) >= len(self.last_indent):
            self.ui.lineEdit.textCursor().insertText(self.last_indent)
        else:
            self.last_indent = ""

    def updateNumPromptLines(self):
        lines = self.getNumberOfPromptLines()
        self.typingPromptText = '\n'.join(self.promptLines[self.promptLinesIndex : self.promptLinesIndex + lines])
        self.ui.textedit_keyPrompt.setPlainText(self.typingPromptText)
        if hasattr(self, "highlighter"):
            self.highlighter.rehighlight()

    def lineEditTextChanged(self):
        if self.changing_line_edit_text:
            return
        self.changing_line_edit_text = True
        typed = self.ui.lineEdit.toPlainText()
        if len(typed) == 1 and len(self.typingPromptText) > 1:
            self.startTime = time.time()
        if self.settings.file.Mode != ModeValue.Key_Practice:
            prompt_idx, typed_idx = 0, 0
            prompt = self.typingPromptText.split("\n")[0]
            match = True
            for prompt_idx, c in enumerate(prompt):
                if typed_idx >= len(typed):
                    match = False
                    break
                if c == typed[typed_idx]:
                    typed_idx = typed_idx+1
                    continue
                if not self.settings.file_settings.IsCode:
                    if (c == ' ' or c == '\t'):
                        if typed_idx > 0 and typed[typed_idx-1] == ' ':
                            continue
                match = False
                break
            else:
                if prompt_idx > 0:
                    prompt_idx = prompt_idx+1
            if typed_idx < len(typed):
                match = False

            self.ui.textedit_keyPrompt.setTypedChars(prompt_idx)
            self.ui.lineEdit.setTypedChars(typed_idx, invert=True)
            if hasattr(self, "highlighter"):
                self.highlighter.setHighlightLen(prompt_idx)
                self.highlighter.rehighlight()
            if hasattr(self, "edit_highlighter"):
                self.edit_highlighter.setHighlightLen(typed_idx)
                self.edit_highlighter.rehighlight()
            ms = self.settings.mode_settings
            if ms.AdvanceOnSpace and self.match and not match and len(typed) > 0 and typed[-1] == ' ':
                self.attemptAdvance.emit()
            else:
                self.match = match
            if self.match and not (ms.AdvanceOnEnter or ms.AdvanceOnSpace):
                self.attemptAdvance.emit()

        self.changing_line_edit_text = False

    @qasync.asyncSlot()
    async def lineEditEnterPressed(self):
        if self.settings.mode_settings.AdvanceOnEnter:
            await self.attemptPromptAdvance()

    @qasync.asyncSlot()
    async def attemptPromptAdvance(self):
        if self.processing_line_edit_enter_pressed:
            return
        self.processing_line_edit_enter_pressed = True
        if self.match:
            if self.settings.file_settings.IsCode:
                m = re.match(r'^[ \t]+', self.ui.lineEdit.toPlainText())
                self.last_indent = m.group(0) if m else ""
            self.nextTypingPromptLine()
        else:
            self.ui.lineEdit.setStyleSheet(self.redLineEditStyle)
            await asyncio.sleep(0.2)
            self.ui.lineEdit.setStyleSheet(self.baseLineEditStyle)
        self.processing_line_edit_enter_pressed = False

    def keyTypeToggled(self, _: bool):
        if not self.initializing_key_flags:
            self.setKeyTypes()

    def setKeyTypes(self):
        self.keyCombos = []
        if self.ui.actionCombos.isChecked():
            self.keyCombos += combos.combos
        if self.ui.actionFunction.isChecked():
            self.keyCombos += combos.function
        if self.ui.actionLowercase.isChecked():
            self.keyCombos += combos.lowercase
        if self.ui.actionModifiers.isChecked():
            self.keyCombos += combos.modifiers
        if self.ui.actionNumbers.isChecked():
            self.keyCombos += combos.numbers
        if self.ui.actionSpecials.isChecked():
            self.keyCombos += combos.specials
        if self.ui.actionSymbols.isChecked():
            self.keyCombos += combos.symbols
        if self.ui.actionUppercase.isChecked():
            self.keyCombos += combos.uppercase
        if len(self.keyCombos) == 0:
            self.keyCombos = [scancode.Esc]
        self.generateNewKeyPrompt()
        self.settings.key_practice.Combos = self.ui.actionCombos.isChecked()
        self.settings.key_practice.Function = self.ui.actionFunction.isChecked()
        self.settings.key_practice.Lowercase = self.ui.actionLowercase.isChecked()
        self.settings.key_practice.Modifiers = self.ui.actionModifiers.isChecked()
        self.settings.key_practice.Numbers = self.ui.actionNumbers.isChecked()
        self.settings.key_practice.Specials = self.ui.actionSpecials.isChecked()
        self.settings.key_practice.Symbols = self.ui.actionSymbols.isChecked()
        self.settings.key_practice.Uppercase = self.ui.actionUppercase.isChecked()

    def eventFilter(self, source, event: QKeyEvent):
        if (t := event.type()) in [QEvent.Type.KeyPress, QEvent.Type.KeyRelease]:
            if not self.rawhid.active:
                if self.settings.file.Mode == ModeValue.Key_Practice:
                    if not event.isAutoRepeat():
                        sc = event.nativeScanCode()
                        if not (k := processScancode(sc)):
                            print(F"Unrecognized scancode {sc}")
                        else:
                            if t == QEvent.Type.KeyPress:
                                asyncio.create_task(self.handle_key_pressed(k, event.modifiers()))
                            else:
                                asyncio.create_task(self.handle_key_released(k))
                    return True
        return False

    async def handle_key_pressed(self, k: scancode, mods):
        mods_pressed = [x[1] for x in zip(QT_MODS, SCANCODE_MODS) if x[0] & mods]
        if k == scancode.LWin and scancode.LWin not in mods_pressed:
            mods_pressed.append(k)
        self.keysPressed = [x for x in self.keysPressed if x not in SCANCODE_MODS]
        if k not in SCANCODE_MODS:
            if not [x for x in self.keysPressed if k in (x if isinstance(x, tuple) else (x,))]:
                self.keysPressed.append(k if not mods_pressed else (*mods_pressed, k))
        mods_pressed = [x for x in mods_pressed if not self.keysPressed or not all(x in (y if isinstance(y, tuple) else (y,)) for y in self.keysPressed)]
        self.keysPressed = [*mods_pressed, *self.keysPressed]
        await self.updateKeysPressed()

    async def handle_key_released(self, k: scancode):
        if k in SCANCODE_MODS:
            self.keysPressed = [x for x in self.keysPressed if k != x]
        else:
            self.keysPressed = [x for x in self.keysPressed if k not in (x if isinstance(x, tuple) else (x,))]
        await self.updateKeysPressed()

    @qasync.asyncSlot(object)
    async def rawHidUpdate(self, keys):
        if self.rawhid.active:
            if self.settings.file.Mode == ModeValue.Key_Practice:
                self.keysPressed = keys
                await self.updateKeysPressed()

    def rawHidStatusChanged(self):
        if self.rawhid.active:
            self.status_label.setText("QMK Direct Mode")
        else:
            self.status_label.setText("Standard Mode")

    def makeKeyString(self, keys):
        return '+'.join(keynames.get(k) or (F"({self.makeKeyString(k)})" if isinstance(k, tuple) else "UnknownKey") for k in keys)
    
    async def updateKeysPressed(self):
        self.ui.label_keysPressed.setText(self.makeKeyString(self.keysPressed))
        if self.keysPressed == self.keyPromptKeys():
            await self.updateKeyPrompt()

    async def updateKeyPrompt(self):
        if self.updating_key_prompt:
            return
        self.updating_key_prompt = True
        self.ui.label_keyPrompt.setStyleSheet(self.greenPromptStyle)
        await asyncio.sleep(0.2)
        self.ui.label_keyPrompt.setStyleSheet(self.basePromptStyle)
        self.generateNewKeyPrompt()
        self.updating_key_prompt = False

    def keyPromptKeys(self):
        if isinstance(self.keyPrompt, tuple):
            return self.keyPrompt[0]
        else:
            return self.keyPrompt

    def keyPromptDesc(self):
        if isinstance(self.keyPrompt, tuple):
            return self.keyPrompt[1]

    def updateKeyPromptText(self):
        # if self.ui.actionOnly_description_for_combos.isChecked():
        #     self.ui.label_keyPrompt.setText(self.keyPromptDesc())
        # else:
        self.ui.label_keyPrompt.setText(self.makeKeyString(self.keyPromptKeys()))

    def generateNewKeyPrompt(self, *, doTime=True):
        self.keyPrompt = self.keyCombos[random.randrange(len(self.keyCombos))]
        self.updateKeyPromptText()
        t = time.time()
        if not doTime or (not self.lastKeyTime) or (t - self.lastKeyTime) > 5:
            self.startTime = t
            self.lastKeyTime = t
            self.totalKeysPressed = 0
            self.ui.label_keysPerSecond.setText("WPM: --")
        else:
            self.lastKeyTime = t
            self.totalKeysPressed += 1
            if self.startTime is None:
                raise Exception()
            self.ui.label_keysPerSecond.setText(F"WPM: {self.WPM(self.totalKeysPressed, t - self.startTime):0.2f}")

    def resizeEvent(self, event):
        if self.settings.file.Mode == ModeValue.Typing_Practice:
            self.updateNumPromptLines()
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.saveGeometry()
        super().closeEvent(event)

    def saveGeometry(self):
        if self._goemetry_initialized:
            ret = super().saveGeometry()
            self.settings.window_geometry.WindowGeometry = ret
            return ret

    def _restore_geometry(self):
        self._goemetry_initialized = True
        geom = self.settings.window_geometry.WindowGeometry
        if geom and isinstance(geom, QByteArray):
            self.restoreGeometry(geom)
            rect = self.frameGeometry()
            screen = QGuiApplication.primaryScreen().availableGeometry()
            if not screen.intersects(rect):
                self.move(screen.center() - self.rect().center())



class AltBlocker(QObject):
    def eventFilter(self, obj, e):
        if e.type() == QEvent.Type.ShortcutOverride and e.key() == Qt.Key.Key_Alt:
            return True
        if e.type() == QEvent.Type.KeyPress and e.key() == Qt.Key.Key_Alt:
            return True
        return super().eventFilter(obj, e)
    
class CharTranslator(QObject):
    def __init__(self, prompt: QPlainTextEdit):
        super().__init__()
        self.prompt = prompt
    def eventFilter(self, obj: QPlainTextEdit, e: QKeyEvent):
        if e.type() == QEvent.Type.KeyPress:
            if c := e.text():
                if promptText := self.prompt.toPlainText().split("\n")[0]:
                    cursor = obj.textCursor()
                    pos = cursor.position()
                    if len(promptText) > pos:
                        if p := char_translations.get(promptText[pos]):
                            if p == c:
                                cursor.insertText(promptText[pos])
                                return True
        return super().eventFilter(obj, e)


if __name__ == "__main__":
    # os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # os.environ["QT_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication([])
    app.setStyle("windowsvista")
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    main_window = mainWindow()
    app.installEventFilter(main_window)
    if sys.platform == "win32":
        myappid = u'windexlight.mappingtrainer.app.1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    main_window.show()
    with loop:
        loop.run_forever()
