from PyQt5 import QtWidgets
# from core.ui_package.


class Settings(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        vertical_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(vertical_layout)
        info = QtWidgets.QLabel("Sorry, this section is in development", self)
        vertical_layout.addWidget(info)
        