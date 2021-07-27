import os
import sys
from pathlib import Path 
from platform import system

from PyQt5 import QtWidgets

from ui_package.ui_rename_deck import Ui__rename_deck

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
SYSTEM = system()
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"
ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")

class RenameDeck(QtWidgets.QDialog, Ui__rename_deck):
    def __init__(self, parent, deck):
        super().__init__(parent)
        self.setupUi(self)
        self.deck = deck
        self.setWindowTitle(f"Rename deck: {self.deck}")
        self._name_box.insert(self.deck)
        self._cancel.clicked.connect(self.close)
        self._save.clicked.connect(self._saveDeckName)
        self.exec_()

    def _saveDeckName(self):
        file_name = f"{ROOT_DIR}/decks/{self.deck}.db"
        new_file_name = f"{ROOT_DIR}/decks/{self._name_box.text()}.db"
        os.rename(file_name, new_file_name)
        os.rename(f"{IMG_DIR}/{self.deck}",
                  f"{IMG_DIR}/{self._name_box.text()}")
        self.close()
        self.parent().setDeckName(self._name_box.text())
        # window.setBrowseDecksMode()