from PyQt5 import QtGui, QtCore, QtWidgets

from core.ui_package.ui_game_mode import Ui_game_mode
import core.io_ as io_

class GameMode(QtWidgets.QWidget, Ui_game_mode):
    def __init__(self, parent, deck=None):
        super().__init__(parent)
        self.deck = deck
        self.setupUi(self)
        self._right_answer = ""
        self.back_button.clicked.connect(self.back)
        self.button_A.clicked.connect(lambda: self.multiple_choice_check("A"))
        self.button_B.clicked.connect(lambda: self.multiple_choice_check("B"))
        self.button_C.clicked.connect(lambda: self.multiple_choice_check("C"))
        self.button_D.clicked.connect(lambda: self.multiple_choice_check("D"))
        self.submit.clicked.connect(self.writing_check)

    def set_deck(self, deck):
        self._deck = deck
        cards_list = io_.SQLiteInput(self.deck)
        self.showQuestions(cards_list)

    def createQuestion(self, cards_list: dict, mode):
        if mode == "multiple":
            pass
        elif mode == "writing":
            pass
        else:
            pass

    def showQuestion(self):
        pass

    def writing_check(self):
        self.calculate_score()
        self.next_question()

    def multiple_choice_check(self, answer):
        print(f"Pressed answer: {answer}")
        self.next_question()
        self.calculate_score()

    def next_question(self):
        pass

    def calculate_score(self):
        pass

    #Optional: calculate time
    def calculate_time(self):
        pass

    def end_test(self):
        self.record_learning_process()

    def record_learning_process(self):
        pass