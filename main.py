import asyncio
import configparser
import os
import random
import time
import re
from pathlib import Path

import qasync
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QKeyEvent
from PyQt5.QtWidgets import (QDialog, QFileDialog, QHeaderView, QInputDialog,
                             QLabel, QMessageBox, QTableWidgetItem, QAbstractButton, QCheckBox, QActionGroup)
from ui_mainWindow import Ui_MainWindow
from keynames import keyNames
from scancodes import *
import combos
from words_no_swears import words

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.config = configparser.ConfigParser(delimiters=('='))
        self.config.read("settings.ini")
        if "LINES" not in self.config:
            self.config["LINES"] = {}
        self.modeActionGroup = QActionGroup(self)
        self.modeActionGroup.addAction(self.ui.actionKey_Practice)
        self.modeActionGroup.addAction(self.ui.actionTyping_Practice)
        self.modeActionGroup.addAction(self.ui.actionWords_Top_10)
        self.modeActionGroup.addAction(self.ui.actionWords_Top_100)
        self.modeActionGroup.addAction(self.ui.actionWords_Top_1000)
        self.modeActionGroup.addAction(self.ui.actionWords_All)
        self.ui.lineEdit.setVisible(False)
        self.ui.lineEdit.setStyleSheet("font-family: Aptos; font-weight: normal; font-size: 11pt;")
        self.ui.pushButton_Back.setVisible(False)
        self.ui.label_line.setVisible(False)
        self.keysPressed = []
        self.setFocusPolicy(Qt.StrongFocus)
        self.lastKeyTime = None
        self.keyCombos = []
        self.setKeyTypes()
        self.updatingKeyPrompt = False
        self.basePromptStyle = self.ui.label_keyPrompt.styleSheet()
        self.promptLines = []
        self.promptLinesIndex = 0
        self.word_count = 0
        self.last_mode = self.ui.actionKey_Practice
        self.filename = None

    def saveConfig(self):
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)

    def focusOutEvent(self, event):
        self.keysPressed.clear()
        self.updateKeysPressed()

    def actionModeKey(self, state: bool):
        if state:
            self.ui.label_keyPrompt.setStyleSheet(self.basePromptStyle)
            self.ui.label_keysPressed.setText("")
            self.generateNewKeyPrompt()
            self.ui.label_keyPrompt.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.ui.lineEdit.setVisible(False)
            self.ui.label_keysPressed.setVisible(True)
            self.ui.pushButton_Back.setVisible(False)
            self.ui.label_line.setVisible(False)
            self.last_mode = self.ui.actionKey_Practice

    def actionModeTyping(self, state: bool):
        if state:
            if self.ui.actionTyping_Practice.isChecked():
                if len(self.promptLines) == 0 or self.word_count > 0:
                    if not self.loadTypingPromptFile():
                        self.last_mode.setChecked()
                        return
                else:
                    self.ui.label_keyPrompt.setText(self.typingPromptText)
                self.ui.label_line.setVisible(True)
                self.word_count = 0
                self.last_mode = self.ui.actionTyping_Practice
            else:
                self.ui.label_line.setVisible(False)
                self.filename = None
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
                self.initTypingPrompt()
            self.ui.label_keyPrompt.setStyleSheet(self.basePromptStyle +
                "font-family: Aptos; font-weight: normal; padding: 0.5px; font-size: 11pt; text-align: left;")
            self.ui.label_keyPrompt.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.ui.lineEdit.setVisible(True)
            self.ui.label_keysPressed.setVisible(False)
            self.ui.lineEdit.setFocus()

    def loadTypingPromptFile(self) -> bool:
        inputFile = QFileDialog.getOpenFileName(self, "Choose text file", "", "Text Files (*.txt)")
        if not (filename := inputFile[0]):
            return False
        inputText = Path(filename).read_text(encoding="utf-8-sig")
        if inputText[-1] != '\n':
            inputText = inputText + '\n'
        filters = r'\n'
        if self.ui.actionSplit_file_by_period.isChecked():
            filters = filters + r'\.\?!'
        self.promptLines = [s.strip() for s in re.split(fr'(.+?[{filters}])', inputText)[1::2] or [inputText] if len(s.strip()) > 0]
        self.filename = filename
        self.initTypingPrompt(line=self.config.getint("LINES", filename, fallback=0))
        return True

    def initTypingPrompt(self, *, line=0):
        self.startTime = None
        if self.ui.actionStart_file_in_random_location.isChecked() or not self.ui.actionTyping_Practice.isChecked():
            self.setTypingPromptLine(random.randrange(len(self.promptLines)))
        else:
            self.setTypingPromptLine(line)
        if not self.ui.actionKey_Practice.isChecked():
            self.ui.lineEdit.setFocus()

    def nextButton(self):
        if self.ui.actionKey_Practice.isChecked():
            self.generateNewKeyPrompt(doTime=False)
        else:
            self.nextTypingPromptLine(doTime=False)
            self.ui.lineEdit.setFocus()

    def backButton(self):
        self.setTypingPromptLine(self.promptLinesIndex - 1, doTime=False)
        self.ui.lineEdit.setFocus()

    def actionSkipQuote(self, state: bool):
        if not self.ui.actionKey_Practice.isChecked():
            self.lineEditTextChanged(self.ui.lineEdit.text())

    def nextTypingPromptLine(self, *, doTime=True):
        if self.ui.actionTyping_Practice.isChecked():
            self.setTypingPromptLine(self.promptLinesIndex + 1, doTime=doTime)
        else:
            while (i := random.randrange(len(self.promptLines))) == self.promptLinesIndex:
                pass
            self.setTypingPromptLine(i, doTime=doTime)

    def setTypingPromptLine(self, line: int, *, doTime=True):
        if line < 0:
            return
        t = time.time()
        if doTime and self.startTime and (t - self.startTime) > 0:
            self.ui.label_keysPerSecond.setText(F"KPS: {len(self.typingPromptText) / (t - self.startTime):0.2f}")
        else:
            self.ui.label_keysPerSecond.setText(F"KPS: --")
        self.startTime = t
        if line > 0 and self.ui.actionTyping_Practice.isChecked():
            self.ui.pushButton_Back.setVisible(True)
        else:
            self.ui.pushButton_Back.setVisible(False)
        self.promptLinesIndex = line
        if self.filename is not None:
            self.config["LINES"][self.filename] = str(line)
            self.saveConfig()
        self.ui.label_line.setText(F"{line} / {len(self.promptLines)}")
        self.typingPromptText = self.promptLines[line % len(self.promptLines)]
        self.ui.label_keyPrompt.setText(self.typingPromptText)
        if len(self.ui.lineEdit.text()) > 0:
            self.ui.lineEdit.clear()
        else:
            self.lineEditTextChanged("")

    def lineEditTextChanged(self, text: str):
        if len(text) == 1 and len(self.typingPromptText) > 1:
            self.startTime = time.time()
        if not self.ui.actionKey_Practice.isChecked():
            i, j = 0, 0
            match = True
            for i, c in enumerate(self.typingPromptText):
                if j >= len(text):
                    match = False
                    break
                if c == text[j]:
                    j = j+1
                    continue
                if c == ' ' or c == '\t':
                    if j > 0 and text[j-1] == ' ':
                        continue
                if self.ui.actionAllow_skip_quote.isChecked() and c == '\"':
                    continue
                match = False
                break
            # match = os.path.commonprefix([text, p := self.typingPromptText])
            p = self.typingPromptText
            self.ui.label_keyPrompt.setText(F"<span style=\"color:rgb(0, 170, 0);\">{p[0:i]}</span>{p[i:]}")
            if match: # i == len(self.typingPromptText): #text == p:
                self.nextTypingPromptLine()

    def keyTypeToggled(self, _: bool):
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

    @qasync.asyncClose
    async def keyPressEvent(self, event: QKeyEvent):
        if self.ui.actionKey_Practice.isChecked():
            if not event.isAutoRepeat():
                sc = event.nativeScanCode()
                if not (k := processScancode(sc)):
                    print(F"Unrecognized scancode {sc} pressed")
                    return
                if k not in self.keysPressed:
                    self.keysPressed.append(k)
                self.updateKeysPressed()
                if self.keysPressed == self.keyPrompt:
                    await self.updateKeyPrompt()
                # print(F"{scancodeNames[k]} pressed")

    @qasync.asyncClose
    async def keyReleaseEvent(self, event: QKeyEvent):
        if self.ui.actionKey_Practice.isChecked():
            if not event.isAutoRepeat():
                sc = event.nativeScanCode()
                if not (k := processScancode(sc)):
                    print(F"Unrecognized scancode {sc} released")
                    return
                self.keysPressed = [i for i in self.keysPressed if i != k]
                self.updateKeysPressed()
                if self.keysPressed == self.keyPrompt:
                    await self.updateKeyPrompt()
                # print(F"{scancodeNames[k]} released")

    def makeKeyString(self, keys):
        if (combo := tuple(keys)) in scancodeNames:
            return scancodeNames[combo]
        return '+'.join(map(lambda k: scancodeNames[k], keys))
    
    def updateKeysPressed(self):
        self.ui.label_keysPressed.setText(self.makeKeyString(self.keysPressed))

    async def updateKeyPrompt(self):
        if self.updatingKeyPrompt:
            return
        self.updatingKeyPrompt = True
        style = self.ui.label_keyPrompt.styleSheet()
        self.ui.label_keyPrompt.setStyleSheet(style + "color: rgb(0, 170, 0);")
        await asyncio.sleep(0.2)
        self.ui.label_keyPrompt.setStyleSheet(style)
        self.generateNewKeyPrompt()
        self.updatingKeyPrompt = False

    def generateNewKeyPrompt(self, *, doTime=True):
        self.keyPrompt = self.keyCombos[random.randrange(len(self.keyCombos))]
        self.ui.label_keyPrompt.setText(self.makeKeyString(self.keyPrompt))
        t = time.time()
        if not doTime or (not self.lastKeyTime) or (t - self.lastKeyTime) > 5:
            self.startTime = t
            self.lastKeyTime = t
            self.totalKeysPressed = 0
            self.ui.label_keysPerSecond.setText("KPS: --")
        else:
            self.lastKeyTime = t
            self.totalKeysPressed += 1
            self.ui.label_keysPerSecond.setText(F"KPS: {self.totalKeysPressed / (t - self.startTime):0.2f}")


if __name__ == "__main__":
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    os.environ["QT_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication([])
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    main_window = mainWindow()
    main_window.show()
    with loop:
        loop.run_forever()
