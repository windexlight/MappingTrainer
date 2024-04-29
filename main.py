import asyncio
import os
import random
import time

import qasync
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QKeyEvent
from PyQt5.QtWidgets import (QDialog, QFileDialog, QHeaderView, QInputDialog,
                             QLabel, QMessageBox, QTableWidgetItem, QAbstractButton, QCheckBox, QActionGroup)
from ui_mainWindow import Ui_MainWindow
from keynames import keyNames
from scancodes import *
from combos import *

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.modeActionGroup = QActionGroup(self)
        self.modeActionGroup.addAction(self.ui.actionKey_Practice)
        self.modeActionGroup.addAction(self.ui.actionTyping_Practice)
        self.ui.lineEdit.setVisible(False)
        self.ui.lineEdit.setStyleSheet("font-family: Aptos; font-weight: normal; font-size: 11pt;")
        self.keysPressed = []
        self.setFocusPolicy(Qt.StrongFocus)
        self.lastKeyTime = time.time() - 100
        self.generateNewKeyPrompt()
        self.updatingKeyPrompt = False
        self.basePromptStyle = self.ui.label_keyPrompt.styleSheet()

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

    def actionModeTyping(self, state: bool):
        if state:
            inputFile = QFileDialog.getOpenFileName(self, "Choose text file", "", "Text Files (*.txt)")
            self.typingPromptText = "The dog is dumb and it leaves much to be desired."
            self.ui.label_keyPrompt.setStyleSheet(self.basePromptStyle +
                "font-family: Aptos; font-weight: normal; padding: 0.5px; font-size: 11pt; text-align: left;")
            self.ui.label_keyPrompt.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.ui.lineEdit.clear()
            self.ui.lineEdit.setVisible(True)
            self.ui.label_keysPressed.setVisible(False)
            self.ui.label_keyPrompt.setText(self.typingPromptText)
            self.ui.lineEdit.setFocus()

    def lineEditTextChanged(self, text: str):
        if self.ui.actionTyping_Practice.isChecked():
            match = os.path.commonprefix([text, prompt := self.typingPromptText])
            self.ui.label_keyPrompt.setText(F"<span style=\"color:rgb(0, 170, 0);\">{prompt[0:len(match)]}</span>{prompt[len(match):]}")


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

    def generateNewKeyPrompt(self):
        self.keyPrompt = keyCombos[random.randrange(len(keyCombos))]
        self.ui.label_keyPrompt.setText(self.makeKeyString(self.keyPrompt))
        if ((t := time.time()) - self.lastKeyTime) > 5:
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
