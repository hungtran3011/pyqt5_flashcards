# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/add_deck.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui__add_deck(object):
    def setupUi(self, _add_deck):
        _add_deck.setObjectName("_add_deck")
        _add_deck.resize(671, 128)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(_add_deck.sizePolicy().hasHeightForWidth())
        _add_deck.setSizePolicy(sizePolicy)
        _add_deck.setMaximumSize(QtCore.QSize(16777215, 210))
        _add_deck.setStyleSheet("QDialog#_add_deck{\n"
"    background-color: white;\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(_add_deck)
        self.verticalLayout.setObjectName("verticalLayout")
        self._new_deck_frame = QtWidgets.QFrame(_add_deck)
        self._new_deck_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._new_deck_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._new_deck_frame.setObjectName("_new_deck_frame")
        self.formLayout = QtWidgets.QFormLayout(self._new_deck_frame)
        self.formLayout.setObjectName("formLayout")
        self._new_deck_label = QtWidgets.QLabel(self._new_deck_frame)
        self._new_deck_label.setObjectName("_new_deck_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._new_deck_label)
        self._new_deck_box = QtWidgets.QLineEdit(self._new_deck_frame)
        self._new_deck_box.setStyleSheet("height: 20px;\n"
"border-radius: 10px;\n"
"background-color: rgb(222, 222, 222);\n"
"padding: 5px;")
        self._new_deck_box.setObjectName("_new_deck_box")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self._new_deck_box)
        self.verticalLayout.addWidget(self._new_deck_frame)
        self._button_frame = QtWidgets.QFrame(_add_deck)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._button_frame.sizePolicy().hasHeightForWidth())
        self._button_frame.setSizePolicy(sizePolicy)
        self._button_frame.setStyleSheet("QPushButton{\n"
"    border: 0px;\n"
"    background: #d3d3d3;\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    margin-right: 10px;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background: #a1a1a1;\n"
"    color:white;\n"
"}")
        self._button_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._button_frame.setObjectName("_button_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self._button_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self._save_button = QtWidgets.QPushButton(self._button_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._save_button.sizePolicy().hasHeightForWidth())
        self._save_button.setSizePolicy(sizePolicy)
        self._save_button.setStyleSheet("QPushButton{\n"
"    background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #77bd65, stop: 1 #91e67b );\n"
"    color: white;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #81cc6e;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 1 #77bd65, stop: 0 #91e67b );\n"
"}")
        self._save_button.setObjectName("_save_button")
        self.horizontalLayout.addWidget(self._save_button)
        self._cancel_button = QtWidgets.QPushButton(self._button_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._cancel_button.sizePolicy().hasHeightForWidth())
        self._cancel_button.setSizePolicy(sizePolicy)
        self._cancel_button.setObjectName("_cancel_button")
        self.horizontalLayout.addWidget(self._cancel_button)
        self.verticalLayout.addWidget(self._button_frame)
        self._message = QtWidgets.QLabel(_add_deck)
        self._message.setText("")
        self._message.setObjectName("_message")
        self.verticalLayout.addWidget(self._message)

        self.retranslateUi(_add_deck)
        QtCore.QMetaObject.connectSlotsByName(_add_deck)

    def retranslateUi(self, _add_deck):
        _translate = QtCore.QCoreApplication.translate
        _add_deck.setWindowTitle(_translate("_add_deck", "Add deck"))
        self._new_deck_label.setText(_translate("_add_deck", "New deck name"))
        self._save_button.setText(_translate("_add_deck", "Save"))
        self._cancel_button.setText(_translate("_add_deck", "Cancel"))
