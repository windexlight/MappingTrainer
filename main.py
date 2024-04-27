import asyncio
import os

import qasync
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QKeyEvent
from PyQt5.QtWidgets import (QDialog, QFileDialog, QHeaderView, QInputDialog,
                             QLabel, QMessageBox, QTableWidgetItem, QAbstractButton, QCheckBox)
from windowMain import Ui_Form
from keynames import keyNames
from scancodenames import scancodes

class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.keysPressed = []
        self.setFocusPolicy(Qt.StrongFocus)

    def focusOutEvent(self, event):
        self.keysPressed.clear()
        self.updateKeysPressed()

    def keyPressEvent(self, event: QKeyEvent):
        if not event.isAutoRepeat():
            k = event.nativeScanCode() #.key()
            if k not in scancodes:
                print(F"Unrecognized scancode {k} pressed")
                return
            if k not in self.keysPressed:
                self.keysPressed.append(k)
            self.updateKeysPressed()
            print(F"{scancodes[k]} pressed")

    def keyReleaseEvent(self, event: QKeyEvent):
        if not event.isAutoRepeat():
            k = event.nativeScanCode() #.key()
            if k not in scancodes:
                print(F"Unrecognized scancode {k} released")
                return
            self.keysPressed = [i for i in self.keysPressed if i != k]
            self.updateKeysPressed()
            print(F"{scancodes[k]} released")

    def sayKeysPressed(self):
        return '+'.join(map(lambda k: scancodes[k], self.keysPressed))
    
    def updateKeysPressed(self):
        self.ui.label_keyPrompt.setText(self.sayKeysPressed())


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
