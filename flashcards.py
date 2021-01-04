import sys
import os
# from os.path import expanduser
import random as rand
from datetime import date, datetime
from platform import system
from shutil import copy, rmtree
from math import ceil
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from ui_browse_deck import Ui__browse_deck
from ui_deck_info import Ui__deck_info
from ui_show_cards import Ui__show_cards
from ui_add_deck import Ui__add_deck
from ui_cards_list import Ui__cards_list
from ui_add_card import Ui__add_card
from ui_rename_deck import Ui__rename_deck
from ui_edit_card import Ui__edit_card
from ui_new_cards_list import Ui__new_cards_list
from ui_card_info import Ui__card_info

import io_

ROOT_DIR = Path(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
print(ROOT_DIR)

SYSTEM = system()
# IMG_DIR = Path.cwd() / ROOT_DIR / "img"
# DECKS_DIR = Path.cwd() / ROOT_DIR / "decks"
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"

# class ClickableFrame(QtWidgets.QFrame):
#     def __init__(self, parent=None, *args, **kwargs):
#         super().__init__(parent)

#     def mousePressEvent(self, event)


class BrowseDeck(Ui__browse_deck, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._add_deck.clicked.connect(self._showAddDeckPopup)
        self._add_deck.setCursor(QtCore.Qt.PointingHandCursor)
        try:
            self._showAllDecks()
        except:
            pass
        self.refresh = self._showAllDecks

    def getDeckArea(self):
        return self.gridLayout
    
    def setNumberOfDecks(self, number):
        text = f'{number} deck' if number == 1 else f'{number} decks'
        self._number_of_decks.setText(text)

    def _showAddDeckPopup(self):
        self._dialog_add_deck = AddDeck(self)

    def _showAllDecks(self):
        DECKS_LIST = [i for i in os.listdir(DECKS_DIR) if i.endswith(".db")]
        DECKS_NUM = len(DECKS_LIST)
        if len(DECKS_LIST) > 0:
            # print(self._all_decks_area.width())
            columns = self._all_decks_area.width() // 480
            rows = DECKS_NUM // columns 
            print(columns, rows)
            remainder = DECKS_NUM % columns
            for i in reversed(range(self.getDeckArea().count())): 
                self.getDeckArea().itemAt(i).widget().setParent(None)
            for row in range(rows):
                for col in range(columns):
                    index = columns * row + col
                    # print(index)
                    deck_name = DeckInfo(self, f"{DECKS_LIST[index][0:len(DECKS_LIST[index]) - 3]}")
                    self.getDeckArea().addWidget(deck_name, row, col)
            if remainder != 0:
                new_row = rows
                for i in range(remainder):
                    index = new_row * columns + i
                    deck_name = DeckInfo(self, f"{DECKS_LIST[index][0:len(DECKS_LIST[index]) - 3]}")
                    self.getDeckArea().addWidget(deck_name, new_row, i)
            self.setNumberOfDecks(DECKS_NUM)
        else:
            try:
                for i in reversed(range(self.getDeckArea().count())): 
                    self.getDeckArea().itemAt(i).widget().setParent(None)
                self.setNumberOfDecks(DECKS_NUM)
            except:
                pass

    def resizeEvent(self, event):
        self._showAllDecks()

class AddDeck(Ui__add_deck, QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self._cancel_button.clicked.connect(self.close)
        self._save_button.clicked.connect(self._save)
        self.exec_()

    def _sendMessage(self, message):
        self._message.setText(message)

    def _save(self):
        def isValidFileName(file_name):
            restricted_char = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
            if len(file_name) == 0 or len(file_name) > 256:
                return False
            else:
                for i in file_name:
                    if i in restricted_char:
                        return False
            return True

        name = self._new_deck_box.text()
        file_name = f"{DECKS_DIR}/{name}.db"
        # print(file_name)
        file_list = os.listdir(DECKS_DIR)
        restricted_char = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
        if name == "":
            self._sendMessage("The name must not be blank")
        else:
            if file_name.split("/")[-1] not in file_list:
                # print(file_name in file_list)
                # print(file_list)
                if isValidFileName(name):
                    open(file_name, "a+").close()
                    out = io_.Output(name)
                    out.createTable("DECK")
                    out.createTable("DATE_")
                    window._showAllDecks()
                    os.chdir(f"{IMG_DIR}")
                    os.mkdir(f"{IMG_DIR}/{name}")
                    self.close()
                else:
                    self._sendMessage(f"""Can't add new deck. Please try renaming it.
    Note: Don't use these characters: {", ".join(restricted_char)}""")
            else:
                self._sendMessage(f"""The deck {file_name.split("/")[-1].split(".")[0]} has been existed""")


class DeckInfo(Ui__deck_info, QtWidgets.QGroupBox):
    def __init__(self, parent, deck):
        super().__init__(parent)
        self.setupUi(self)
        self.deck = deck
        self.setDeckName(self.deck)
        shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(201, 199, 199))
        self.setGraphicsEffect(shadow)
        self._game_mode.clicked.connect(self._showGameMode)
        self._game_mode.setCursor(QtCore.Qt.PointingHandCursor)
        self._view_cards_list.clicked.connect(self._showViewMode)
        self._view_cards_list.setCursor(QtCore.Qt.PointingHandCursor)
        self._flash_mode.setCursor(QtCore.Qt.PointingHandCursor)
        self.contextMenu = QtWidgets.QMenu()
        self.contextMenu.addAction("Delete deck").triggered.connect(self._deleteDeck)
        self.contextMenu.addAction("Rename deck").triggered.connect(self._renameDeck)
        self._more_funcs.setMenu(self.contextMenu)
        self._more_funcs.setCursor(QtCore.Qt.PointingHandCursor)
        self._evaluateNumOfCards()
        self._evaluateNumOfCardsToReview()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        
    def _evaluateNumOfCards(self):
        deck_name = self.getDeckName()
        inp = io_.Input(deck_name)
        number = len(inp.fetchDataFromDBDeck())
        text = f'{number} card' if number == 1 else f'{number} cards'
        self._num_of_cards.setText(text)

    def _evaluateNumOfCardsToReview(self):
        deck_name = self.getDeckName()
        inp = io_.Input(deck_name)
        dates = inp.fetchDataFromDBDate_()
        # print(dates)
        number = 0
        for rows in dates:
            if datetime.today() >= datetime.strptime(rows[3], "%Y-%m-%d"):
                number += 1
        text = f'{number} card to review' if number == 1 else f'{number} cards to review'
        self._cards_to_review.setText(text)

    def setDeckName(self, new_name):
        self._deck_name.setText(new_name)
        self._flash_mode.clicked.connect(lambda: self._showFlashMode(new_name))

    def getDeckName(self):
        return self._deck_name.text()

    def _showFlashMode(self, deck=None):
        self._flash_window = FlashMode(self, deck)

    def _showGameMode(self, deck=None):
        self._game_window = GameMode(self)

    def _showViewMode(self, deck=None):
        self._view_mode = CardsList(self, self.deck)

    def _deleteDeck(self):
        os.chdir(os.path.dirname(__file__))
        file_name = f"{DECKS_DIR}/{self.getDeckName()}.db"
        os.remove(file_name)
        img_folder_name = f"{IMG_DIR}/{self.getDeckName()}"
        # os.rmdir(img_folder_name)
        rmtree(img_folder_name)
        window._showAllDecks()

    def _renameDeck(self):
        self._rename_window = RenameDeck(self, self.deck)

    def mousePressEvent(self, event):
        self._view_mode = NewCardsList(self, self.deck)
        window.refresh()


class FlashMode(Ui__show_cards, QtWidgets.QDialog):
    def __init__(self, parent, deck=None):
        super().__init__(parent)
        self.deck = deck
        self.setupUi(self)
        self.setWindowTitle(f"Cards from: {self.deck}")
        shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=30, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(211, 211, 211))
        self._card_img.setGraphicsEffect(shadow)
        self._card_img.mousePressEvent = self._flipAnimationClicked
        self._card_img.mouseReleaseEvent = self._flipAnimationReleased
        self._card.setWordWrap(True)
        self._back.clicked.connect(self.close)
        self._flip.clicked.connect(self._flipCard)
        self._next.clicked.connect(self._nextCard)
        self._previous.clicked.connect(self._prevCard)
        self._shuffle.clicked.connect(self._shuffleCards)
        self._practice.clicked.connect(self._practiceDeck)
        self._add_card.clicked.connect(self._addCard)
        self._refresh.clicked.connect(self._refreshCards)
        self.cards_list = self._createCardsLists()
        self.front_list = list(self.cards_list)
        rand.shuffle(self.front_list)
        self._number = 0
        self._face = 0
        try:
            self._displayCard()
        except IndexError:
            self._card.setText("")
        self.exec_()

    def _createCardsLists(self):
        inp = io_.Input(self.deck)
        raw_deck = inp.fetchDataFromDBDeck()
        decks_list = {}
        for i in raw_deck:
            decks_list[i[1]] = [i[2], i[3]]
        return decks_list 

    def _count(self):
        if (cards_num := len(self.front_list)) > 0:
            self._num.setText(f"{self._number + 1}/{cards_num}")
        else:
            self._num.setText("0/0")

    def _displayCard(self):
        self._count()
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
                    pixmap = QtGui.QPixmap(f"{IMG_DIR}/white.jpg")
                    self._img.setPixmap(pixmap.scaledToWidth(300))

            elif self._face == 1:
                self._card.setText(back)
                pixmap = QtGui.QPixmap(f"{IMG_DIR}/white.jpg")
                self._img.setPixmap(pixmap.scaledToWidth(300))
                
            if self._number == len(self.front_list) - 1:
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
        self._number = self._number + 1 if self._number < len(self.front_list) - 1 else self._number
        self._face = 0             
        self._displayCard()

    def _prevCard(self):
        self._number = self._number - 1 if self._number > 0 else self._number
        self._face = 0
        self._displayCard()

    def _shuffleCards(self):
        self._number = 0
        self._face = 0
        rand.shuffle(self.front_list)
        self._displayCard()

    def _practiceDeck(self):
        self._game_window = GameMode(self)

    def closeEvent(self, event):
        window.refresh()

    def _refreshCards(self):
        self.cards_list = self._createCardsLists()
        self.front_list = list(self.cards_list)
        self._shuffleCards()

    def _addCard(self):
        self._add_card_dialog = AddCard(self, self.deck)
        self._refreshCards()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Left: 
            self._prevCard()
        elif event.key() == QtCore.Qt.Key_Right:
            self._nextCard()
        # elif event.key() == Qt.Key_Up:
        #     self._flipCard()  

    def _flipAnimationClicked(self, event):
        self._flipCard()
        shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=5, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(211, 211, 211))
        self._card_img.setGraphicsEffect(shadow)

    def _flipAnimationReleased(self, event):
        shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=30, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(211, 211, 211))
        self._card_img.setGraphicsEffect(shadow)

    
