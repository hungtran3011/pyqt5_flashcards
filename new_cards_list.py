import os
import sys
import shutil
from pathlib import Path
import functools


from PyQt5 import QtGui, QtWidgets, QtCore, QtSvg
from ui_package.ui_new_cards_list import Ui__new_cards_list
from ui_package.ui_edit_card import Ui__edit_card
from ui_package.ui_card_info import Ui__card_info

import io_
from add_cards import AddCards

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"

ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")

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

    def _createCardsList(self):
        """
        Generate cards list from local database
        "Cards" a.k.a customized groupboxes are placed in grid layout
        inside a QScrollArea
        Responsive layout is implemented in this method, but needs some improvement
        (e.g smooth and faster arrange the 'cards') 
        """
        inp = io_.SQLiteInput(self.deck)
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
            for card in reversed(range(self.getCardsArea().count())):
                tmp_widget = self.getCardsArea().itemAt(card).widget()
                self.getCardsArea().removeWidget(tmp_widget)
                tmp_widget.setParent(None)
                tmp_widget.deleteLater()
            self.getCardsArea().addWidget(self._add_card_icon, 0, 0)
            self.getCardsArea().addWidget(self._add_card_label, 1, 0)
            self._add_card_icon.show()
            self._add_card_label.show()

    def _addCard(self):
        self._showAddCard = AddCards(self, self.deck)
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