import os
import sys
from pathlib import Path
from platform import system
from datetime import date, datetime
import shutil
import functools

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

import io_
from ui_package.ui_browse_deck import Ui__browse_deck
from ui_package.ui_deck_info import Ui__deck_info

from add_deck import AddDeck
from rename_deck import RenameDeck

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
SYSTEM = system()
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"
ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")

class BrowseDeck(Ui__browse_deck, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self._add_deck.setCursor(QtCore.Qt.PointingHandCursor)
        self._add_deck_icon = QtSvg.QSvgWidget(ADD_DECK_ICON)
        self._add_deck_icon.mousePressEvent = self.showAddDeckPopup
        self._add_deck_icon.setToolTip("Add a deck")
        self._add_deck_icon.setCursor(QtCore.Qt.PointingHandCursor)
        self._add_deck_icon.setMaximumSize(200, 200)
        self._add_deck_label = QtWidgets.QLabel("Please add some decks")
        self._add_deck_label.setAlignment(QtCore.Qt.AlignCenter)
        self._create_function_menu()
        # self.refresh = self.show_all_decks

        

    def refresh(self):
        self.show_all_decks()

    def getDecksArea(self):
        return self.gridLayout

    def setNumberOfDecks(self):
        DECKS_LIST = [i for i in os.listdir(DECKS_DIR) if i.endswith(".db")]
        DECKS_NUM = len(DECKS_LIST)
        text = f'{DECKS_NUM} deck' if DECKS_NUM == 1 else f'{DECKS_NUM} decks'
        self._number_of_decks.setText(text)

    def showAddDeckPopup(self, event=None):
        self._dialog_add_deck = AddDeck(self)

    def _create_function_menu(self):
        function_menu = QtWidgets.QMenu(self._more_funcs)
        settings = function_menu.addAction("Settings...")
        settings.triggered.connect(self.showAddDeckPopup)
        self._more_funcs.setMenu(function_menu)

    def keyPressEvent(self, event=QtCore.Qt.Key_F5):
        self.show_all_decks()

    def mousePressEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction("Refresh").triggered.connect(self.show_all_decks)
        menu.popup(self.mapToGlobal(event.pos()))
            

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
        self._evaluateNumOfCards()
        self._evaluateNumOfCardsToReview()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolTip("Click the title to view cards list")

    def _evaluateNumOfCards(self):
        deck_name = self.getDeckName()
        inp = io_.SQLiteInput(deck_name)
        try:
            number = len(inp.fetchDataFromDBDeck())
        except shutil.Error:
            number = 0
        text = f'{number} card' if number == 1 else f'{number} cards'
        self._num_of_cards.setText(text)

    def _evaluateNumOfCardsToReview(self):
        deck_name = self.getDeckName()
        inp = io_.SQLiteInput(deck_name)
        dates = inp.fetchDataFromDBDate_()
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
        finally:
            self.close()

    def renameDeck(self):
        self._rename_window = RenameDeck(self, self.deck)