class GameMode(QtWidgets.QDialog):
    def __init__(self, parent, deck=None):
        super().__init__(parent)
        self.deck = deck
        # self.setupUi(self)
        # self._back.clicked.connect(self.close)
        label = QtWidgets.QLabel("This feature is being developed", self)
        label.adjustSize()
        self.adjustSize()
        self.exec_()


class AddCard(QtWidgets.QDialog, Ui__add_card):
    def __init__(self, parent, deck):
        super().__init__(parent)
        self.deck = deck 
        self.setupUi(self)
        self.setWindowTitle(f"Add new card to deck: {self.deck}")
        self._img.setGeometry(self._img.x(), self._img.y(), 300, 400)
        self._save_button.clicked.connect(self._saveCards)
        self._choose_image.clicked.connect(self._chooseImage)
        self._cancel_button.clicked.connect(self.close)
        self._img_file = ""
        self.exec_()

    def _saveCards(self):
        img_file_ = ""
        inp = io_.Input(self.deck)
        index = len(inp.fetchDataFromDBDeck()) + 1
        out = io_.Output(self.deck)
        front = self._front_box.toPlainText()
        back = self._back_box.toPlainText()
        try:
            img_file = self._img_file.split("/")[-1]
            tmp = img_file.split(".")
            tmp[-2] = front
            img_file_ = ".".join(tmp)
            print(f"{IMG_DIR}/{self.deck}/{img_file_}")
        except:
            pass
        data_card = (index, front, back, f"{IMG_DIR}/{self.deck}/{img_file_}")
        data_date = (index, front, None, date.today())
        out.writeToDB(data_card, "DECK")
        out.writeToDB(data_date, "DATE_")
        if self._img_file != "":
            import shutil
            shutil.copyfile(self._img_file, f"{IMG_DIR}/{self.deck}/{img_file_}")
        else:
            pass
        self.close()

    def _chooseImage(self):
        default_dir = f'{os.path.expanduser("~")}/Pictures'
        print(default_dir)
        self._img_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", default_dir)
        pixmap = QtGui.QPixmap(self._img_file)
        self._img.setPixmap(pixmap.scaledToHeight(200))


