# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/game_mode.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_game_mode(object):
    def setupUi(self, game_mode):
        game_mode.setObjectName("game_mode")
        game_mode.resize(853, 541)
        game_mode.setStyleSheet("QWidget{\n"
"    background: white;\n"
"}")
        self.gridLayout = QtWidgets.QGridLayout(game_mode)
        self.gridLayout.setObjectName("gridLayout")
        self.score_frame = QtWidgets.QFrame(game_mode)
        self.score_frame.setMinimumSize(QtCore.QSize(200, 0))
        self.score_frame.setMaximumSize(QtCore.QSize(250, 16777215))
        self.score_frame.setStyleSheet("border-radius: 5px")
        self.score_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.score_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.score_frame.setObjectName("score_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.score_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.score_label = QtWidgets.QLabel(self.score_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.score_label.sizePolicy().hasHeightForWidth())
        self.score_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.score_label.setFont(font)
        self.score_label.setAlignment(QtCore.Qt.AlignCenter)
        self.score_label.setObjectName("score_label")
        self.verticalLayout.addWidget(self.score_label)
        self.score = QtWidgets.QLabel(self.score_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.score.sizePolicy().hasHeightForWidth())
        self.score.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.score.setFont(font)
        self.score.setStyleSheet("margin-bottom: 30px;\n"
"margin-top: 30px;\n"
"color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #77bd65, stop: 1 #91e67b );")
        self.score.setAlignment(QtCore.Qt.AlignCenter)
        self.score.setObjectName("score")
        self.verticalLayout.addWidget(self.score)
        self.revise_label = QtWidgets.QLabel(self.score_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.revise_label.sizePolicy().hasHeightForWidth())
        self.revise_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.revise_label.setFont(font)
        self.revise_label.setObjectName("revise_label")
        self.verticalLayout.addWidget(self.revise_label)
        self.revised_frame = QtWidgets.QScrollArea(self.score_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.revised_frame.sizePolicy().hasHeightForWidth())
        self.revised_frame.setSizePolicy(sizePolicy)
        self.revised_frame.setStyleSheet("QWidget{\n"
"    background: white;\n"
"}\n"
"QScrollBar:vertical {\n"
"    border: 0;\n"
"    width: 6px;\n"
"    border-radius: 3px;\n"
"    background: #d3d3d3;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical {\n"
"    border: 0;\n"
"    border-radius: 3px;\n"
"    background: rgb(161, 161, 161);\n"
"}\n"
"QScrollBar::handle:vertical:hover {\n"
"    background-color: rgb(143, 143, 143);\n"
"}\n"
"QScrollBar::handle:vertical:pressed{\n"
"    background-color: rgb(120, 120, 120);\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"    height: 0px;\n"
"}\n"
"QScrollBar:horizontal {\n"
"    border: 0;\n"
"    height: 6px;\n"
"    border-radius: 3px;\n"
"    background: #d3d3d3;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    border: 0;\n"
"    border-radius: 3px;\n"
"    background: rgb(161, 161, 161);\n"
"}\n"
"QScrollBar::handle:horizontal:hover {\n"
"    background-color: rgb(143, 143, 143);\n"
"}\n"
"QScrollBar::handle:horizontal:pressed{\n"
"    background-color: rgb(120, 120, 120);\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    width: 0px;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    width: 0px;\n"
"}")
        self.revised_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.revised_frame.setWidgetResizable(True)
        self.revised_frame.setObjectName("revised_frame")
        self.revised_widget = QtWidgets.QWidget()
        self.revised_widget.setGeometry(QtCore.QRect(0, 0, 188, 343))
        self.revised_widget.setObjectName("revised_widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.revised_widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.revised_frame.setWidget(self.revised_widget)
        self.verticalLayout.addWidget(self.revised_frame)
        self.gridLayout.addWidget(self.score_frame, 0, 2, 5, 1)
        self.header_frame = QtWidgets.QFrame(game_mode)
        self.header_frame.setStyleSheet("border-radius: 5px;")
        self.header_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.header_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.back_button = QtWidgets.QPushButton(self.header_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.back_button.sizePolicy().hasHeightForWidth())
        self.back_button.setSizePolicy(sizePolicy)
        self.back_button.setStyleSheet("QPushButton{\n"
"    border: 2px solid #91e67b;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;    \n"
"    background:white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #91e67b;\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: #7fc86b;\n"
"    border-color: #7fc86b;\n"
"    color: white;\n"
"}")
        self.back_button.setObjectName("back_button")
        self.horizontalLayout_2.addWidget(self.back_button)
        self.game_progress = QtWidgets.QProgressBar(self.header_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_progress.sizePolicy().hasHeightForWidth())
        self.game_progress.setSizePolicy(sizePolicy)
        self.game_progress.setMinimumSize(QtCore.QSize(0, 0))
        self.game_progress.setMaximumSize(QtCore.QSize(16777215, 10))
        self.game_progress.setStyleSheet("QProgressBar{\n"
"    border: 0px;\n"
"    border-radius: 5px;\n"
"    background-color: rgb(227, 227, 227);\n"
"}\n"
"\n"
"QProgressBar::chunk{\n"
"    border: 0px;\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #77bd65, stop: 1 #91e67b );\n"
"  border-radius: 5px;\n"
"}")
        self.game_progress.setProperty("value", 24)
        self.game_progress.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.game_progress.setTextVisible(False)
        self.game_progress.setOrientation(QtCore.Qt.Horizontal)
        self.game_progress.setInvertedAppearance(False)
        self.game_progress.setFormat("")
        self.game_progress.setObjectName("game_progress")
        self.horizontalLayout_2.addWidget(self.game_progress)
        self.gridLayout.addWidget(self.header_frame, 0, 1, 1, 1)
        self.game_frame = QtWidgets.QFrame(game_mode)
        self.game_frame.setStyleSheet("border-radius: 5px;")
        self.game_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.game_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.game_frame.setObjectName("game_frame")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.game_frame)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.question_type_label = QtWidgets.QLabel(self.game_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.question_type_label.sizePolicy().hasHeightForWidth())
        self.question_type_label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.question_type_label.setFont(font)
        self.question_type_label.setStyleSheet("color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #77bd65, stop: 1 #91e67b );")
        self.question_type_label.setAlignment(QtCore.Qt.AlignCenter)
        self.question_type_label.setObjectName("question_type_label")
        self.verticalLayout_5.addWidget(self.question_type_label)
        self.question_frame = QtWidgets.QFrame(self.game_frame)
        self.question_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.question_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.question_frame.setObjectName("question_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.question_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.question_img = QtWidgets.QLabel(self.question_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.question_img.sizePolicy().hasHeightForWidth())
        self.question_img.setSizePolicy(sizePolicy)
        self.question_img.setMaximumSize(QtCore.QSize(200, 100))
        self.question_img.setText("")
        self.question_img.setPixmap(QtGui.QPixmap("ui/../../../Downloads/dien-bien-bat-ngo-khi-ta-ga-trong-f5f141.jpg"))
        self.question_img.setScaledContents(True)
        self.question_img.setObjectName("question_img")
        self.horizontalLayout.addWidget(self.question_img)
        self.question_label = QtWidgets.QLabel(self.question_frame)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.question_label.setFont(font)
        self.question_label.setWordWrap(True)
        self.question_label.setOpenExternalLinks(False)
        self.question_label.setObjectName("question_label")
        self.horizontalLayout.addWidget(self.question_label)
        self.next_question_button = QtWidgets.QPushButton(self.question_frame)
        self.next_question_button.setEnabled(False)
        self.next_question_button.setMaximumSize(QtCore.QSize(150, 16777215))
        self.next_question_button.setStyleSheet("QPushButton{\n"
"    background: #d3d3d3;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background: rgb(157, 157, 157);\n"
"    color: white;\n"
"}")
        self.next_question_button.setObjectName("next_question_button")
        self.horizontalLayout.addWidget(self.next_question_button)
        self.verticalLayout_5.addWidget(self.question_frame)
        self.question_widget = QtWidgets.QStackedWidget(self.game_frame)
        self.question_widget.setStyleSheet("QPushButton{\n"
"    background: #d3d3d3;\n"
"    border-radius: 5px;\n"
"    padding: 20px 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background: rgb(157, 157, 157);\n"
"    color: white;\n"
"}")
        self.question_widget.setObjectName("question_widget")
        self.writing_widget = QtWidgets.QWidget()
        self.writing_widget.setObjectName("writing_widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.writing_widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.answer_box = QtWidgets.QTextEdit(self.writing_widget)
        self.answer_box.setStyleSheet("background-color: #d3d3d3;\n"
"padding: 5px;\n"
"border-radius: 5px;")
        self.answer_box.setObjectName("answer_box")
        font = QtGui.QFont()
        font.setPointSize(18)
        self.answer_box.setFont(font)
        self.verticalLayout_2.addWidget(self.answer_box)
        self.submit_frame = QtWidgets.QFrame(self.writing_widget)
        self.submit_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.submit_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.submit_frame.setObjectName("submit_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.submit_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.submit = QtWidgets.QPushButton(self.submit_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.submit.sizePolicy().hasHeightForWidth())
        self.submit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.submit.setFont(font)
        self.submit.setStyleSheet("QPushButton{\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #77bd65, stop: 1 #91e67b );\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #81cc6e;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 1 #77bd65, stop: 0 #91e67b );\n"
"}")
        self.submit.setObjectName("submit")
        self.horizontalLayout_3.addWidget(self.submit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addWidget(self.submit_frame)
        self.question_widget.addWidget(self.writing_widget)
        self.multiple_widget = QtWidgets.QWidget()
        self.multiple_widget.setObjectName("multiple_widget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.multiple_widget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.answer_frame = QtWidgets.QFrame(self.multiple_widget)
        self.answer_frame.setStyleSheet("QPushButton{\n"
"    background: #d3d3d3;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background: rgb(157, 157, 157);\n"
"    color: white;\n"
"}")
        self.answer_frame.setObjectName("answer_frame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.answer_frame)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.button_D = QtWidgets.QPushButton(self.answer_frame)
        self.button_D.setObjectName("button_D")
        self.gridLayout_2.addWidget(self.button_D, 1, 1, 1, 1)
        self.button_A = QtWidgets.QPushButton(self.answer_frame)
        self.button_A.setCheckable(False)
        self.button_A.setAutoDefault(False)
        self.button_A.setDefault(False)
        self.button_A.setFlat(False)
        self.button_A.setObjectName("button_A")
        self.gridLayout_2.addWidget(self.button_A, 0, 0, 1, 1)
        self.button_B = QtWidgets.QPushButton(self.answer_frame)
        self.button_B.setObjectName("button_B")
        self.gridLayout_2.addWidget(self.button_B, 0, 1, 1, 1)
        self.button_C = QtWidgets.QPushButton(self.answer_frame)
        self.button_C.setObjectName("button_C")
        self.gridLayout_2.addWidget(self.button_C, 1, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.answer_frame)
        self.question_widget.addWidget(self.multiple_widget)
        self.verticalLayout_5.addWidget(self.question_widget)
        self.true_answer_label = QtWidgets.QLabel(self.game_frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.true_answer_label.setFont(font)
        self.true_answer_label.setStyleSheet("color: #91e67b")
        self.true_answer_label.setAlignment(QtCore.Qt.AlignCenter)
        self.true_answer_label.setObjectName("true_answer_label")
        self.verticalLayout_5.addWidget(self.true_answer_label)
        self.gridLayout.addWidget(self.game_frame, 1, 1, 1, 1)

        self.retranslateUi(game_mode)
        self.question_widget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(game_mode)

    def retranslateUi(self, game_mode):
        _translate = QtCore.QCoreApplication.translate
        game_mode.setWindowTitle(_translate("game_mode", "Game mode for deck: "))
        self.score_label.setText(_translate("game_mode", "Your score:"))
        self.score.setText(_translate("game_mode", "0"))
        self.revise_label.setText(_translate("game_mode", "Revised"))
        self.back_button.setText(_translate("game_mode", "Back"))
        self.question_type_label.setText(_translate("game_mode", "Type the right answer"))
        self.question_label.setText(_translate("game_mode", "Question"))
        self.next_question_button.setText(_translate("game_mode", "Next question"))
        self.submit.setText(_translate("game_mode", "Submit"))
        self.button_D.setText(_translate("game_mode", "D. PushButton"))
        self.button_A.setText(_translate("game_mode", "A. PushButton"))
        self.button_B.setText(_translate("game_mode", "B. PushButton"))
        self.button_C.setText(_translate("game_mode", "C. PushButton"))
        self.true_answer_label.setText(_translate("game_mode", "TextLabel"))
