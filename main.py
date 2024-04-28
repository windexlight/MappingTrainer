import asyncio
import os
import random

import qasync
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QKeyEvent
from PyQt5.QtWidgets import (QDialog, QFileDialog, QHeaderView, QInputDialog,
                             QLabel, QMessageBox, QTableWidgetItem, QAbstractButton, QCheckBox)
from windowMain import Ui_mainWindow
from keynames import keyNames
from scancodes import *
from combos import *

class mainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.keysPressed = []
        self.setFocusPolicy(Qt.StrongFocus)
        self.updateKeyPrompt()

    def focusOutEvent(self, event):
        self.keysPressed.clear()
        self.updateKeysPressed()

    def keyPressEvent(self, event: QKeyEvent):
        if not event.isAutoRepeat():
            sc = event.nativeScanCode()
            if not (k := processScancode(sc)):
                print(F"Unrecognized scancode {sc} pressed")
                return
            if k not in self.keysPressed:
                self.keysPressed.append(k)
            self.updateKeysPressed()
            if self.keysPressed == self.keyPrompt:
                self.updateKeyPrompt()
            # print(F"{scancodeNames[k]} pressed")

    def keyReleaseEvent(self, event: QKeyEvent):
        if not event.isAutoRepeat():
            sc = event.nativeScanCode()
            if not (k := processScancode(sc)):
                print(F"Unrecognized scancode {sc} released")
                return
            self.keysPressed = [i for i in self.keysPressed if i != k]
            self.updateKeysPressed()
            if self.keysPressed == self.keyPrompt:
                self.updateKeyPrompt()
            # print(F"{scancodeNames[k]} released")

    def makeKeyString(self, keys):
        if (combo := tuple(keys)) in scancodeNames:
            return scancodeNames[combo]
        return '+'.join(map(lambda k: scancodeNames[k], keys))
    
    def updateKeysPressed(self):
        self.ui.label_keysPressed.setText(self.makeKeyString(self.keysPressed))

    def updateKeyPrompt(self):
        self.keyPrompt = keyCombos[random.randrange(len(keyCombos))]
        self.ui.label_keyPrompt.setText(self.makeKeyString(self.keyPrompt))


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
