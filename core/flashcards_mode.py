import sys 
import os
import random as rand
from pathlib import Path

from PyQt5 import QtWidgets, QtGui

import core.io_ as io_
from core.ui_package.ui_show_cards import Ui__show_cards

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
IMG_DIR = ROOT_DIR / "../img"
DECKS_DIR = ROOT_DIR / "../decks"

class FlashcardsMode(Ui__show_cards, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self._flip.clicked.connect(self._flipCard)
        self._next.clicked.connect(self._nextCard)
        self._previous.clicked.connect(self._prevCard)
        self._shuffle.clicked.connect(self._shuffleCards)
        # self._practice.clicked.connect(self._practiceDeck)
        self._refresh.clicked.connect(self._refreshCards)

    def configureWidgets(self):
        self.setWindowTitle(f"Cards from: {self.deck}")
        self._img.setText("")
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=30, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(211, 211, 211))
        self._card_img.setGraphicsEffect(shadow)
        self._card_img.mousePressEvent = self._flipAnimationClicked
        self._card_img.mouseReleaseEvent = self._flipAnimationReleased
        self._card.setWordWrap(True)
        self.cards_list = self._createCardsLists()
        self.front_list = list(self.cards_list)
        rand.shuffle(self.front_list)
        self._number = 0
        self._face = 0
        try:
            self._displayCard()
        except IndexError:
            self._card.setText("")
        # self.exec_()

    def _createCardsLists(self):
        inp = io_.SQLiteInput(self.deck)
        raw_deck = inp.fetchDataFromDBDeck()
        decks_list = {}
        for i in raw_deck:
            decks_list[i[1]] = [i[2], i[3]]
        return decks_list

    def _count(self):
        cards_num = len(self.front_list)
        if cards_num > 0:
            self._num.setText(f"{self._number + 1}/{cards_num}")
        else:
            self._num.setText("0/0")

    def _displayCard(self):
        self._count()
        print(len(self.front_list) > 0)
        if len(self.front_list) > 0:
            front = self.front_list[self._number]
            back = self.cards_list[front][0]
            img_file = self.cards_list[front][1]
            if self._face == 0:
                self._card.setText(front)
                self._img.show()
                pixmap = QtGui.QPixmap(img_file)
                if not pixmap.isNull():
                    self._img.setPixmap(pixmap.scaledToWidth(300))
                else:
                    pixmap = QtGui.QPixmap(f"{str(IMG_DIR)}/dull_image.png")
                    self._img.setPixmap(pixmap.scaledToWidth(300))
                self._img.show()

            elif self._face == 1:
                self._card.setText(back)
                pixmap = QtGui.QPixmap(f"{str(IMG_DIR)}/dull_image.png")
                self._img.setPixmap(pixmap.scaledToWidth(300))

            if self._number == len(self.front_list) - 1 \
                    or (self._number == 1 and len(self.front_list) == 1):
                self._next.setEnabled(False)
            else:
                self._next.setEnabled(True)
            if self._number == 0:
                self._previous.setEnabled(False)
            else:
                self._previous.setEnabled(True)
        else:
            self._previous.setEnabled(False)
            self._next.setEnabled(False)
            self._flip.setEnabled(False)
            self._refresh.setEnabled(False)
            self._shuffle.setEnabled(False)
            self._practice.setEnabled(False)

    def _flipCard(self, event=None):
        self._face = 1 if self._face == 0 else 0
        self._displayCard()

    def _nextCard(self):
        print(self._number)
        self._number = self._number + \
            1 if self._number < len(self.front_list) - 1 else self._number
        self._face = 0
        self._displayCard()

    def _prevCard(self):
        print(self._number)
        self._number = self._number - 1 if self._number > 0 else self._number
        self._face = 0
        self._displayCard()

    def _shuffleCards(self):
        self._number = 0
        self._face = 0
        rand.shuffle(self.front_list)
        self._displayCard()

    # def _practiceDeck(self):
    #     window.setGameMode(self.deck)

    # def closeEvent(self, event):
    #     window.getBrowseDeckWidget().refresh()

    def _refreshCards(self):
        self.cards_list = self._createCardsLists()
        self.front_list = list(self.cards_list)
        self._shuffleCards()

    def _flipAnimationClicked(self, event):
        self._flipCard()
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=5, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(211, 211, 211))
        self._card_img.setGraphicsEffect(shadow)

    def _flipAnimationReleased(self, event):
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=30, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(211, 211, 211))
        self._card_img.setGraphicsEffect(shadow)

    def set_deck(self, deck_name):
        self.deck = deck_name
        print(self.deck)
        self.cards_list = self._createCardsLists()
        self.front_list = list(self.cards_list)
        rand.shuffle(self.front_list)
        self._number = 0
        self._face = 0
        self.configureWidgets()