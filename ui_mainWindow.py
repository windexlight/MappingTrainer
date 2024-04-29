# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(527, 292)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_keysPerSecond = QtWidgets.QLabel(self.centralwidget)
        self.label_keysPerSecond.setMaximumSize(QtCore.QSize(16777215, 16))
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(10)
        self.label_keysPerSecond.setFont(font)
        self.label_keysPerSecond.setAlignment(QtCore.Qt.AlignCenter)
        self.label_keysPerSecond.setObjectName("label_keysPerSecond")
        self.verticalLayout.addWidget(self.label_keysPerSecond)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_keysPressed = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_keysPressed.setFont(font)
        self.label_keysPressed.setStyleSheet("background-color: rgb(223, 255, 255);")
        self.label_keysPressed.setText("")
        self.label_keysPressed.setAlignment(QtCore.Qt.AlignCenter)
        self.label_keysPressed.setObjectName("label_keysPressed")
        self.horizontalLayout.addWidget(self.label_keysPressed)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setAcceptDrops(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_keyPrompt = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_keyPrompt.sizePolicy().hasHeightForWidth())
        self.label_keyPrompt.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Cascadia Code")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_keyPrompt.setFont(font)
        self.label_keyPrompt.setStyleSheet("background-color: rgb(223, 255, 255);")
        self.label_keyPrompt.setScaledContents(False)
        self.label_keyPrompt.setAlignment(QtCore.Qt.AlignCenter)
        self.label_keyPrompt.setWordWrap(True)
        self.label_keyPrompt.setObjectName("label_keyPrompt")
        self.verticalLayout.addWidget(self.label_keyPrompt)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 527, 26))
        self.menubar.setObjectName("menubar")
        self.menuMode = QtWidgets.QMenu(self.menubar)
        self.menuMode.setObjectName("menuMode")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionKey_Practice = QtWidgets.QAction(MainWindow)
        self.actionKey_Practice.setCheckable(True)
        self.actionKey_Practice.setChecked(True)
        self.actionKey_Practice.setObjectName("actionKey_Practice")
        self.actionTyping_Practice = QtWidgets.QAction(MainWindow)
        self.actionTyping_Practice.setCheckable(True)
        self.actionTyping_Practice.setObjectName("actionTyping_Practice")
        self.menuMode.addAction(self.actionKey_Practice)
        self.menuMode.addAction(self.actionTyping_Practice)
        self.menubar.addAction(self.menuMode.menuAction())

        self.retranslateUi(MainWindow)
        self.actionKey_Practice.toggled['bool'].connect(MainWindow.actionModeKey) # type: ignore
        self.actionTyping_Practice.toggled['bool'].connect(MainWindow.actionModeTyping) # type: ignore
        self.lineEdit.textChanged['QString'].connect(MainWindow.lineEditTextChanged) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mapping Trainer"))
        self.label_keysPerSecond.setText(_translate("MainWindow", "--"))
        self.label_keyPrompt.setText(_translate("MainWindow", "KEY TO TYPE"))
        self.menuMode.setTitle(_translate("MainWindow", "Mode"))
        self.actionKey_Practice.setText(_translate("MainWindow", "Key Practice"))
        self.actionTyping_Practice.setText(_translate("MainWindow", "Typing Practice"))