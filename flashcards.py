#!/usr/bin/env python3

import sys
import os
import random as rand
from datetime import date, datetime
from platform import system
import shutil
# from math import ceil
from pathlib import Path
import functools

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

from ui_browse_deck import Ui__browse_deck
from ui_deck_info import Ui__deck_info
from ui_show_cards import Ui__show_cards
from ui_cards_list import Ui__cards_list
from ui_add_card import Ui_add_card
from ui_rename_deck import Ui__rename_deck
from ui_edit_card import Ui__edit_card
from ui_new_cards_list import Ui__new_cards_list
from ui_card_info import Ui__card_info
from ui_game_mode import Ui__game_mode
from ui_new_add_deck import Ui_new_add_deck

import io_

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
SYSTEM = system()
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"

if not os.path.isdir(IMG_DIR):
    os.mkdir(IMG_DIR)
if not os.path.isdir(DECKS_DIR):
    os.mkdir(DECKS_DIR)

ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")


class BrowseDeck(Ui__browse_deck, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setupUi(self)
        self._add_deck.clicked.connect(self._showAddDeckPopup)
        self._add_deck.setCursor(QtCore.Qt.PointingHandCursor)
        self._add_deck_icon = QtSvg.QSvgWidget(ADD_DECK_ICON)
        self._add_deck_icon.mousePressEvent = self._showAddDeckPopup
        self._add_deck_icon.setToolTip("Add a deck")
        self._add_deck_icon.setCursor(QtCore.Qt.PointingHandCursor)
        self._add_deck_icon.setMaximumSize(200, 200)
        self._add_deck_label = QtWidgets.QLabel("Please add some decks")
        self._add_deck_label.setAlignment(QtCore.Qt.AlignCenter)
        self._create_function_menu()
        try:
            self._show_all_decks()
        except:
            pass
        # self.refresh = self._show_all_decks

    def refresh(self):
        self._show_all_decks()

    def getDecksArea(self):
        return self.gridLayout

    def setNumberOfDecks(self):
        DECKS_LIST = [i for i in os.listdir(DECKS_DIR) if i.endswith(".db")]
        DECKS_NUM = len(DECKS_LIST)
        text = f'{DECKS_NUM} deck' if DECKS_NUM == 1 else f'{DECKS_NUM} decks'
        self._number_of_decks.setText(text)

    def _showAddDeckPopup(self, event=None):
        self._dialog_add_deck = AddDeck(self)

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
                    deck_name = DeckInfo(
                        self, f"{DECKS_LIST[index][0:len(DECKS_LIST[index]) - 3]}")
                    self.getDecksArea().addWidget(deck_name, row, col)
            if remainder != 0:
                new_row = full_rows_num
                for i in range(remainder):
                    index = new_row * columns + i
                    deck_name = DeckInfo(
                        self, f"{DECKS_LIST[index][0:len(DECKS_LIST[index]) - 3]}")
                    self.getDecksArea().addWidget(deck_name, new_row, i)
            self.setNumberOfDecks()
        else:
            try:
                for deck in reversed(range(self.getDecksArea().count())):
                    tmp_widget = self.getCardsArea().itemAt(deck).widget()
                    self.getDecksArea().removeWidget(tmp_widget)
                    tmp_widget.setParent(None)
                    tmp_widget.deleteLater()
                self.setNumberOfDecks()
                self.getDecksArea().addWidget(self._add_deck_icon, 0, 0)
                self.getDecksArea().addWidget(self._add_deck_label, 1, 0)
            except:
                print("Nothing")

    def resizeEvent(self, event):
        self._show_all_decks()

    def _create_function_menu(self):
        function_menu = QtWidgets.QMenu(self._more_funcs)
        settings = function_menu.addAction("Settings...")
        settings.triggered.connect(self._showAddDeckPopup)
        self._more_funcs.setMenu(function_menu)

    def keyPressEvent(self, event=QtCore.Qt.Key_F5):
        self._show_all_decks()

    def mousePressEvent(self, event):
        if event == QtCore.Qt.RightButton:
            menu = QtWidgets.QMenu(self)
            menu.addAction("Refresh").triggered.connect(self._show_all_decks)
            menu.popup(self.mapToGlobal(event.pos()))


# class AddDeck(Ui__add_deck, QtWidgets.QDialog):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.setupUi(self)
#         self._cancel_button.clicked.connect(self.close)
#         self._save_button.clicked.connect(self._save)
#         self.exec_()

#     def _sendMessage(self, message):
#         self._message.setText(message)

#     def _save(self):
#         def isValidFileName(file_name):
#             restricted_char = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
#             if len(file_name) == 0 or len(file_name) > 256:
#                 return False
#             else:
#                 for i in file_name:
#                     if i in restricted_char:
#                         return False
#             return True

#         name = self._new_deck_box.text()
#         file_name = f"{DECKS_DIR}/{name}.db"
#         file_list = os.listdir(DECKS_DIR)
#         restricted_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
#         if name == "":
#             self._sendMessage("The name must not be blank")
#         else:
#             if file_name.split("/")[-1] not in file_list:
#                 if isValidFileName(name):
#                     open(file_name, "a+").close()
#                     out = io_.SQLiteOutput(name)
#                     out.createTable("DECK")
#                     out.createTable("DATE_")
#                     # window.getBrowseDeckWidget()._show_all_decks()
#                     window.setBrowseDecksMode()
#                     os.chdir(f"{IMG_DIR}")
#                     os.mkdir(f"{IMG_DIR}/{name}")
#                     self.close()
#                 else:
#                     self._sendMessage(f"""Can't add new deck. Please try a different name.
#     Note: Don't use these characters: {", ".join(restricted_chars)}""")
#             else:
#                 self._sendMessage(f"""The deck {file_name.split("/")[-1].split(".")[0]} has been existed""")


class AddDeck(Ui_new_add_deck, QtWidgets.QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.import_button.clicked.connect(self.import_file)
        self.save_button.clicked.connect(self.save)
        self.cancel_button.clicked.connect(self.close)
        self.file_obj = ["", ""]
        self.exec()

    def _send_message(self, message):
        popup = QtWidgets.QMessageBox(self)
        popup.setIcon(QtWidgets.QMessageBox.Warning)
        popup.setText(message)
        popup.exec()

    def import_file(self):
        open_dialog = QtWidgets.QFileDialog(self)
        open_dialog.setAcceptMode(open_dialog.AcceptOpen)
        self.file_obj = open_dialog.getOpenFileName(
            directory="~", filter="CSV Files (*.csv);; JSON Files (*.json);; XML Files (*.xml)")
        # The file_obj is a tuple returned by QFileDialog.getOpenFileName
        # with the structure ([FILE_DIRECTORY], [FILE_TYPE_FILTER])
        # Use file_obj[0] to get the directory of the file chosen
        # and file_obj[1] to get the file type
        imported_file = self.file_obj[0]
        self.imported_file_name.setText(self.file_obj[0])
        self.parsed_data = ""
        if self.file_obj[1] == "CSV Files (*.csv)":
            importer = io_.CSVImporter(imported_file)
            self.parsed_data = importer.get_parsed_data()
            print(self.parsed_data)
        elif self.file_obj[1] == "JSON Files (*.json)":
            importer = io_.JSONImporter(imported_file)
            self.parsed_data = importer.get_parsed_data()
            print(self.parsed_data)
        elif self.file_obj[1] == "XML Files (*.XML)":
            importer = io_.XMLImporter(imported_file)
            self.parsed_data = importer.get_parsed_data()
            print(self.parsed_data)
        else:
            raise ValueError("The file type must be CSV, JSON or XML")

    def save(self):
        def isValidFileName(file_name):
            restricted_char = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
            if len(file_name) == 0 or len(file_name) > 256:
                return False
            else:
                for i in file_name:
                    if i in restricted_char:
                        return False
            return True

        name = self.deck_name_box.text()
        file_name = f"{DECKS_DIR}/{name}.db"
        file_list = os.listdir(DECKS_DIR)
        restricted_chars = ["<", ">", ":", "\"", "/", "\\", "|", "?", "*"]
        if name == "":
            self._send_message("The name must not be blank")
        else:
            if os.path.basename(file_name) not in file_list:
                if isValidFileName(name):
                    open(file_name, "a+").close()
                    out = io_.SQLiteOutput(name)
                    out.createTable("DECK")
                    out.createTable("DATE_")
                    window.setBrowseDecksMode()
                    os.chdir(f"{IMG_DIR}")
                    os.mkdir(f"{IMG_DIR}/{name}")
                    del out
                else:
                    self._send_message(f"""Can't add new deck. Please try a different name.
    Note: Don't use these characters: {", ".join(restricted_chars)}""")
            else:
                self._send_message(
                    f"""The deck {name} has been existed""")
        if self.importing_radiobutton.isChecked() is True and self.file_obj[0] != "":
            # try:
                open(file_name, "a+").close()
                output = io_.SQLiteOutput(name)
                for card in self.parsed_data:
                    output.writeToDB(card, "DECK")
                    output.writeToDB(
                        (card[0], card[1], None, date.today()),
                         "DATE_"
                    )
                window.setBrowseDecksMode()
                self.close()
            # except:
            #     self._send_message("Error in importing file(s)")
        elif self.importing_radiobutton.isChecked() is True and self.file_obj[0] == "":
            self._send_message("The name of the imported file must not be blank")
        else:
            pass


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
        self._game_mode.clicked.connect(
            functools.partial(self._showGameMode, self.deck))
        self._game_mode.setCursor(QtCore.Qt.PointingHandCursor)
        self._view_cards_list.clicked.connect(self._showViewMode)
        self._view_cards_list.setCursor(QtCore.Qt.PointingHandCursor)
        self._flash_mode.setCursor(QtCore.Qt.PointingHandCursor)
        self._contextMenu = QtWidgets.QMenu()
        self._contextMenu.addAction("Delete deck").triggered.connect(self._deleteDeck)
        self._contextMenu.addAction("Rename deck").triggered.connect(self._renameDeck)
        self._more_funcs.setMenu(self._contextMenu)
        self._more_funcs.setCursor(QtCore.Qt.PointingHandCursor)
        self._evaluateNumOfCards()
        self._evaluateNumOfCardsToReview()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setToolTip("Click the title to view cards list")

    def _evaluateNumOfCards(self):
        deck_name = self.getDeckName()
        inp = io_.SQLiteInput(deck_name)
        number = len(inp.fetchDataFromDBDeck())
        text = f'{number} card' if number == 1 else f'{number} cards'
        self._num_of_cards.setText(text)

    def _evaluateNumOfCardsToReview(self):
        deck_name = self.getDeckName()
        inp = io_.SQLiteInput(deck_name)
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
        print("name = ", new_name)
        self._flash_mode.clicked.connect(lambda: self._showFlashMode(new_name))

    def getDeckName(self):
        return self._deck_name.text()

    def _showFlashMode(self, deck=None):
        window.setFlashcardsMode(deck)

    def _showGameMode(self, deck=None):
        window.setGameMode(deck)

    def _showViewMode(self, deck=None):
        window.setNewCardsList(self.deck)

    def _deleteDeck(self):
        # os.chdir(os.path.dirname(__file__))
        try:
            file_name = f"{DECKS_DIR}/{self.getDeckName()}.db"
            os.remove(file_name)
            img_folder_name = f"{IMG_DIR}/{self.getDeckName()}"
            shutil.rmtree(img_folder_name)
        except:
            pass
        finally:
            window.setBrowseDecksMode()

    def _renameDeck(self):
        self._rename_window = RenameDeck(self, self.deck)

    def mousePressEvent(self, event):
        window.setNewCardsList(self.deck)


class FlashMode(Ui__show_cards, QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.deck = None
        self.setupUi(self)
        #self._add_card.clicked.connect(self._addCard)
        self._add_card.hide()
        self._flip.clicked.connect(self._flipCard)
        self._next.clicked.connect(self._nextCard)
        self._previous.clicked.connect(self._prevCard)
        self._shuffle.clicked.connect(self._shuffleCards)
        self._practice.clicked.connect(self._practiceDeck)
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
        self._back.clicked.connect(window.setBrowseDecksMode)
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
        # if (cards_num := len(self.front_list)) > 0:
        #     self._num.setText(f"{self._number + 1}/{cards_num}")
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
                    pixmap = QtGui.QPixmap(f"{str(IMG_DIR)} / dull_image.png")
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

    def _practiceDeck(self):
        window.setGameMode(self.deck)

    def closeEvent(self, event):
        window.getBrowseDeckWidget().refresh()

    def _refreshCards(self):
        self.cards_list = self._createCardsLists()
        self.front_list = list(self.cards_list)
        self._shuffleCards()

    def _addCard(self):
        self._add_card_dialog = AddCards(self, self.deck)
        self._refreshCards()

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
        # try:
        #self._displayCard()
        # except IndexError:
        #     self._card.setText("")
        # self.exec_()
        self.configureWidgets()


class GameMode(QtWidgets.QWidget, Ui__game_mode):
    def __init__(self, parent, deck=None):
        super().__init__(parent)
        self._deck = deck
        self.setupUi(self)
        # self.adjustSize()
        # self.exec_()
        self._right_answer = ""
        self._back.clicked.connect(self.back)
        self.button_A.clicked.connect(self.A_pressed)
        self.button_B.clicked.connect(self.B_pressed)
        self.button_C.clicked.connect(self.C_pressed)
        self.button_D.clicked.connect(self.D_pressed)

    def back(self):
        window.setBrowseDecksMode()

    def set_deck(self, deck):
        self._deck = deck

    def writting_check(self):
        pass

    def createQuestion(self):
        pass

    def A_pressed(self):
        self.multiple_choice_check("A")

    def B_pressed(self):
        self.multiple_choice_check("B")

    def C_pressed(self):
        self.multiple_choice_check("C")

    def D_pressed(self):
        self.multiple_choice_check("D")

    def multiple_choice_check(self, answer):
        print(f"Pressed answer: {answer}")


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


class CardsList(QtWidgets.QDialog, Ui__cards_list):
    def __init__(self, parent, deck):
        super().__init__(parent)
        self.deck = deck
        self.setupUi(self)
        self._add_card_button.clicked.connect(self._showAddCard)
        self._delete_button.clicked.connect(self._deleteCard)
        self._edit_button.clicked.connect(self._editCards)
        self._refresh_shortcut = QtWidgets.QShortcut(
            QtGui.QKeySequence("F5"), self)
        self._refresh_shortcut.activated.connect(self._showItems)
        self._cards_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self._cards_table.setSelectionBehavior(
            QtWidgets.QAbstractItemView.SelectRows)
        self._showItems()
        self.setWindowTitle(f"Cards list from deck: {self.deck}")
        self.exec_()

    def _showItems(self):
        self._cards_list = io_.SQLiteInput(self.deck).fetchDataFromDBDeck()
        self._cards_table.setRowCount(0)
        for idx in self._cards_list:
            id_, front, back, img = idx
            row = id_ - 1
            self._cards_table.insertRow(row)
            self._cards_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(front))
            self._cards_table.setItem(row, 1, QtWidgets.QTableWidgetItem(back))
            del img

    def _deleteCard(self):
        current_row = self._cards_table.currentRow()
        word = self._cards_table.item(current_row, 0).text()
        db = io_.SQLiteInput(self.deck)
        out = io_.SQLiteOutput(self.deck)
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
            data = (key + 1,) + val
            out.writeToDB(data, "DECK")
        db.cursor.execute("SELECT CARD, LAST_REVIEW, NEXT_REVIEW FROM DATE_")
        tmp_date = db.cursor.fetchall()
        out.cursor.execute("DROP TABLE DATE_")
        out.conn.commit()
        out.createTable("DATE_")
        for key, val in enumerate(tmp_date):
            data = (key + 1,) + val
            out.writeToDB(data, "DATE_")
        self._showItems()

    def _showAddCard(self):
        self._add_card_dialog = AddCards(self, self.deck)
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
        window.setBrowseDecksMode()


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
        window.setBrowseDecksMode()


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
        inp = io_.SQLiteInput(self.deck)
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
        self._img_file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select Image", default_dir)
        pixmap = QtGui.QPixmap(self._img_file)
        self._img_preview.setPixmap(pixmap.scaledToHeight(100))

    def _save(self):
        try:
            img_file = os.path.basename(self._img_file)
            tmp_link = f"{IMG_DIR}/{self.deck}/{img_file}"
            print()
            if self._img_file != "":
                if not os.path.exists(f'{os.path.splitext(tmp_link)}.*'):
                    shutil.copyfile(self._img_file, tmp_link)
                else:
                    os.remove(f'{os.path.splitext(tmp_link)}.*')
                    shutil.copyfile(self._img_file, tmp_link)
            else:
                pass
            output = io_.SQLiteOutput(self.deck)
            output.updateTable("DECK", "IMG", tmp_link,
                               condition=f"FRONT='{self.word}'")
        except:
            pass
        finally:
            output = io_.SQLiteOutput(self.deck)
            output.updateTable(
                "DECK", "BACK", self._back_box.toPlainText(), f"FRONT='{self.word}'")
            self.close()

# The new cards list classes
# with new fresh ui
# with customized and editable groupboxes (look like cards) for information:
# front, back, image

class NewCardsList(QtWidgets.QDialog, Ui__new_cards_list):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self._add_card.clicked.connect(self._addCard)
        self._back.clicked.connect(self._back_home)

    def set_deck(self, deck):
        self.deck = deck
        self.configureWidgets()

    def configureWidgets(self):
        self.cards_data_widgets = []
        self.setWindowTitle(f"Deck: {self.deck}")
        self.deck_label.setText(f"Cards list from deck: {self.deck}")
        self._add_card_label = QtWidgets.QLabel("Please add some cards")
        self._add_card_label.setAlignment(QtCore.Qt.AlignCenter)
        self._add_card_icon = QtSvg.QSvgWidget(ADD_CARDS_ICON)
        self._add_card_icon.setMaximumSize(200, 200)
        self._createCardsList()

    def getCardsArea(self):
        return self.gridLayout

    def _back_home(self):
        window.setBrowseDecksMode()
        # window.getBrowseDeckWidget()._show_all_decks()

    def _createCardsList(self):
        """
        Generate cards list from local database
        "Cards" a.k.a customized groupboxes are placed in grid layout
        inside a QScrollArea
        Responsive layout is implemented in this method, but needs some improvement
        (e.g smooth and faster arrange the 'cards') 
        """
        inp = io_.SQLiteInput(self.deck)
        #cards_data = []
        raw_cards_data = inp.fetchDataFromDBDeck()
        delete_cards_data = {}
        for data in raw_cards_data:
            delete_cards_data.update(
                {data[1]: functools.partial(self._deleteCard, data[1])})
        num_of_cards = len(raw_cards_data)
        for card in reversed(range(self.getCardsArea().count())):
            tmp_widget = self.getCardsArea().itemAt(card).widget()
            self.getCardsArea().removeWidget(tmp_widget)
            tmp_widget.setParent(None)
            tmp_widget.deleteLater()
        if num_of_cards > 0:
            columns = self._all_cards_area.width() // 230
            rows = num_of_cards // columns
            remainder = num_of_cards % columns
            for row in range(rows):
                for col in range(columns):
                    index = columns * row + col
                    card_info = CardInfo(
                        self, raw_cards_data[index], self.deck)
                    #self.cards_data_widgets.append(card_info)
                    contextMenu = QtWidgets.QMenu()
                    contextMenu.addAction("Delete card").triggered.connect(
                        delete_cards_data[raw_cards_data[index][1]])
                    card_info._options.setMenu(contextMenu)
                    self.getCardsArea().addWidget(card_info, row, col)
            if remainder != 0:
                new_row = rows
                for i in range(remainder):
                    index = new_row * columns + i
                    card_info = CardInfo(
                        self, raw_cards_data[index], self.deck)
                    contextMenu = QtWidgets.QMenu()
                    contextMenu.addAction("Delete card").triggered.connect(
                        delete_cards_data[raw_cards_data[index][1]])
                    card_info._options.setMenu(contextMenu)
                    self.getCardsArea().addWidget(card_info, new_row, i)
        else:
            self.getCardsArea().addWidget(self._add_card_icon, 0, 0)
            self.getCardsArea().addWidget(self._add_card_label, 1, 0)
            self._add_card_icon.show()
            self._add_card_label.show()

    def _addCard(self):
        self._showAddCard = AddCards(self, self.deck)
        #inp = io_.SQLiteInput(self.deck)
        #self.cards_data = inp.fetchDataFromDBDeck()
        self._createCardsList()

    def resizeEvent(self, event):
        self.set_deck(self.deck)

    def _deleteCard(self, card):
        print(card)
        db = io_.SQLiteInput(self.deck)
        out = io_.SQLiteOutput(self.deck)
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
        # card = self.getCardsArea().count()
        # print(self.getCardsArea().itemAt(card).widget())
        self._createCardsList()

    def keyPressEvent(self, event):
        print(event.key())
        print(QtCore.Qt.Key_F5)
        if event.key() == QtCore.Qt.Key_F5:
            self._createCardsList()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            menu = QtWidgets.QMenu(self)
            menu.addAction("Refresh").triggered.connect(self._createCardsList)
            # self.setMenu(menu)
            menu.popup(self.mapToGlobal(event.pos()))


class CardInfo(QtWidgets.QGroupBox, Ui__card_info):
    def __init__(self, parent, card_info: tuple, deck=None):
        super().__init__(parent)
        self.card_info = card_info
        self.deck = deck
        self.setupUi(self)
        shadow = QtWidgets.QGraphicsDropShadowEffect(
            blurRadius=20, xOffset=0, yOffset=0)
        shadow.setColor(QtGui.QColor(201, 199, 199))
        self._front.setWordWrap(True)
        self._back.setWordWrap(True)
        self.setGraphicsEffect(shadow)
        self._displayCardInfo()
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self._options.setCursor(QtCore.Qt.PointingHandCursor)

    def _displayCardInfo(self):
        _, front, back, img = self.card_info
        self._front.setText(front)
        self._back.setText(back)
        pixmap = QtGui.QPixmap(img)
        if not pixmap.isNull():
            self._img.setPixmap(pixmap.scaledToWidth(300))
        else:
            self._img.setText("")

    def editCard(self):
        self._editCard = EditCard(self, self.deck, self._front.text())
        self._displayCardInfo()

    def mousePressEvent(self, event):
        self.editCard()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 536)
        self.setWindowTitle("All decks")
        self.setWindowIcon(QtGui.QIcon(str(IMG_DIR) + "/flash.ico"))
        # self.setStyleSheet("background: white;")
        self._stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self._stacked_widget)
        self._browse_decks_widget = BrowseDeck(self._stacked_widget)
        self._stacked_widget.addWidget(self._browse_decks_widget)
        self._flash_mode_widget = FlashMode(self)
        # self._flash_mode_widget.setStyleSheet()
        self._stacked_widget.addWidget(self._flash_mode_widget)
        self._game_mode_widget = GameMode(self)
        self._stacked_widget.addWidget(self._game_mode_widget)
        self._new_cards_list = NewCardsList(self)
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
        self._flash_mode_widget.set_deck(deck)
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


class Settings(QtWidgets.QWidget):
    pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
