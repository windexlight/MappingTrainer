# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QVBoxLayout, QWidget)

from visibleWhitespaceTextEdit import VisibleWhitespaceTextEdit

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(527, 345)
        self.actionKey_Practice = QAction(MainWindow)
        self.actionKey_Practice.setObjectName(u"actionKey_Practice")
        self.actionKey_Practice.setCheckable(True)
        self.actionKey_Practice.setChecked(True)
        self.actionTyping_Practice = QAction(MainWindow)
        self.actionTyping_Practice.setObjectName(u"actionTyping_Practice")
        self.actionTyping_Practice.setCheckable(True)
        self.actionLoad_typing_content_file = QAction(MainWindow)
        self.actionLoad_typing_content_file.setObjectName(u"actionLoad_typing_content_file")
        self.actionNumbers = QAction(MainWindow)
        self.actionNumbers.setObjectName(u"actionNumbers")
        self.actionNumbers.setCheckable(True)
        self.actionNumbers.setChecked(True)
        self.actionSymbols = QAction(MainWindow)
        self.actionSymbols.setObjectName(u"actionSymbols")
        self.actionSymbols.setCheckable(True)
        self.actionSymbols.setChecked(True)
        self.actionSpecials = QAction(MainWindow)
        self.actionSpecials.setObjectName(u"actionSpecials")
        self.actionSpecials.setCheckable(True)
        self.actionSpecials.setChecked(True)
        self.actionLowercase = QAction(MainWindow)
        self.actionLowercase.setObjectName(u"actionLowercase")
        self.actionLowercase.setCheckable(True)
        self.actionLowercase.setChecked(True)
        self.actionUppercase = QAction(MainWindow)
        self.actionUppercase.setObjectName(u"actionUppercase")
        self.actionUppercase.setCheckable(True)
        self.actionUppercase.setChecked(True)
        self.actionModifiers = QAction(MainWindow)
        self.actionModifiers.setObjectName(u"actionModifiers")
        self.actionModifiers.setCheckable(True)
        self.actionModifiers.setChecked(True)
        self.actionFunction = QAction(MainWindow)
        self.actionFunction.setObjectName(u"actionFunction")
        self.actionFunction.setCheckable(True)
        self.actionFunction.setChecked(True)
        self.actionCombos = QAction(MainWindow)
        self.actionCombos.setObjectName(u"actionCombos")
        self.actionCombos.setCheckable(True)
        self.actionCombos.setChecked(True)
        self.actionWords_Top_10 = QAction(MainWindow)
        self.actionWords_Top_10.setObjectName(u"actionWords_Top_10")
        self.actionWords_Top_10.setCheckable(True)
        self.actionWords_Top_100 = QAction(MainWindow)
        self.actionWords_Top_100.setObjectName(u"actionWords_Top_100")
        self.actionWords_Top_100.setCheckable(True)
        self.actionWords_Top_1000 = QAction(MainWindow)
        self.actionWords_Top_1000.setObjectName(u"actionWords_Top_1000")
        self.actionWords_Top_1000.setCheckable(True)
        self.actionWords_All = QAction(MainWindow)
        self.actionWords_All.setObjectName(u"actionWords_All")
        self.actionWords_All.setCheckable(True)
        self.actionSerif_Font = QAction(MainWindow)
        self.actionSerif_Font.setObjectName(u"actionSerif_Font")
        self.actionSerif_Font.setCheckable(True)
        self.actionSerif_Font.setChecked(True)
        self.actionAdvance_On_Enter = QAction(MainWindow)
        self.actionAdvance_On_Enter.setObjectName(u"actionAdvance_On_Enter")
        self.actionAdvance_On_Enter.setCheckable(True)
        self.actionAdvance_On_Space = QAction(MainWindow)
        self.actionAdvance_On_Space.setObjectName(u"actionAdvance_On_Space")
        self.actionAdvance_On_Space.setCheckable(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(12)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pushButton_Minus = QPushButton(self.centralwidget)
        self.pushButton_Minus.setObjectName(u"pushButton_Minus")
        self.pushButton_Minus.setMaximumSize(QSize(30, 16777215))
        self.pushButton_Minus.setStyleSheet(u"\n"
"          QPushButton {\n"
"            border-radius: 5px;\n"
"            background-color: #eee;\n"
"            padding: 5px;\n"
"            font-weight: 500;\n"
"          }\n"
"          QPushButton:hover {\n"
"            background-color: #ddd;\n"
"          }\n"
"         ")
        self.pushButton_Minus.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_Minus)

        self.pushButton_Plus = QPushButton(self.centralwidget)
        self.pushButton_Plus.setObjectName(u"pushButton_Plus")
        self.pushButton_Plus.setMaximumSize(QSize(30, 16777215))
        self.pushButton_Plus.setStyleSheet(u"\n"
"          QPushButton {\n"
"            border-radius: 5px;\n"
"            background-color: #eee;\n"
"            padding: 5px;\n"
"            font-weight: 500;\n"
"          }\n"
"          QPushButton:hover {\n"
"            background-color: #ddd;\n"
"          }\n"
"         ")
        self.pushButton_Plus.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_Plus)

        self.label_keysPerSecond = QLabel(self.centralwidget)
        self.label_keysPerSecond.setObjectName(u"label_keysPerSecond")
        self.label_keysPerSecond.setMaximumSize(QSize(16777215, 16))
        font = QFont()
        font.setFamilies([u"Cascadia Code"])
        font.setPointSize(10)
        font.setBold(False)
        self.label_keysPerSecond.setFont(font)
        self.label_keysPerSecond.setStyleSheet(u"color: #444; background: transparent;")
        self.label_keysPerSecond.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_keysPerSecond)

        self.label_line = QLabel(self.centralwidget)
        self.label_line.setObjectName(u"label_line")
        self.label_line.setMaximumSize(QSize(135, 16777214))
        self.label_line.setFont(font)
        self.label_line.setStyleSheet(u"color: #444; background: transparent;")
        self.label_line.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.label_line)

        self.pushButton_Back = QPushButton(self.centralwidget)
        self.pushButton_Back.setObjectName(u"pushButton_Back")
        self.pushButton_Back.setMaximumSize(QSize(30, 16777215))
        self.pushButton_Back.setStyleSheet(u"\n"
"          QPushButton {\n"
"            border-radius: 5px;\n"
"            background-color: #eee;\n"
"            padding: 5px;\n"
"            font-weight: 500;\n"
"          }\n"
"          QPushButton:hover {\n"
"            background-color: #ddd;\n"
"          }\n"
"         ")
        self.pushButton_Back.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_Back)

        self.pushButton_Next = QPushButton(self.centralwidget)
        self.pushButton_Next.setObjectName(u"pushButton_Next")
        self.pushButton_Next.setMaximumSize(QSize(30, 16777215))
        self.pushButton_Next.setStyleSheet(u"\n"
"          QPushButton {\n"
"            border-radius: 5px;\n"
"            background-color: #eee;\n"
"            padding: 5px;\n"
"            font-weight: 500;\n"
"          }\n"
"          QPushButton:hover {\n"
"            background-color: #ddd;\n"
"          }\n"
"         ")
        self.pushButton_Next.setFlat(True)

        self.horizontalLayout_2.addWidget(self.pushButton_Next)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_keysPressed = QLabel(self.centralwidget)
        self.label_keysPressed.setObjectName(u"label_keysPressed")
        self.label_keysPressed.setStyleSheet(u"\n"
"          background-color: #f9fbff;\n"
"          border: 1px solid #ccc;\n"
"          border-radius: 8px;\n"
"          padding: 6px;\n"
"          color: #222;\n"
"         ")
        self.label_keysPressed.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_keysPressed)

        self.lineEdit = VisibleWhitespaceTextEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setStyleSheet(u"\n"
"          QPlainTextEdit {\n"
"            background-color: #f9fbff;\n"
"            border: 1px solid #ccc;\n"
"            border-radius: 8px;\n"
"            padding: 8px;\n"
"            color: #222;\n"
"            font-weight: normal;\n"
"            padding: 0.5px;\n"
"            text-align: left;\n"
"          }\n"
"         ")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.textedit_keyPrompt = VisibleWhitespaceTextEdit(self.centralwidget)
        self.textedit_keyPrompt.setObjectName(u"textedit_keyPrompt")
        self.textedit_keyPrompt.setStyleSheet(u"\n"
"        QPlainTextEdit {\n"
"          background-color: #f9fbff;\n"
"          border: 1px solid #ccc;\n"
"          border-radius: 8px;\n"
"          padding: 8px;\n"
"          color: #222;\n"
"          padding: 0.5px;\n"
"          text-align: left;\n"
"        }\n"
"\n"
"        /* Vertical scrollbar */\n"
"        QScrollBar:vertical {\n"
"          border: none;\n"
"          background: #f0f2f5;\n"
"          width: 12px;\n"
"          margin: 2px 0 2px 0;\n"
"          border-radius: 6px;\n"
"        }\n"
"        QScrollBar::handle:vertical {\n"
"          background: #bbb;\n"
"          min-height: 20px;\n"
"          border-radius: 6px;\n"
"        }\n"
"        QScrollBar::handle:vertical:hover {\n"
"          background: #999;\n"
"        }\n"
"        QScrollBar::add-line:vertical,\n"
"        QScrollBar::sub-line:vertical {\n"
"          border: none;\n"
"          background: none;\n"
"          height: 0;\n"
"        }\n"
"\n"
"        /* Horizontal scrollbar */\n"
"        QScrollBar:h"
                        "orizontal {\n"
"          border: none;\n"
"          background: #f0f2f5;\n"
"          height: 12px;\n"
"          margin: 0 2px 0 2px;\n"
"          border-radius: 6px;\n"
"        }\n"
"        QScrollBar::handle:horizontal {\n"
"          background: #bbb;\n"
"          min-width: 20px;\n"
"          border-radius: 6px;\n"
"        }\n"
"        QScrollBar::handle:horizontal:hover {\n"
"          background: #999;\n"
"        }\n"
"        QScrollBar::add-line:horizontal,\n"
"        QScrollBar::sub-line:horizontal {\n"
"          border: none;\n"
"          background: none;\n"
"          width: 0;\n"
"        }\n"
"      ")
        self.textedit_keyPrompt.setReadOnly(True)

        self.verticalLayout.addWidget(self.textedit_keyPrompt)

        self.label_keyPrompt = QLabel(self.centralwidget)
        self.label_keyPrompt.setObjectName(u"label_keyPrompt")
        self.label_keyPrompt.setStyleSheet(u"\n"
"        background-color: #f9fbff;\n"
"        border: 1px solid #ccc;\n"
"        border-radius: 8px;\n"
"        padding: 8px;\n"
"        color: #222;\n"
"      ")
        self.label_keyPrompt.setAlignment(Qt.AlignCenter)
        self.label_keyPrompt.setWordWrap(True)

        self.verticalLayout.addWidget(self.label_keyPrompt)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 527, 35))
        self.menubar.setStyleSheet(u"\n"
"        QMenuBar {\n"
"            background-color: #f4f4f4;\n"
"            spacing: 6px;\n"
"            padding: 2px;\n"
"            color: black; /* normal text color */\n"
"        }\n"
"        QMenuBar::item {\n"
"            spacing: 4px;\n"
"            padding: 5px 12px;\n"
"            background: transparent;\n"
"            font-weight: 500;\n"
"            color: black; /* force text visible */\n"
"        }\n"
"        QMenuBar::item:hover {\n"
"            background-color: #ddd;\n"
"            border-radius: 4px;\n"
"            color: black; /* ensure text visible */\n"
"        }\n"
"        QMenuBar::item:pressed {\n"
"            background-color: #ccc;\n"
"            border-radius: 4px;\n"
"            color: black;\n"
"        }\n"
"        QMenu {\n"
"            background-color: #f9f9f9;\n"
"            border: 1px solid #ccc;\n"
"            padding: 6px;\n"
"            color: black; /* menu item text color */\n"
"        }\n"
"        QMenu::item:selected {\n"
"           "
                        " background-color: #ddd;\n"
"            border-radius: 4px;\n"
"            color: black;\n"
"        }\n"
"    ")
        self.menuMode = QMenu(self.menubar)
        self.menuMode.setObjectName(u"menuMode")
        self.menuOptions = QMenu(self.menubar)
        self.menuOptions.setObjectName(u"menuOptions")
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuMode.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menuMode.addAction(self.actionKey_Practice)
        self.menuMode.addAction(self.actionTyping_Practice)
        self.menuMode.addAction(self.actionWords_Top_10)
        self.menuMode.addAction(self.actionWords_Top_100)
        self.menuMode.addAction(self.actionWords_Top_1000)
        self.menuMode.addAction(self.actionWords_All)
        self.menuOptions.addAction(self.actionSerif_Font)
        self.menuOptions.addAction(self.actionAdvance_On_Enter)
        self.menuOptions.addAction(self.actionAdvance_On_Space)
        self.menuOptions.addAction(self.actionNumbers)
        self.menuOptions.addAction(self.actionSymbols)
        self.menuOptions.addAction(self.actionSpecials)
        self.menuOptions.addAction(self.actionModifiers)
        self.menuOptions.addAction(self.actionLowercase)
        self.menuOptions.addAction(self.actionUppercase)
        self.menuOptions.addAction(self.actionFunction)
        self.menuOptions.addAction(self.actionCombos)
        self.menuFile.addAction(self.actionLoad_typing_content_file)

        self.retranslateUi(MainWindow)
        self.actionKey_Practice.toggled.connect(MainWindow.actionModeKey)
        self.actionTyping_Practice.toggled.connect(MainWindow.actionModeTyping)
        self.lineEdit.textChanged.connect(MainWindow.lineEditTextChanged)
        self.actionLoad_typing_content_file.triggered.connect(MainWindow.loadTypingPromptFile)
        self.actionCombos.toggled.connect(MainWindow.keyTypeToggled)
        self.actionFunction.toggled.connect(MainWindow.keyTypeToggled)
        self.actionLowercase.toggled.connect(MainWindow.keyTypeToggled)
        self.actionModifiers.toggled.connect(MainWindow.keyTypeToggled)
        self.actionNumbers.toggled.connect(MainWindow.keyTypeToggled)
        self.actionSpecials.toggled.connect(MainWindow.keyTypeToggled)
        self.actionSymbols.toggled.connect(MainWindow.keyTypeToggled)
        self.actionUppercase.toggled.connect(MainWindow.keyTypeToggled)
        self.actionWords_Top_10.toggled.connect(MainWindow.actionModeTyping)
        self.actionWords_Top_100.toggled.connect(MainWindow.actionModeTyping)
        self.actionWords_Top_1000.toggled.connect(MainWindow.actionModeTyping)
        self.actionWords_All.toggled.connect(MainWindow.actionModeTyping)
        self.pushButton_Next.clicked.connect(MainWindow.nextButton)
        self.pushButton_Back.clicked.connect(MainWindow.backButton)
        self.actionSerif_Font.toggled.connect(MainWindow.actionSerifFont)
        self.pushButton_Plus.clicked.connect(MainWindow.plusButton)
        self.pushButton_Minus.clicked.connect(MainWindow.minusButton)
        self.actionAdvance_On_Enter.toggled.connect(MainWindow.actionAdvanceOnEnter)
        self.actionAdvance_On_Space.toggled.connect(MainWindow.actionAdvanceOnSpace)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Mapping Trainer", None))
        self.actionKey_Practice.setText(QCoreApplication.translate("MainWindow", u"Keys", None))
        self.actionTyping_Practice.setText(QCoreApplication.translate("MainWindow", u"Typing", None))
        self.actionLoad_typing_content_file.setText(QCoreApplication.translate("MainWindow", u"Load typing content file...", None))
        self.actionNumbers.setText(QCoreApplication.translate("MainWindow", u"Numbers", None))
        self.actionSymbols.setText(QCoreApplication.translate("MainWindow", u"Symbols", None))
        self.actionSpecials.setText(QCoreApplication.translate("MainWindow", u"Specials", None))
        self.actionLowercase.setText(QCoreApplication.translate("MainWindow", u"Lowercase", None))
        self.actionUppercase.setText(QCoreApplication.translate("MainWindow", u"Uppercase", None))
        self.actionModifiers.setText(QCoreApplication.translate("MainWindow", u"Modifiers", None))
        self.actionFunction.setText(QCoreApplication.translate("MainWindow", u"Function", None))
        self.actionCombos.setText(QCoreApplication.translate("MainWindow", u"Combos", None))
        self.actionWords_Top_10.setText(QCoreApplication.translate("MainWindow", u"Words (Top 10)", None))
        self.actionWords_Top_100.setText(QCoreApplication.translate("MainWindow", u"Words (Top 100)", None))
        self.actionWords_Top_1000.setText(QCoreApplication.translate("MainWindow", u"Words (Top 1000)", None))
        self.actionWords_All.setText(QCoreApplication.translate("MainWindow", u"Words (All)", None))
        self.actionSerif_Font.setText(QCoreApplication.translate("MainWindow", u"Serif Font", None))
        self.actionAdvance_On_Enter.setText(QCoreApplication.translate("MainWindow", u"Advance On Enter", None))
        self.actionAdvance_On_Space.setText(QCoreApplication.translate("MainWindow", u"Advance On Space", None))
        self.pushButton_Minus.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_Plus.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.label_keysPerSecond.setText(QCoreApplication.translate("MainWindow", u"--", None))
        self.label_line.setText(QCoreApplication.translate("MainWindow", u"99999 / 99999", None))
        self.pushButton_Back.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.pushButton_Next.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.label_keyPrompt.setText(QCoreApplication.translate("MainWindow", u"KEY TO TYPE", None))
        self.menuMode.setTitle(QCoreApplication.translate("MainWindow", u"Mode", None))
        self.menuOptions.setTitle(QCoreApplication.translate("MainWindow", u"Options", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

