import os
import sys
from pathlib import Path
from platform import system
from datetime import date, datetime
import shutil
import functools

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

import core.io_ as io_
from core.ui_package.ui_browse_deck import Ui__browse_deck
from core.ui_package.ui_deck_info import Ui__deck_info

from core.add_deck import AddDeck
from core.rename_deck import RenameDeck

# from core.settings import Settings

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
SYSTEM = system()
IMG_DIR = ROOT_DIR / "../img"
DECKS_DIR = ROOT_DIR / "../decks"
# To handle exceptions when running executable file
if not (os.path.isdir(str(IMG_DIR)) and os.path.isdir(str(DECKS_DIR))):
    IMG_DIR = ROOT_DIR / "img"
    DECKS_DIR = ROOT_DIR / "decks"
ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")


class BrowseDeck(Ui__browse_deck, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self._add_deck.setCursor(QtCore.Qt.PointingHandCursor)
        self._create_function_menu()
        # self.refresh = self.show_all_decks

    def refresh(self):
        self.show_all_decks()

    def show_all_decks(self):
        decks_list = [i for i in os.listdir(DECKS_DIR) if i.endswith(".db")]
        print(decks_list)
        decks_num = len(decks_list)
        if len(decks_list) > 0:
            print(self._all_decks_area.width())
            columns = self._all_decks_area.width() // 480
            full_rows_num = decks_num // columns
            print(f"columns = {columns}, full_rows_num = {full_rows_num}")
            remainder = decks_num % columns
            for deck in reversed(range(self.getDecksArea().count())):
                tmp_widget = self.getDecksArea().itemAt(deck).widget()
                self.getDecksArea().removeWidget(tmp_widget)
                tmp_widget.setParent(None)
                tmp_widget.deleteLater()

            for row in range(full_rows_num):
                for col in range(columns):
                    index = columns * row + col
                    file_name_without_ext = os.path.splitext(decks_list[index])[0]
                    deck_name = self.DeckInfo(
                        self, f"{file_name_without_ext}")
                    self.getDecksArea().addWidget(deck_name, row, col)
            if remainder != 0:
                new_row = full_rows_num
                for col in range(remainder):
                    index = new_row * columns + col
                    deck_name = self.DeckInfo(
                        self, f"{decks_list[index][0:len(decks_list[index]) - 3]}"
                    )
                    self.getDecksArea().addWidget(deck_name, new_row, col)
            self.set_number_of_decks()
        else:
            self.insert_icon()

    def getDecksArea(self):
        return self.gridLayout

    def set_number_of_decks(self):
        decks_list = [i for i in os.listdir(DECKS_DIR) if i.endswith(".db")]
        decks_num = len(decks_list)
        text = f'{decks_num} deck' if decks_num == 1 else f'{decks_num} decks'
        self._number_of_decks.setText(text)
        return decks_num

    def showAddDeckPopup(self, event=None):
        self._dialog_add_deck = AddDeck(self)

    def keyPressEvent(self, event=QtCore.Qt.Key_F5):
        self.show_all_decks()

    def mousePressEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction("Refresh").triggered.connect(self.show_all_decks)
        menu.popup(self.mapToGlobal(event.pos()))

    def insert_icon(self):
        _add_deck_icon = QtSvg.QSvgWidget(ADD_DECK_ICON, self)
        _add_deck_icon.mousePressEvent = self.showAddDeckPopup
        _add_deck_icon.setToolTip("Add a deck")
        _add_deck_icon.setCursor(QtCore.Qt.PointingHandCursor)
        _add_deck_icon.setMaximumSize(200, 200)
        _add_deck_label = QtWidgets.QLabel("Please add some decks", self)
        _add_deck_label.setAlignment(QtCore.Qt.AlignCenter)
        for deck in reversed(range(self.getDecksArea().count())):
            tmp_widget = self.getDecksArea().itemAt(deck).widget()
            self.getDecksArea().removeWidget(tmp_widget)
            tmp_widget.setParent(None)
            tmp_widget.deleteLater()
        self.set_number_of_decks()
        self.getDecksArea().addWidget(_add_deck_icon, 0, 0)
        self.getDecksArea().addWidget(_add_deck_label, 1, 0)

    class DeckInfo(Ui__deck_info, QtWidgets.QGroupBox):
        def __init__(self, parent, deck):
            super().__init__(parent)
            self.setupUi(self)
            self.deck = deck
            self.setDeckName(self.deck)
            shadow = QtWidgets.QGraphicsDropShadowEffect(
                blurRadius=20, xOffset=0, yOffset=0)
            shadow.setColor(QtGui.QColor(201, 199, 199))
            self.setGraphicsEffect(shadow)
            self._game_mode.setCursor(QtCore.Qt.PointingHandCursor)
            self._view_cards_list.setCursor(QtCore.Qt.PointingHandCursor)
            self._flash_mode.setCursor(QtCore.Qt.PointingHandCursor)
            self._more_funcs.setCursor(QtCore.Qt.PointingHandCursor)
            self._evaluate_num_of_cards()
            self._evaluate_num_of_cards_to_review()
            self.setCursor(QtCore.Qt.PointingHandCursor)
            self.setToolTip("Click the title to view cards list")

        def _evaluate_num_of_cards(self):
            deck_name = self.getDeckName()
            inp = io_.SQLiteImporter(deck_name)
            try:
                number = len(inp.fetch_from_db_Deck())
            except shutil.Error:
                number = 0
            text = f'{number} card' if number == 1 else f'{number} cards'
            self._num_of_cards.setText(text)

        def _evaluate_num_of_cards_to_review(self):
            deck_name = self.getDeckName()
            inp = io_.SQLiteImporter(deck_name)
            dates = inp.fetch_from_db_Date_()
            number = 0
            for rows in dates:
                if datetime.today() >= datetime.strptime(rows[3], "%Y-%m-%d"):
                    number += 1
            text = f'{number} card to review' if number == 1 else f'{number} cards to review'
            self._cards_to_review.setText(text)

        def setDeckName(self, new_name):
            self._deck_name.setText(new_name)
            print("name = ", new_name)
            # self._flash_mode.clicked.connect(lambda: self._showFlashcardsMode(new_name))

        def getDeckName(self):
            return self._deck_name.text()

        def deleteDeck(self):
            # os.chdir(os.path.dirname(__file__))
            try:
                file_name = f"{DECKS_DIR}/{self.getDeckName()}.db"
                os.remove(file_name)
                img_folder_name = f"{IMG_DIR}/{self.getDeckName()}"
                shutil.rmtree(img_folder_name)
            except FileNotFoundError:
                pass
            # finally:
            #     self.close()

        def renameDeck(self):
            self._rename_window = RenameDeck(self, self.deck)
