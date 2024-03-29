# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/show_cards.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui__show_cards(object):
    def setupUi(self, _show_cards):
        _show_cards.setObjectName("_show_cards")
        _show_cards.resize(710, 585)
        # _show_cards.setStyleSheet("background: white")
        self.verticalLayout = QtWidgets.QVBoxLayout(_show_cards)
        self.verticalLayout.setObjectName("verticalLayout")
        self._back = QtWidgets.QPushButton(_show_cards)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._back.sizePolicy().hasHeightForWidth())
        self._back.setSizePolicy(sizePolicy)
        self._back.setMinimumSize(QtCore.QSize(100, 0))
        self._back.setStyleSheet("QPushButton{\n"
"    background: rgba(45, 197, 66, 200);\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgba(45, 197, 66, 255);\n"
"}\n"
"")
        self._back.setObjectName("_back")
        self.verticalLayout.addWidget(self._back)
        self._card_frame = QtWidgets.QFrame(_show_cards)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._card_frame.sizePolicy().hasHeightForWidth())
        self._card_frame.setSizePolicy(sizePolicy)
        self._card_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._card_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._card_frame.setObjectName("_card_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self._card_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self._previous = QtWidgets.QPushButton(self._card_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._previous.sizePolicy().hasHeightForWidth())
        self._previous.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self._previous.setFont(font)
        self._previous.setStyleSheet("QPushButton{\n"
"    border: 0;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    color: #91e67b\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    color: #77bd65;\n"
"}")
        self._previous.setObjectName("_previous")
        self.horizontalLayout_2.addWidget(self._previous)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self._card_with_img = QtWidgets.QFrame(self._card_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._card_with_img.sizePolicy().hasHeightForWidth())
        self._card_with_img.setSizePolicy(sizePolicy)
        self._card_with_img.setMinimumSize(QtCore.QSize(500, 0))
        self._card_with_img.setMaximumSize(QtCore.QSize(500, 16777215))
        self._card_with_img.setStyleSheet("QFrame{\n"
"    background: white;\n"
"    border-radius: 5px;\n"
"}")
        self._card_with_img.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._card_with_img.setFrameShadow(QtWidgets.QFrame.Raised)
        self._card_with_img.setObjectName("_card_with_img")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self._card_with_img)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self._card = QtWidgets.QLabel(self._card_with_img)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._card.sizePolicy().hasHeightForWidth())
        self._card.setSizePolicy(sizePolicy)
        self._card.setMinimumSize(QtCore.QSize(0, 0))
        self._card.setMaximumSize(QtCore.QSize(16777215, 200))
        font = QtGui.QFont()
        font.setPointSize(20)
        self._card.setFont(font)
        self._card.setStyleSheet("background: white;")
        self._card.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self._card.setObjectName("_card")
        self.verticalLayout_2.addWidget(self._card)
        self._img = QtWidgets.QLabel(self._card_with_img)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._img.sizePolicy().hasHeightForWidth())
        self._img.setSizePolicy(sizePolicy)
        self._img.setMinimumSize(QtCore.QSize(0, 200))
        self._img.setMaximumSize(QtCore.QSize(16777215, 200))
        self._img.setAlignment(QtCore.Qt.AlignCenter)
        self._img.setObjectName("_img")
        self.verticalLayout_2.addWidget(self._img)
        self.horizontalLayout_2.addWidget(self._card_with_img)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self._next = QtWidgets.QPushButton(self._card_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._next.sizePolicy().hasHeightForWidth())
        self._next.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self._next.setFont(font)
        self._next.setStyleSheet("QPushButton{\n"
"    border: 0;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    color: #91e67b\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    color: #77bd65;\n"
"}")
        self._next.setObjectName("_next")
        self.horizontalLayout_2.addWidget(self._next)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.verticalLayout.addWidget(self._card_frame)
        self._num = QtWidgets.QLabel(_show_cards)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._num.sizePolicy().hasHeightForWidth())
        self._num.setSizePolicy(sizePolicy)
        self._num.setAlignment(QtCore.Qt.AlignCenter)
        self._num.setObjectName("_num")
        self.verticalLayout.addWidget(self._num)
        self.frame = QtWidgets.QFrame(_show_cards)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self._flip = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._flip.sizePolicy().hasHeightForWidth())
        self._flip.setSizePolicy(sizePolicy)
        self._flip.setMinimumSize(QtCore.QSize(300, 30))
        self._flip.setMaximumSize(QtCore.QSize(400, 16777215))
        self._flip.setStyleSheet("QPushButton{\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #77bd65, stop: 1 #91e67b );\n"
"    color: white;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #81cc6e;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 1 #77bd65, stop: 0 #91e67b );\n"
"}")
        self._flip.setObjectName("_flip")
        self.horizontalLayout_3.addWidget(self._flip)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout.addWidget(self.frame)
        self._button_frame = QtWidgets.QFrame(_show_cards)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._button_frame.sizePolicy().hasHeightForWidth())
        self._button_frame.setSizePolicy(sizePolicy)
        self._button_frame.setStyleSheet("QPushButton{\n"
"    background-color: rgb(118, 255, 80);\n"
"    color: white;\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(112, 236, 74);\n"
"}")
        self._button_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._button_frame.setObjectName("_button_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self._button_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem6)
        self._shuffle = QtWidgets.QPushButton(self._button_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._shuffle.sizePolicy().hasHeightForWidth())
        self._shuffle.setSizePolicy(sizePolicy)
        self._shuffle.setMinimumSize(QtCore.QSize(161, 0))
        self._shuffle.setStyleSheet("QPushButton{\n"
"    background-color: rgb(118, 255, 80);\n"
"    color: white;\n"
"    padding: 5px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: rgb(112, 236, 74);\n"
"}")
        self._shuffle.setObjectName("_shuffle")
        self.horizontalLayout.addWidget(self._shuffle)
        self._refresh = QtWidgets.QPushButton(self._button_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._refresh.sizePolicy().hasHeightForWidth())
        self._refresh.setSizePolicy(sizePolicy)
        self._refresh.setMinimumSize(QtCore.QSize(161, 0))
        self._refresh.setStyleSheet("")
        self._refresh.setObjectName("_refresh")
        self.horizontalLayout.addWidget(self._refresh)
        self._practice = QtWidgets.QPushButton(self._button_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._practice.sizePolicy().hasHeightForWidth())
        self._practice.setSizePolicy(sizePolicy)
        self._practice.setMinimumSize(QtCore.QSize(161, 30))
        self._practice.setStyleSheet("")
        self._practice.setObjectName("_practice")
        self.horizontalLayout.addWidget(self._practice)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.verticalLayout.addWidget(self._button_frame)

        self.retranslateUi(_show_cards)
        QtCore.QMetaObject.connectSlotsByName(_show_cards)
        _show_cards.setTabOrder(self._back, self._previous)
        _show_cards.setTabOrder(self._previous, self._next)
        _show_cards.setTabOrder(self._next, self._flip)
        _show_cards.setTabOrder(self._flip, self._shuffle)
        _show_cards.setTabOrder(self._shuffle, self._refresh)
        _show_cards.setTabOrder(self._refresh, self._practice)

    def retranslateUi(self, _show_cards):
        _translate = QtCore.QCoreApplication.translate
        _show_cards.setWindowTitle(_translate("_show_cards", "Cards from: "))
        self._back.setText(_translate("_show_cards", "Back"))
        self._previous.setText(_translate("_show_cards", "<"))
        self._card.setText(_translate("_show_cards", "TextLabel"))
        self._img.setText(_translate("_show_cards", "TextLabel"))
        self._next.setText(_translate("_show_cards", ">"))
        self._num.setText(_translate("_show_cards", "0/0"))
        self._flip.setText(_translate("_show_cards", "Flip"))
        self._shuffle.setText(_translate("_show_cards", "Shuffle"))
        self._refresh.setText(_translate("_show_cards", "Refresh"))
        self._practice.setText(_translate("_show_cards", "Practice"))
