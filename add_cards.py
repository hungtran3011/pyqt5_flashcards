import os
import sys
from pathlib import Path
from platform import system
from datetime import date
import shutil

from PyQt5 import QtCore, QtGui, QtWidgets

import io_
from ui_package.ui_add_card import Ui_add_card

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
SYSTEM = system()
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"
ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")

class AddCards(QtWidgets.QDialog, Ui_add_card):
    def __init__(self, parent, deck):
        super().__init__(parent)
        self.deck = deck
        self.setupUi(self)
        self.setWindowTitle(f"Add new card to deck: {self.deck}")
        self.img.setGeometry(self.img.x(), self.img.y(), 300, 400)
        self.save_button_single.clicked.connect(self._saveSingleCard)
        self.choose_image.clicked.connect(self._chooseImage)
        self.cancel_button_single.clicked.connect(self.close)
        self.img_file = ""
        self.exec_()

    def _saveSingleCard(self):
        inp = io_.SQLiteInput(self.deck)
        index = len(inp.fetchDataFromDBDeck()) + 1
        out = io_.SQLiteOutput(self.deck)
        front = self.front_box.toPlainText()
        back = self.back_box.toPlainText()
        try:
            img_file = os.path.basename(self.img_file)
        except:
            pass
        data_card = (index, front, back, f"{IMG_DIR}/{self.deck}/{img_file}")
        data_date = (index, front, None, date.today())
        out.writeToDB(data_card, "DECK")
        out.writeToDB(data_date, "DATE_")
        if self.img_file != "":
            shutil.copyfile(self.img_file, f"{IMG_DIR}/{self.deck}/{img_file}")
        else:
            pass
        self.close()

    def _chooseImage(self):
        default_dir = f'{os.path.expanduser("~")}/Pictures'
        print(default_dir)
        self.img_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Image", default_dir)
        pixmap = QtGui.QPixmap(self.img_file)
        self.img.setPixmap(pixmap.scaledToHeight(200))