class CardsList(QtWidgets.QDialog, Ui__cards_list):
    def __init__(self, parent, deck):
        super().__init__(parent)
        self.deck = deck
        self.setupUi(self)
        self._add_card_button.clicked.connect(self._showAddCard)
        self._delete_button.clicked.connect(self._deleteCard)
        self._edit_button.clicked.connect(self._editCards)
        self._refresh_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("F5"), self)
        self._refresh_shortcut.activated.connect(self._showItems)
        self._cards_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self._cards_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._cards_table.doubleClicked.connect(self.boo)
        self._showItems()
        self.setWindowTitle(f"Cards list from deck: {self.deck}")
        self.exec_()

    def boo(self):
        print(self._cards_table.selectedIndexes())
        index = self._cards_table.selectedIndexes()
        for i in index:
            id_us = self._cards_table.model().data(i)
            print(id_us, end=" ")
        print()

    def _showItems(self):
        self._cards_list = io_.Input(self.deck).fetchDataFromDBDeck()
        self._cards_table.setRowCount(0)
        for idx in self._cards_list:
            id_, front, back, img = idx
            row = id_ - 1
            self._cards_table.insertRow(row)
            self._cards_table.setItem(row, 0, QtWidgets.QTableWidgetItem(front))
            self._cards_table.setItem(row, 1, QtWidgets.QTableWidgetItem(back)) 

    def _deleteCard(self):
        current_row = self._cards_table.currentRow()
        word = self._cards_table.item(current_row, 0).text()
        print(word)
        db = io_.Input(self.deck)
        out = io_.Output(self.deck)
        out.cursor.execute("DELETE FROM DECK WHERE FRONT = ?", (word,))
        out.conn.commit()
        out.cursor.execute("DELETE FROM DATE_ WHERE CARD = ?", (word,))
        out.conn.commit()

        db.cursor.execute("SELECT FRONT, BACK, IMG FROM DECK")
        tmp_deck = db.cursor.fetchall()
        out.cursor.execute("DROP TABLE DECK")
        out.conn.commit()
        out.createTable("DECK")
        for key, val in enumerate(tmp_deck):
            print(key)
            data = (key + 1,) + val
            out.writeToDB(data, "DECK")
        print(tmp_deck)
        db.cursor.execute("SELECT CARD, LAST_REVIEW, NEXT_REVIEW FROM DATE_")
        tmp_date = db.cursor.fetchall()
        print(tmp_date)
        out.cursor.execute("DROP TABLE DATE_")
        out.conn.commit()
        out.createTable("DATE_")
        for key, val in enumerate(tmp_date):
            data = (key + 1,) + val
            out.writeToDB(data, "DATE_")
        self._showItems()

    def _showAddCard(self):
        self._add_card_dialog = AddCard(self, self.deck)
        self._showItems()

    def _editCards(self):
        current_row = self._cards_table.currentRow()
        try:
            word = self._cards_table.item(current_row, 0).text()
            self._edit_dialog = EditCard(self, self.deck, word)
            self._showItems()
        except AttributeError:
            pass

    def closeEvent(self, event):
        window._showAllDecks()


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
        os.rename(f"{IMG_DIR}/{self.deck}", f"{IMG_DIR}/{self._name_box.text()}")
        self.close()
        self.parent().setDeckName(self._name_box.text())
        window._showAllDecks()


