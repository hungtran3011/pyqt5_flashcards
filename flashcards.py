#!/usr/bin/env python3
import sys
import os
from platform import system
from pathlib import Path

from PyQt5 import QtGui, QtWidgets

from browse_deck import BrowseDeck, DeckInfo
from flashcards_mode import FlashcardsMode
from game_mode import GameMode
from new_cards_list import NewCardsList

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
SYSTEM = system()
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"

if not os.path.isdir(IMG_DIR):
    os.mkdir(IMG_DIR)
if not os.path.isdir(DECKS_DIR):
    os.mkdir(DECKS_DIR)

ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")

class ModifiedBrowseDeck(BrowseDeck):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._add_deck.clicked.connect(self.showAddDeck)
        try:
            self._show_all_decks()
        except ZeroDivisionError:
            pass

    def getDecksArea(self):
        return self.gridLayout
    
    def _show_all_decks(self):
        DECKS_LIST = [i for i in os.listdir(DECKS_DIR) if i.endswith(".db")]
        DECKS_NUM = len(DECKS_LIST)
        if len(DECKS_LIST) > 0:
            print(self._all_decks_area.width())
            columns = self._all_decks_area.width() // 480
            full_rows_num = DECKS_NUM // columns
            print(f"columns = {columns}, full_rows_num = {full_rows_num}")
            remainder = DECKS_NUM % columns
            for deck in reversed(range(self.getDecksArea().count())):
                tmp_widget = self.getDecksArea().itemAt(deck).widget()
                self.getDecksArea().removeWidget(tmp_widget)
                tmp_widget.setParent(None)
                tmp_widget.deleteLater()

            for row in range(full_rows_num):
                for col in range(columns):
                    index = columns * row + col
                    try:
                        deck_name = ModifiedDeckInfo(
                            self, f"{DECKS_LIST[index][0:len(DECKS_LIST[index]) - 3]}")
                        self.getDecksArea().addWidget(deck_name, row, col)
                    except:
                        col -= 1
            if remainder != 0:
                new_row = full_rows_num
                for col in range(remainder):
                    index = new_row * columns + col
                    try:
                        deck_name = ModifiedDeckInfo(
                            self, f"{DECKS_LIST[index][0:len(DECKS_LIST[index]) - 3]}")
                        self.getDecksArea().addWidget(deck_name, new_row, col)
                    except:
                        col -= 1
            self.setNumberOfDecks()
        else:
                for deck in reversed(range(self.getDecksArea().count())):
                    tmp_widget = self.getDecksArea().itemAt(deck).widget()
                    self.getDecksArea().removeWidget(tmp_widget)
                    tmp_widget.setParent(None)
                    tmp_widget.deleteLater()
                self.setNumberOfDecks()
                self.getDecksArea().addWidget(self._add_deck_icon, 0, 0)
                self.getDecksArea().addWidget(self._add_deck_label, 1, 0)

    def resizeEvent(self, event):
        self._show_all_decks()
    
    def showAddDeck(self, event):
        try:
            self.showAddDeckPopup()
        finally:
            window.setBrowseDecksMode()


class ModifiedDeckInfo(DeckInfo):
    def __init__(self, parent, deck, *args, **kwargs):
        super().__init__(parent, deck)
        self._game_mode.clicked.connect(self._showGameMode)
        self._view_cards_list.clicked.connect(self._showViewCardsMode)
        self._flash_mode.clicked.connect(self._showFlashcardsMode)
        self._contextMenu = QtWidgets.QMenu()
        self._contextMenu.addAction("Delete deck").triggered.connect(self.modified_deleteDeck)
        self._contextMenu.addAction("Rename deck").triggered.connect(self.renameDeck)
        self._more_funcs.setMenu(self._contextMenu)
    
    def _showFlashcardsMode(self):
        window.setFlashcardsMode(self.deck)

    def _showGameMode(self, deck=None):
        window.setGameMode(self.deck)

    def _showViewCardsMode(self, deck=None):
        window.setNewCardsList(self.deck)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        window.setNewCardsList(self.deck)

    def modified_deleteDeck(self):
        self.deleteDeck()
        window.setBrowseDecksMode()

class ModifiedFlashcardsMode(FlashcardsMode):
    def __init__(self, *args, **kwargs):
        super().__init__()

    def modified_configureWidgets(self):
        self._back.clicked.connect(window.setBrowseDecksMode)
        self.configureWidgets()
    
    def modified_set_deck(self, deck, event=None):
        self.set_deck(deck)
        self.modified_configureWidgets()

    def _practiceDeck(self):
        window.setGameMode(self.deck)

    def back(self):
        try:
            window.setBrowseDeckMode()
        except:
            window.setBrowseDeckMode()


class ModifiedGameMode(GameMode):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.back_button.clicked.connect(self.back)
    
    def back(self):
        window.setBrowseDecksMode()


class ModifiedNewCardsList(NewCardsList):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self._back.clicked.connect(self._back_home)

    def _back_home(self):
        window.setBrowseDecksMode()


class Settings(QtWidgets.QWidget):
    pass


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setMinimumSize(600, 536)
        self.setWindowTitle("All decks")
        self.setWindowIcon(QtGui.QIcon(str(IMG_DIR) + "/flash.ico"))
        self._stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self._stacked_widget)
        self._browse_decks_widget = ModifiedBrowseDeck(self._stacked_widget)
        self._stacked_widget.addWidget(self._browse_decks_widget)
        self._flash_mode_widget = ModifiedFlashcardsMode(self)
        self._stacked_widget.addWidget(self._flash_mode_widget)
        self._game_mode_widget = ModifiedGameMode(self)
        self._stacked_widget.addWidget(self._game_mode_widget)
        self._new_cards_list = ModifiedNewCardsList(self)
        self._stacked_widget.addWidget(self._new_cards_list)
        self._stacked_widget.setCurrentWidget(self._browse_decks_widget)
        self.adjustSize()

    def getBrowseDeckWidget(self):
        return self._browse_decks_widget

    def setBrowseDecksMode(self):
        self._stacked_widget.setCurrentWidget(self._browse_decks_widget)
        self.setWindowTitle("All decks")
        self._browse_decks_widget._show_all_decks()

    def setFlashcardsMode(self, deck):
        self._stacked_widget.setCurrentWidget(self._flash_mode_widget)
        self._flash_mode_widget.modified_set_deck(deck)
        print(self._flash_mode_widget.deck)
        self.setWindowTitle(f"Flashcards mode from deck: {deck}")
        # self._flash_mode_widget.configureWidgets()

    def setGameMode(self, deck):
        self._stacked_widget.setCurrentWidget(self._game_mode_widget)
        self._game_mode_widget.set_deck(deck)
        self.setWindowTitle(f"Practice mode/ Game mode for deck: {deck}")

    def setNewCardsList(self, deck):
        self._stacked_widget.setCurrentWidget(self._new_cards_list)
        self._new_cards_list.set_deck(deck)
        self.setWindowTitle(f"Cards list from deck: {deck}")

    def resizeEvent(self, event: QtGui.QResizeEvent =None) -> None:
        print(self.height())

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()