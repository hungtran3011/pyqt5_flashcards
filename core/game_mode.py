import os
from pathlib import Path
import sys
from PyQt5 import QtGui, QtWidgets, QtCore, QtMultimedia
import random as rand
from datetime import date, datetime, timedelta

from core.ui_package.ui_game_mode import Ui_game_mode
import core.io_ as io_

ROOT_DIR = Path(
    getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
)
IMG_DIR = ROOT_DIR / "../img"
DECKS_DIR = ROOT_DIR / "../decks"
AUDIO_DIR = ROOT_DIR / "../audio"
print(AUDIO_DIR)
print("AUDIO_DIR:", os.path.isdir(str(AUDIO_DIR)))
if not (os.path.isdir(str(IMG_DIR)) \
    and os.path.isdir(str(DECKS_DIR) \
    and os.path.isdir(str(AUDIO_DIR))
    )):
    IMG_DIR = ROOT_DIR / "img"
    DECKS_DIR = ROOT_DIR / "decks"
    AUDIO_DIR = ROOT_DIR / "audio"

class GameMode(QtWidgets.QWidget, Ui_game_mode):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self._right_answer = ""
        self.questions_list: list = []
        self.question_num = 0
        self.question = {}
        self.cards_status = {}
        self.score_ = 0
        self.false_answer_list = []
        correct_audio_link = QtCore.QUrl.fromLocalFile(f"{AUDIO_DIR}/correct.wav")
        wrong_audio_link = QtCore.QUrl.fromLocalFile(f"{AUDIO_DIR}/wrong.wav")
        click_audio_link = QtCore.QUrl.fromLocalFile(f"{AUDIO_DIR}/click.wav")
        congrats_audio_link = QtCore.QUrl.fromLocalFile(f"{AUDIO_DIR}/congratulations.mp3")
        self.correct_audio = QtMultimedia.QMediaPlayer()
        self.correct_audio.setMedia(QtMultimedia.QMediaContent(correct_audio_link))
        self.wrong_audio = QtMultimedia.QMediaPlayer()
        self.wrong_audio.setMedia(QtMultimedia.QMediaContent(wrong_audio_link))
        # self.correct_audio = QtMultimedia.QSoundEffect()
        # self.correct_audio.setSource(correct_audio_link)
        # self.wrong_audio = QtMultimedia.QSoundEffect()
        # self.wrong_audio.setSource(wrong_audio_link)
        self.click_audio = QtMultimedia.QMediaPlayer()
        self.click_audio.setMedia(QtMultimedia.QMediaContent(click_audio_link))
        self.congrats_audio = QtMultimedia.QMediaPlayer()
        self.congrats_audio.setMedia(QtMultimedia.QMediaContent(congrats_audio_link))
        self.back_button.clicked.connect(self.back)
        self.button_A.clicked.connect(lambda: self.check_answers(self.button_A.text(), mode="multiple", button_clicked=self.button_A))
        self.button_B.clicked.connect(lambda: self.check_answers(self.button_B.text(), mode="multiple", button_clicked=self.button_B))
        self.button_C.clicked.connect(lambda: self.check_answers(self.button_C.text(), mode="multiple", button_clicked=self.button_C))
        self.button_D.clicked.connect(lambda: self.check_answers(self.button_D.text(), mode="multiple", button_clicked=self.button_D))
        self.submit.clicked.connect(lambda: self.check_answers(self.answer_box.toPlainText().strip(" "), mode="writing"))
        # self.next_question_button.clicked.connect(self.next_question)
        self.show_game_progress(0)

    def set_deck(self, deck):
        self.deck = deck
        importer = io_.SQLiteImporter(self.deck)
        tmp_cards_list = importer.fetch_from_db_Deck()
        cards_data: dict = {}
        for card in tmp_cards_list:
            cards_data.update(
                {
                    card[1]: {
                        "back": card[2],
                        "img": card[3]
                    }
                    
                }
            )
        date_data = importer.fetch_from_db_Date_()
        # if len(tmp_cards_list) >= 5:
        self.cards_list = {}
        for item in date_data:
            # print(item)
            if datetime.strptime(item[3], "%Y-%m-%d") <= datetime.today():
                front = item[1]
                self.cards_list.update(
                    {
                        front: 
                        {
                            "back": cards_data[front]["back"],
                            "img": cards_data[front]["img"]
                        }
                    }
                )
        # print("card_list: ", cards_list)     
        init_question = self.create_question(self.cards_list)
        if init_question:
            self.show_questions(self.question_num)
            # self.send_message("The deck must have at least 5 cards to play games")
            # raise ValueError("The deck must have at least 5 cards to play games")

    def create_question(self, cards_list: dict):
        multiple_choice = []
        writing = []
        front_list = tuple(cards_list.keys())
        back_list = list(cards_list.keys())
        # print(front_list)
        if len(front_list) == 0:
            for i in 'ABCD':
                eval(f"self.button_{i}.setEnabled(False)")
            self.send_message(text="There is no card to learn today", type="information")
            return 0
        else:
            for i in 'ABCD':
                eval(f"self.button_{i}.setEnabled(True)")
            for card in front_list:
                back_and_img = cards_list[card]
                back = back_and_img["back"]
                img = back_and_img["img"]
                multiple_question_answers = [card]
                writing.append(
                    {
                        "mode": "writing",
                        "question": back,
                        "right answer": card,
                        "img": img,
                    }
                )
                if len(front_list) >= 4:
                    while len(multiple_question_answers) < 4:
                        if (random_answer := rand.choice(front_list)) not in multiple_question_answers:
                            multiple_question_answers.append(random_answer)
                    rand.shuffle(multiple_question_answers)
                else:
                    multiple_question_answers = back_list.copy()
                    rand.shuffle(multiple_question_answers)
                    while len(multiple_question_answers) < 4:
                        multiple_question_answers.append("")
                multiple_choice.append(
                    {
                        "mode": "multiple choice",
                        "question": back,
                        "answer list": multiple_question_answers,
                        "right answer": card,
                        "img": img
                    }
                )
                self.cards_status.update(
                    {
                        card: {
                            "writing": False,
                            "multiple choice": False
                        }
                    }   
                )
            self.questions_list = multiple_choice + writing
            rand.shuffle(self.questions_list)
            return 1
            # with open(f"{ROOT_DIR}/../question_list.txt") as file_:
            #     file_.writelines(str(self.questions_list))

    def show_questions(self, num):
        print(num)
        self.question = self.questions_list[num]
        print(self.question)
        self.true_answer_label.setText("")
        self.answer_box.clear()
        self.next_question_button.setEnabled(False)
        self.submit.setEnabled(True)
        assert type(self.questions_list) == list
        assert type(self.question) == dict
        if self.question["mode"] == "writing":
            self.question_widget.setCurrentWidget(self.writing_widget)
            self.question_label.setText(self.question["question"])
            self.question_type_label.setText("Type the right answer")
            # print(self.question["img"])
            pixmap = QtGui.QPixmap(self.question["img"])
            if not pixmap.isNull():
                pixmap.scaledToHeight(100)
                self.question_img.setPixmap(pixmap)
            else:
                pixmap = QtGui.QPixmap(f"{IMG_DIR}/dull_image.png")
                pixmap.scaledToHeight(100)
                self.question_img.setPixmap(pixmap)
        elif self.question["mode"] == "multiple choice":
            self.question_widget.setCurrentWidget(self.multiple_widget)
            self.question_label.setText(self.question["question"])
            self.question_type_label.setText("Choose the right answer")
            pixmap = QtGui.QPixmap(self.question["img"])
            if not pixmap.isNull():
                pixmap.scaledToHeight(100)
                self.question_img.setPixmap(pixmap)
            else:
                pixmap = QtGui.QPixmap(f"{IMG_DIR}/dull_image.png")
                pixmap.scaledToHeight(100)
                self.question_img.setPixmap(pixmap)
            self.button_A.setText(f"A. {self.question['answer list'][0]}")
            self.button_A.setStyleSheet(
            """
                QPushButton{
                    background: #d3d3d3;
                }

                QPushButton:hover{
                    background: rgb(157, 157, 157);
                    color: white;
                } 
            """ 
            )
            self.button_B.setText(f"B. {self.question['answer list'][1]}")
            self.button_B.setStyleSheet(
            """
                QPushButton{
                    background: #d3d3d3;
                }

                QPushButton:hover{
                    background: rgb(157, 157, 157);
                    color: white;
                } 
            """
            )
            self.button_C.setText(f"C. {self.question['answer list'][2]}")
            self.button_C.setStyleSheet(
            """
                QPushButton{
                    background: #d3d3d3;
                }

                QPushButton:hover{
                    background: rgb(157, 157, 157);
                    color: white;
                } 
            """
            )
            self.button_D.setText(f"D. {self.question['answer list'][3]}")
            self.button_D.setStyleSheet(
            """
                QPushButton{
                    background: #d3d3d3;
                }

                QPushButton:hover{
                    background: rgb(157, 157, 157);
                    color: white;
                } 
            """
            )
        else:
            raise ValueError("Injected")
        self.answer_box.setStyleSheet(
            """
            background-color: #d3d3d3;
            padding: 5px;
            border-radius: 5px;
            """
        )
    
    def check_answers(self, answer, mode, button_clicked:QtWidgets.QPushButton=None):
        def writing_check(answer):
            self.submit.setEnabled(False)
            right_answer = self.question["right answer"].strip()
            answer_to_check = answer.strip()
            if right_answer == answer_to_check:
                self.answer_box.setStyleSheet(
                    """
                    background-color: #91e67b;
                    padding: 5px;
                    border-radius: 5px;
                    """
                )
                answer_status = True
                # print(self.correct_audio.status())
                self.correct_audio.play()
            else:
                self.answer_box.setStyleSheet(
                    """
                    background-color: #f0422b;
                    padding: 5px;
                    border-radius: 5px;
                    """
                )
                answer_status = False
                # print(self.wrong_audio.status())
                self.wrong_audio.play()
            self.true_answer_label.setText(f"Correct answer: {right_answer}")
            self.cards_status[self.question["right answer"]]["writing"] = answer_status
            self.calculate_score(answer_status)
            # self.next_question()

        def multiple_choice_check(answer, button_clicked:QtWidgets.QPushButton):
            # print(f"Pressed answer: {answer}")
            right_answer = self.question["right answer"]
            answer_to_check = answer[3:]
            answer_status = True
            if answer_to_check == right_answer:
                button_clicked.setStyleSheet(
                    """
                    QPushButton{
                        background-color: #91e67b;
                    }
                    """
                )
                answer_status = True
                # print(self.correct_audio.status())
                self.correct_audio.play()
            else:
                button_clicked.setStyleSheet(
                    """
                    QPushButton {
                        background-color: #f0422b;
                    }
                    """
                )
                answer_status = False
                # print(self.wrong_audio.status())
                self.wrong_audio.play()
            self.true_answer_label.setText(f"Correct answer: {right_answer}")
            self.cards_status[self.question["right answer"]]["multiple choice"] = answer_status
            self.calculate_score(answer_status)
            # self.next_question()

        if mode == "multiple":
            multiple_choice_check(answer, button_clicked)
            self.next_question_button.setEnabled(True)
        elif mode == "writing":
            writing_check(answer)
            self.next_question_button.setEnabled(True)
        else:
            raise ValueError("'mode' argument must be one of two values: 'multiple' or 'writing'")


    # def next_question(self):
    #     self.show_game_progress(int((self.question_num + 1) / len(self.questions_list) * 100))

    def calculate_score(self, true_or_false: bool):
        score = 0
        if true_or_false is True:
            score = 10
        self.score_ += score
        self.score.setText(str(self.score_))

    def send_message(self, text, type):
        message = QtWidgets.QMessageBox(self)
        if type == "warning":
            message.setIcon(QtWidgets.QMessageBox.Warning)
        elif type == "information":
            message.setIcon(QtWidgets.QMessageBox.Information)
        elif type == "no icon":
            message.setIcon(QtWidgets.QMessageBox.NoIcon)
        elif type =="question":
            message.setIcon(QtWidgets.QMessageBox.Question)
        elif type == "critical":
            message.setIcon(QtWidgets.QMessageBox.Critical)
        elif type in ["congratulations", "congrats"]:
            pixmap = QtGui.QPixmap(f"{IMG_DIR}/congrats.png")
            pixmap.scaledToHeight(32)
            message.setIconPixmap(pixmap)
            font = QtGui.QFont()
            font.setPointSize(15)
            message.setFont(font)
        else:
            raise ValueError("The 'type' arguments just accept these str values: \
                'warning', 'information', 'no icon', 'question' and 'critical'")
        message.setText(text)
        message.exec()

    #Optional: calculate time
    def calculate_time(self):
        pass

    def end_test(self):
        # print(self.cards_status)
        self.record_learning_process()

    def record_learning_process(self):
        exporter = io_.SQLiteExporter(self.deck)
        importer = io_.SQLiteImporter(self.deck)
        # date_ = importer.fetch_from_db_Date_()
        for item in self.cards_list.keys():
            card = item
            status = self.cards_status[card]
            last_review = date.today()
            next_review = date.today()
            if status["writing"] and status["multiple choice"]:
                print(f"{card}: 2/2")
                next_review += timedelta(days=5)
            elif status["writing"] or status["multiple choice"]:
                print(f"{card}: 1/2")
                next_review += timedelta(days=1)
            else:
                print(f"{card}: 0/2")
                next_review += timedelta(days=0)
            exporter.updateTable(
                table="DATE_", column_to_change="LAST_REVIEW",
                data=last_review, condition=card
            )
            exporter.updateTable(
                table="DATE_", column_to_change="NEXT_REVIEW",
                data=next_review, condition=card
            )
        # for card in self.cards_status.keys():
        #     # print(card)
        #     # print(self.cards_status[card])
        #     status = self.cards_status[card]
            

    def show_game_progress(self, percent):
        self.game_progress.setValue(percent)

    def reset(self):
        self.question_num = 0
        self.score_ = 0
        self.show_game_progress(0)
        # self.create_question()
        self.score.setText(str(self.score_))
        self.show_questions(self.question_num)