class EditCard(QtWidgets.QDialog, Ui__edit_card):
    def __init__(self, parent, deck, word):
        super().__init__(parent)
        self.deck = deck
        self.word = word
        self.setupUi(self)
        self.setWindowTitle(f"Edit card: {self.word}")
        self._save_button.clicked.connect(self._save)
        self._img_button.clicked.connect(self._chooseImage)
        self._cancel_button.clicked.connect(self.close)
        self.__insertInfo()
        self.exec_()

    def __insertInfo(self):
        inp = io_.Input(self.deck)
        self.card_info = inp.selectFromDBDeck("FRONT", self.word)[0]
        _, self.front_text, self.back_text, self.img_link = self.card_info
        self._img_file = ""
        self._front.setText(self.front_text)
        self._back_box.insertPlainText(self.back_text)
        pixmap = QtGui.QPixmap(self.img_link)
        if not pixmap.isNull():
            self._img_preview.setPixmap(pixmap)
        else:
            self._img_preview.setText("")

    def _chooseImage(self):
        default_dir = f'{os.path.expanduser("~")}/Pictures'
        print(default_dir)
        self._img_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select Image", default_dir)
        pixmap = QtGui.QPixmap(self._img_file)
        self._img_preview.setPixmap(pixmap.scaledToHeight(100))

    def _save(self):
        img_file_ = ""
        try:
            img_file = self._img_file.split("/")[-1]
            print(img_file)
            tmp = img_file.split(".")
            tmp[-2] = self.word
            img_file_ = ".".join(tmp)
            tmp_link = f"{IMG_DIR}/{self.deck}/{img_file_}"
        except:
            pass
        if self._img_file != "":
            import shutil
            if not os.path.exists(f'{os.path.splitext(tmp_link)}.*'):
                shutil.copyfile(self._img_file, tmp_link)
            else:
                os.remove(f'{os.path.splitext(tmp_link)}.*')
                shutil.copyfile(self._img_file, tmp_link)
        else:
            pass
        output = io_.Output(self.deck)
        output.updateTable("DECK", "IMG", tmp_link, f"FRONT='{self.word}'")
        output.updateTable("DECK", "BACK", self._back_box.toPlainText(), f"FRONT='{self.word}'")
        self.close()

