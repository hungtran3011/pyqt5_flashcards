import os
import sys
from pathlib import Path
from platform import system
from datetime import date
import shutil
import sqlite3 as sql

from PyQt5 import QtCore, QtGui, QtWidgets

import core.io_ as io_
from core.ui_package.ui_add_card import Ui_add_card

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
SYSTEM = system()
IMG_DIR = ROOT_DIR / "../img"
DECKS_DIR = ROOT_DIR / "../decks"
if not (os.path.isdir(str(IMG_DIR)) and os.path.isdir(str(DECKS_DIR))):
    IMG_DIR = ROOT_DIR / "img"
    DECKS_DIR = ROOT_DIR / "decks"

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
        inp = io_.SQLiteImporter(self.deck)
        index = len(inp.fetch_from_db_Deck()) + 1
        out = io_.SQLiteExporter(self.deck)
        front: str = self.front_box.toPlainText()
        back: str = self.back_box.toPlainText()
        if not (front.isspace() or back.isspace()):
            # try:
            img_file = os.path.basename(self.img_file)
            # except:
            #     pass
            data_card = (index, front, back, f"{IMG_DIR}/{self.deck}/{img_file}")
            data_date = (index, front, None, date.today())
            try:
                out.writeToDB(data_card, "DECK")
                out.writeToDB(data_date, "DATE_")
            except sql.IntegrityError:
                self._sendMessage(f"Card '{front}' is already exist", "Card exist")
            if self.img_file != "":
                shutil.copyfile(self.img_file, f"{IMG_DIR}/{self.deck}/{img_file}")
            else:
                pass
            self.close()
        else:
            self._sendMessage("The front and back of the card must not be empty")

    def _chooseImage(self):
        default_dir = f'{os.path.expanduser("~")}/Pictures'
        print(default_dir)
        self.img_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Image", default_dir)
        pixmap = QtGui.QPixmap(self.img_file)
        self.img.setPixmap(pixmap.scaledToHeight(200))

    def _sendMessage(self, text, title=""):
        message = QtWidgets.QMessageBox(self)
        message.setWindowTitle(title)
        message.setIcon(QtWidgets.QMessageBox.Warning)
        message.setText(text)
        message.exec()