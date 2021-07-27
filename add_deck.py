import os
import sys
from pathlib import Path
from platform import system 
from datetime import date

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg

from ui_package.ui_new_add_deck import Ui_new_add_deck

import io_
from rename_deck import RenameDeck

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
SYSTEM = system()
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"
ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")

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
                    os.chdir(f"{IMG_DIR}")
                    os.mkdir(f"{IMG_DIR}/{name}")
                    del out
                    self.close()
                else:
                    self._send_message(f"""Can't add new deck. Please try a different name.
    Note: Don't use these characters: {", ".join(restricted_chars)}""")
            else:
                self._send_message(
                    f"""The deck {name} has been existed""")
        if self.importing_radiobutton.isChecked() is True and self.file_obj[0] != "":
            try:
                open(file_name, "a+").close()
                output = io_.SQLiteOutput(name)
                for card in self.parsed_data:
                    output.writeToDB(card, "DECK")
                    output.writeToDB(
                        (card[0], card[1], None, date.today()),
                         "DATE_"
                    )
                self.close()
            except:
                self._send_message("Error in importing file(s)")
        elif self.importing_radiobutton.isChecked() is True and self.file_obj[0] == "":
            self._send_message("The name of the imported file must not be blank")
        else:
            pass

    # def mousePressEvent(self, event):
    #     window.setNewCardsList(self.deck)