#The new cards list classes
class NewCardsList(QtWidgets.QDialog, Ui__new_cards_list):
    def __init__(self, parent, deck):
        super().__init__(parent)
        self.setupUi(self)
        self.deck = deck
        self.cards_data_widgets = []
        inp = io_.Input(self.deck)
        self.cards_data = inp.fetchDataFromDBDeck()
        self.setWindowTitle(f"Deck: {self.deck}")
        self.label.setText(f"Cards list from deck: {self.deck}")
        self._createCardsList()
        self._add_card.clicked.connect(self._addCard)
        self.exec_()

    def getCardsArea(self):
        return self.gridLayout_2

    def _createCardsList(self):
        num_of_cards = len(self.cards_data)
        if num_of_cards > 0:
            columns = self._all_cards_area.width() // 230
            rows = num_of_cards // columns 
            remainder = num_of_cards % columns
            for i in reversed(range(self.getCardsArea().count())): 
                self.getCardsArea().itemAt(i).widget().setParent(None)
            for row in range(rows):
                for col in range(columns):
                    index = columns * row + col
                    card_info = CardInfo(self, self.cards_data[index], self.deck)
                    self.cards_data_widgets.append(card_info)
                    contextMenu = QtWidgets.QMenu()
                    contextMenu.addAction("Delete card").triggered.connect(lambda: self._deleteCard(self.cards_data[index][1]))
                    card_info._options.setMenu(contextMenu)
                    self.getCardsArea().addWidget(card_info, row, col)
            if remainder != 0:
                new_row = rows
                for i in range(remainder):
                    index = new_row * columns + i
                    card_info = CardInfo(self, self.cards_data[index], self.deck)
                    self.getCardsArea().addWidget(card_info, new_row, i)

    def _addCard(self):
        self._showAddCard = AddCard(self, self.deck)
        inp = io_.Input(self.deck)
        self.cards_data = inp.fetchDataFromDBDeck()
        self._createCardsList()

    def resizeEvent(self, event):
        self._createCardsList()

    def _deleteCard(self, card):
        db = io_.Input(self.deck)
        out = io_.Output(self.deck)
        out.cursor.execute("DELETE FROM DECK WHERE FRONT = ?", (card,))
        out.conn.commit()
        out.cursor.execute("DELETE FROM DATE_ WHERE CARD = ?", (card,))
        out.conn.commit()
        db.cursor.execute("SELECT FRONT, BACK, IMG FROM DECK")
        tmp_deck = db.cursor.fetchall()
        out.cursor.execute("DROP TABLE DECK")
        out.conn.commit()
        out.createTable("DECK")
        self.cards_data = []
        for key, val in enumerate(tmp_deck):
            data = (key + 1,) + val
            out.writeToDB(data, "DECK")
            self.cards_data.append(data)
        db.cursor.execute("SELECT CARD, LAST_REVIEW, NEXT_REVIEW FROM DATE_")
        tmp_date = db.cursor.fetchall()
        out.cursor.execute("DROP TABLE DATE_")
        out.conn.commit()
        out.createTable("DATE_")
        for key, val in enumerate(tmp_date):
            data = (key + 1,) + val
            out.writeToDB(data, "DATE_")
        self._createCardsList()

