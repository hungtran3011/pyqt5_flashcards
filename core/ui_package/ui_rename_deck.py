# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/rename_deck.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui__rename_deck(object):
    def setupUi(self, _rename_deck):
        _rename_deck.setObjectName("_rename_deck")
        _rename_deck.resize(490, 110)
        self.verticalLayout = QtWidgets.QVBoxLayout(_rename_deck)
        self.verticalLayout.setObjectName("verticalLayout")
        self._rename_frame = QtWidgets.QFrame(_rename_deck)
        self._rename_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._rename_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._rename_frame.setLineWidth(1)
        self._rename_frame.setObjectName("_rename_frame")
        self.formLayout = QtWidgets.QFormLayout(self._rename_frame)
        self.formLayout.setObjectName("formLayout")
        self._name_label = QtWidgets.QLabel(self._rename_frame)
        self._name_label.setObjectName("_name_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self._name_label)
        self._name_box = QtWidgets.QLineEdit(self._rename_frame)
        self._name_box.setObjectName("_name_box")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self._name_box)
        self.verticalLayout.addWidget(self._rename_frame)
        self._button_frame = QtWidgets.QFrame(_rename_deck)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._button_frame.sizePolicy().hasHeightForWidth())
        self._button_frame.setSizePolicy(sizePolicy)
        self._button_frame.setLayoutDirection(QtCore.Qt.RightToLeft)
        self._button_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self._button_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._button_frame.setObjectName("_button_frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self._button_frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self._cancel = QtWidgets.QPushButton(self._button_frame)
        self._cancel.setObjectName("_cancel")
        self._cancel.setStyleSheet("QPushButton{\n"
"    /*background: #d3d3d3;*/\n"
"    border: 2px solid #91e67b;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #91e67b;\n"
"    color: white;\n"
"}\n"
"")
        self.horizontalLayout.addWidget(self._cancel)
        self._save = QtWidgets.QPushButton(self._button_frame)
        self._save.setObjectName("_save")
        self._save.setStyleSheet("QPushButton{\n"
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
        self.horizontalLayout.addWidget(self._save)
        self.verticalLayout.addWidget(self._button_frame)

        self.retranslateUi(_rename_deck)
        QtCore.QMetaObject.connectSlotsByName(_rename_deck)

    def retranslateUi(self, _rename_deck):
        _translate = QtCore.QCoreApplication.translate
        _rename_deck.setWindowTitle(_translate("_rename_deck", "Rename deck: "))
        self._name_label.setText(_translate("_rename_deck", "New name"))
        self._cancel.setText(_translate("_rename_deck", "Cancel"))
        self._save.setText(_translate("_rename_deck", "Save"))
