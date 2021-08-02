import os

from PyQt5 import QtWidgets
from core.ui_package.ui_export_deck import Ui_export_deck
import core.io_ as io_

class ExportDeck(QtWidgets.QDialog, Ui_export_deck):
    def __init__(self, parent, deck) -> None:
        super().__init__(parent)
        self.deck = deck
        self.setupUi(self)
        self.deck_to_export.setText(f"Deck to export: {self.deck}")
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.close)

    def save(self):
        extension = ""
        if self.csv_button.isChecked():
            extension = ".csv"
        elif self.xml_button.isChecked():
            extension = ".xml"
        elif self.json_button.isChecked():
            extension = ".json"
        else:
            pass
        