class CardInfo(QtWidgets.QGroupBox, Ui__card_info):
    def __init__(self, parent, card_info: tuple, deck=None):
        super().__init__(parent)
        self.card_info = card_info
        self.deck = deck
        self.setupUi(self)
        shadow = QtWidgets.QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(201, 199, 199))
        self._front.setWordWrap(True)
        self._back.setWordWrap(True)
        self.setGraphicsEffect(shadow)
        self._displayCardInfo()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        # self.contextMenu = QtWidgets.QMenu()
        # self.contextMenu.addAction("Delete card").triggered.connect(self._deleteCard)
        # self.contextMenu.addAction("Edit card").triggered.connect(self._editCard)
        # self._options.setMenu(self.contextMenu)
        self._options.setCursor(QtCore.Qt.PointingHandCursor)

    def _displayCardInfo(self):
        _, front, back, img = self.card_info
        self._front.setText(front)
        self._back.setText(back)
        pixmap = QtGui.QPixmap(img)
        if not pixmap.isNull():
            self._img.setPixmap(pixmap)
        else:
            self._img.setText("")

    def mousePressEvent(self, event):
        self._editCard = EditCard(self, self.deck, self._front.text())
        self._displayCardInfo()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BrowseDeck()
    window.setWindowTitle("Flashcards - All decks")
    window.setWindowIcon(QtGui.QIcon("flash.ico"))
    window.show()
    app.exec_()
