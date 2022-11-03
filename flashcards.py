#!/usr/bin/env python3
"""
This is the main script of the project, where the main window and the components communicating 
and interacting on each other.
The structure of the project can be quite confusing despite my efforts to make it clear. It's
very kind of you to help me out with the way of structuring the code - in an effective way 
"""

import shutil
import sys
import os
# from platform import system
from pathlib import Path

from PyQt5 import QtGui, QtWidgets, QtCore

from core.browse_deck import BrowseDeck
from core.flashcards_mode import FlashcardsMode
from core.game_mode import GameMode
from core.new_cards_list import NewCardsList
from core.add_deck import AddDeck
from core.settings import Settings
from core.export_deck import ExportDeck

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
# SYSTEM = system()
IMG_DIR = ROOT_DIR / "img"
DECKS_DIR = ROOT_DIR / "decks"

if not os.path.isdir(IMG_DIR):
    os.mkdir(IMG_DIR)
if not os.path.isdir(DECKS_DIR):
    os.mkdir(DECKS_DIR)

ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(600, 536)
        self.setWindowTitle("All decks")
        self.setWindowIcon(QtGui.QIcon(str(IMG_DIR) + "/flash.ico"))
        self._stacked_widget = QtWidgets.QStackedWidget(self)
        self.setCentralWidget(self._stacked_widget)
        self._browse_decks_widget = self.ModifiedBrowseDeck(self)
        self._stacked_widget.addWidget(self._browse_decks_widget)
        self._flash_mode_widget = self.ModifiedFlashcardsMode(self)
        self._stacked_widget.addWidget(self._flash_mode_widget)
        self._game_mode_widget = self.ModifiedGameMode(self)
        self._stacked_widget.addWidget(self._game_mode_widget)
        self._new_cards_list = self.ModifiedNewCardsList(self)
        self._stacked_widget.addWidget(self._new_cards_list)
        self._stacked_widget.setCurrentWidget(self._browse_decks_widget)
        self.adjustSize()

    def get_browse_decks_widget(self):
        return self._browse_decks_widget

    def set_browse_decks_mode(self):
        self._stacked_widget.setCurrentWidget(self._browse_decks_widget)
        self.setWindowTitle("All decks")
        self._browse_decks_widget.show_all_decks()

    def set_flashcards_mode(self, deck):
        self._stacked_widget.setCurrentWidget(self._flash_mode_widget)
        self._flash_mode_widget.modified_set_deck(deck)
        print(self._flash_mode_widget.deck)
        self.setWindowTitle(f"Flashcards mode from deck: {deck}")

    def set_game_mode(self, deck):
        self._stacked_widget.setCurrentWidget(self._game_mode_widget)
        try:
            self._game_mode_widget.set_deck(deck)
            self.setWindowTitle(f"Practice mode/ Game mode for deck: {deck}")
        except ValueError:
            self.set_new_cards_list(deck)

    def set_new_cards_list(self, deck):
        self._stacked_widget.setCurrentWidget(self._new_cards_list)
        self._new_cards_list.set_deck(deck)
        self.setWindowTitle(f"Cards list from deck: {deck}")

    def resizeEvent(self, event: QtGui.QResizeEvent = None) -> None:
        print(self.height())

    class ModifiedBrowseDeck(BrowseDeck):
        """
        Modified browse deck widget from browse_deck.py:
        Add some method to communicate with MainWindow - the wrapping widget
        """
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent)
            self._main_window_widget: MainWindow = parent
            self._add_deck.clicked.connect(self.show_add_deck_popup)
            try:
                self.show_all_decks()
            except ZeroDivisionError:
                pass

        def resizeEvent(self, event):
            self.show_all_decks()

        def show_add_deck_popup(self, event=None):
            _dialog_add_deck = AddDeck(self)
            self.show_all_decks()

        def show_flashcards_mode(self, deck):
            self._main_window_widget.set_flashcards_mode(deck)

        def show_game_mode(self, deck):
            self._main_window_widget.set_game_mode(deck)

        def show_view_cards_mode(self, deck):
            self._main_window_widget.set_new_cards_list(deck)

        def delete_deck(self, name):
            try:
                file_name = f"{DECKS_DIR}/{name}.db"
                os.remove(file_name)
                img_folder_name = f"{IMG_DIR}/{name}"
                shutil.rmtree(img_folder_name)
            except FileNotFoundError:
                pass
            self.show_all_decks()

        def _create_function_menu(self):
            function_menu = QtWidgets.QMenu(self._more_funcs)
            function_menu.setStyleSheet(
                """
                QMenu {
                            background: white;
                            border-radius: 5px;
                            padding: 4px;
                            border: 1px solid #d3d3d3
                        }

                        QMenu::item {
                            /* sets background of menu item. set this to something non-transparent
                                if you want menu color and menu item color to be different */
                            background-color: white;
                            border-radius: 5px;
                            padding: 4px;
                        }

                        QMenu::item:selected { /* when user selects item using mouse or keyboard */
                            background-color: #91e67b;
                            color: white;\n
                        }
                """
            )
            settings = function_menu.addAction("Settings...")
            settings.triggered.connect(self.show_settings)
            self._more_funcs.setMenu(function_menu)
        
        def show_settings(self):
            settings_dialog = self._main_window_widget.ModifiedSettings(self)
            settings_dialog.exec()

        class DeckInfo(BrowseDeck.DeckInfo):
            def __init__(self, parent, deck, *args, **kwargs):
                super().__init__(parent, deck)
                self.parent_widget: MainWindow.ModifiedBrowseDeck = parent
                self.deck = deck
                self._game_mode.clicked.connect(self.show_game_mode)
                self._view_cards_list.clicked.connect(self.show_view_cards_mode)
                self._flash_mode.clicked.connect(self.show_flashcards_mode)
                self._context_menu = QtWidgets.QMenu()
                self._context_menu.setWindowFlags(self._context_menu.windowFlags() | QtCore.Qt.FramelessWindowHint)
                self._context_menu.setStyleSheet(
                """
                    QMenu {
                        background: white;
                        border-radius: 5px;
                        padding: 4px;
                        border: 1px solid #d3d3d3;
                        margin: 0;
                    }

                    QMenu::item {
                        /* sets background of menu item. set this to something non-transparent
                            if you want menu color and menu item color to be different */
                        background-color: none;
                        border-radius: 5px;
                        padding: 4px;
                    }

                    QMenu::item:selected { /* when user selects item using mouse or keyboard */
                        background-color: #91e67b;
                        color: white;\n
                    }
                """
                )
                self._context_menu.addAction("Delete this deck").triggered.connect(lambda: self.delete_deck(self.getDeckName()))
                self._context_menu.addAction("Rename this deck").triggered.connect(self.renameDeck)
                self._context_menu.addAction("Export cards").triggered.connect(self.export_deck)
                self._more_funcs.setMenu(self._context_menu)
                self._more_funcs.setPopupMode(QtWidgets.QToolButton.InstantPopup)

            def show_flashcards_mode(self):
                self.parent_widget.show_flashcards_mode(self.deck)

            def show_game_mode(self):
                self.parent_widget.show_game_mode(self.deck)

            def show_view_cards_mode(self):
                self.parent_widget.show_view_cards_mode(self.deck)

            def delete_deck(self, name):
                self.parent_widget.delete_deck(name)

            def rename_deck(self):
                self.renameDeck()
                self.parent_widget.show_all_decks()

            def export_deck(self):
                export_dialog = QtWidgets.QFileDialog(self)
                file_name, ext = export_dialog.getSaveFileName(
                    directory=f"~/Documents/{self.deck}", 
                    filter="CSV Files (*.csv);; JSON Files (*.json);; XML Files (*.xml)"
                )

    class ModifiedNewCardsList(NewCardsList):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent)
            self._main_window_widget: MainWindow = parent
            self._back.clicked.connect(self._back_home)

        def _back_home(self):
            self._main_window_widget.set_browse_decks_mode()

    class ModifiedGameMode(GameMode):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent)
            self._main_window_widget: MainWindow = parent
            self.back_button.clicked.connect(self.back)
            self.next_question_button.clicked.connect(self.next_question)

        def back(self):
            self.reset()
            self._main_window_widget.set_browse_decks_mode()
            self.click_audio.play()

        def next_question(self):
            self.click_audio.play()
            if self.question_num < len(self.questions_list) - 1:
                self.question_num += 1
                self.show_game_progress(int(self.question_num / len(self.questions_list) * 100))
                self.show_questions(self.question_num)
            else:
                self.show_game_progress(int(self.question_num / len(self.questions_list) * 100))
                self.end_test()

        def end_test(self):
            self._main_window_widget.set_browse_decks_mode()
            self.send_message(f"Congrats! You've finished the game \n Your score: {self.score_} \
            / {len(self.questions_list) * 10}", type="congratulations")
            self.congrats_audio.play()
            super().end_test()

    class ModifiedFlashcardsMode(FlashcardsMode):
        def __init__(self, parent, *args, **kwargs):
            super().__init__(parent)
            self._main_window_widget: MainWindow = parent
            self._practice.clicked.connect(self._practice_deck)

        def modified_configure_widgets(self):
            self._back.clicked.connect(self._main_window_widget.set_browse_decks_mode)
            self._practice.clicked.connect(self._practice_deck)
            self.configureWidgets()

        def modified_set_deck(self, deck, event=None):
            self.set_deck(deck)
            self.modified_configure_widgets()

        def _practice_deck(self):
            self._main_window_widget.set_game_mode(self.deck)

        def back(self):
            self._main_window_widget.setBrowseDeckMode()

    class ModifiedSettings(Settings):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
    