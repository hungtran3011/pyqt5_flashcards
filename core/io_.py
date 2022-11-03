from shutil import Error
import sqlite3 as sql
import os
from pathlib import Path
import sys
import csv
import json
import defusedxml.ElementTree as ET
import defusedxml.minidom as minidom
from io import BytesIO


ROOT_DIR = Path(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))
IMG_DIR = ROOT_DIR / "../img"
DECKS_DIR = ROOT_DIR / "../decks"

if not os.path.isdir(IMG_DIR):
    IMG_DIR = ROOT_DIR / "img"
if not os.path.isdir(DECKS_DIR):
    DECKS_DIR = ROOT_DIR / "decks"

ADD_DECK_ICON = str(IMG_DIR / "add_deck.svg")
ADD_CARDS_ICON = str(IMG_DIR / "add_cards.svg")


class SQLiteImporter:
    def __init__(self, database):
        # Sometimes can be treated as the deck's name
        self.database = database
        if self.database != "":
            self.file_name = f"{DECKS_DIR}/{self.database}.db"
            print(self.file_name)
            self.conn = sql.connect(self.file_name)
            self.cursor = self.conn.cursor()
        else:
            pass


    def fetch_from_db_Deck(self):
        try:
            self.cursor.execute("SELECT * FROM DECK")
            result = self.cursor.fetchall()
            return result
        except sql.OperationalError:
            os.remove(f"{self.file_name}")
            raise Error("Table DECK not found")
        # This line will be the exception handler for the case when the cursor is not found
        except AttributeError:
            pass

    def fetch_from_db_Date_(self, condition: str = None):
        try:
            if condition is None:
                self.cursor.execute("SELECT * FROM DATE_")
            else:
                self.cursor.execute("SELECT * FROM DATE_ WHERE ?VVV", (condition,))
            result = self.cursor.fetchall()
            return result
        except sql.OperationalError:
            os.remove(f"{self.file_name}")
        except AttributeError:
            pass

    def getImgFile(self):
        try:
            tmp_list = self.fetch_from_db_Deck()
            return tmp_list[3]
        except sql.OperationalError:
            return []
        except AttributeError:
            pass

    def selectFromDBDeck(self, data_request):
        try:
            self.cursor.execute('SELECT * FROM DECK WHERE FRONT = ?', (data_request,))
            return self.cursor.fetchall()
        except AttributeError:
            pass



class SQLiteExporter:
    def __init__(self, database: str):
        self.database = database
        self.file_name = f"{ROOT_DIR}/../decks/{self.database}.db"
        if not os.path.exists(self.file_name):
            self.file_name = f"{ROOT_DIR}/decks/{self.database}.db"
        self.conn = sql.connect(self.file_name)
        self.cursor = self.conn.cursor()

    def writeToDB(self, data, table) -> None:
        if table == "DECK":
            self.cursor.execute("INSERT INTO DECK (ID, FRONT, BACK, IMG) VALUES (?, ?, ?, ?)", data)
            self.conn.commit()
        elif table == "DATE_":
            self.cursor.execute("INSERT INTO DATE_ (ID, CARD, LAST_REVIEW, NEXT_REVIEW) VALUES (?, ?, ?, ?)", data)
            self.conn.commit()

    def createTable(self, name) -> None:
        if name == "DECK":
            self.cursor.execute("CREATE TABLE DECK (ID INT PRIMARY KEY, FRONT TEXT UNIQUE, BACK TEXT, IMG TEXT)")
            self.conn.commit()
        elif name == "DATE_":
            self.cursor.execute(
                "CREATE TABLE DATE_(ID INT PRIMARY KEY, CARD TEXT UNIQUE, LAST_REVIEW DATE, NEXT_REVIEW DATE)")
            self.conn.commit()

    def updateTable(self, table: str, column_to_change: str, data: str, condition: str):
        if table == "DECK":
            if column_to_change == "BACK":
                self.cursor.execute("UPDATE DECK SET BACK = ? WHERE FRONT = ?", (data, condition))
                self.conn.commit()
            elif column_to_change == "IMG":
                self.cursor.execute("UPDATE DECK SET IMG = ? WHERE FRONT = ?", (data, condition))
                self.conn.commit()
            else:
                raise ValueError
        elif table == "DATE_":
            if column_to_change == "LAST_REVIEW":
                self.cursor.execute("UPDATE DATE_ SET LAST_REVIEW = ? WHERE CARD = ?", (data, condition))
                self.conn.commit()
            elif column_to_change == "NEXT_REVIEW":
                self.cursor.execute("UPDATE DATE_ SET NEXT_REVIEW = ? WHERE CARD = ?", (data, condition))
                self.conn.commit()
            else:
                raise ValueError
        else:
            raise ValueError("Table not existed")

    def deleteItem(self, table: str, item: str, ):
        pass


class CSVExporter:
    def __init__(self, raw_data: tuple, output_file: str):
        self.raw_data = raw_data
        self.output_file = self._process_csv_extension(output_file)
        self.output_string = self._convert_csv(self.raw_data)

    def _process_csv_extension(self, output_file):
        return output_file + ".csv" if not output_file.endswith(".csv") else output_file

    def _convert_csv(self, raw_data: tuple):
        return_string = ""
        for data in raw_data:
            tmp_str = ""
            for key, items in enumerate(data):
                tmp_str += str(items)
                tmp_str += ", " if key < len(data) - 1 else ""
            return_string += (tmp_str + "\n")
        print(return_string)
        return return_string

    def _convert_csv_specified(self, raw_data: tuple):
        return_string = ""
        for data in raw_data:
            tmp_str = ""
            for key, items in enumerate(data):
                if key > len(data) - 2:
                    break
                tmp_str += str(items)
                tmp_str += ", " if key < len(data) - 2 else ""
            return_string += (tmp_str + "\n")
        print(return_string)
        return return_string

    def write_to_file(self):
        with open(self.output_file, mode="w+", encoding="utf-8") as file_:
            # file_.write("id, front, back, img\n")
            file_.write(self.output_string)


class CSVImporter:
    def __init__(self, input_file):
        if not input_file.endswith(".csv"):
            raise ValueError("The input file must be a .csv file")
        self.input_file = input_file
        self._parsed_data = self._parse_csv_file()

    def _parse_csv_file(self):
        parsed_data = []
        with open(self.input_file) as file_:
            for data in csv.reader(file_, skipinitialspace=True):
                while len(data) < 4:
                    data.append("")
                parsed_data.append(tuple(data))
        return tuple(parsed_data)

    def get_parsed_data(self):
        return self._parsed_data


class JSONExporter:
    def __init__(self, raw_data: tuple, output_file: str):
        self.raw_data: tuple = raw_data
        self.output_file: str = output_file
        self.output_file = self._process_json_extension(self.output_file)

        self.return_dict = self._generate_dict(self.raw_data)
        print(self.return_dict)

    def _process_json_extension(self, file_name):
        if not file_name.endswith(".json"):
            file_name += ".json"
            assert file_name.endswith(".json") is True
        else:
            pass
        return file_name

    def _generate_dict(self, raw_data: tuple):
        return_dict: dict = {}
        for datum in raw_data:
            return_dict.update(
                {
                    datum[0]: {
                        "front": datum[1],
                        "back": datum[2]
                    }
                }
            )
        return return_dict

    def write_to_file(self):
        with open(self.output_file, mode="w+", encoding='utf-8') as file_:
            json.dump(self.return_dict, file_)


class JSONImporter:
    def __init__(self, input_file: str):
        if not input_file.endswith(".json"):
            raise ValueError("The file name must be a JSON file")
        self.input_file = input_file
        with open(input_file, mode="r", encoding='utf-8') as inp:
            self.input_dict = json.load(inp)
        self.return_list = []
        for datum in self.input_dict.keys():
            tmp_list = [datum, self.input_dict[datum]["front"], self.input_dict[datum]["back"], ""]
            while len(tmp_list) < 4:
                tmp_list.append("")
            self.return_list.append(tmp_list)

    def get_parsed_data(self):
        return tuple(self.return_list)


class XMLExporter:
    def __init__(self, raw_data: tuple, output_file: str):
        self.raw_data = raw_data
        self.output_file = output_file
        self.output_file = self.process_xml_extension(self.output_file)
        root = ET.Element("deck", attrib={"name": output_file[:-4]})
        for data in raw_data:
            card = ET.Element("card")
            id_ = ET.SubElement(card, "id")
            id_.text = str(data[0])
            front = ET.SubElement(card, "front")
            front.text = data[1]
            back = ET.SubElement(card, 'back')
            back.text = data[2]
            root.append(card)
        buf = BytesIO()
        buf.write(ET.tostring(root))
        buf.seek(0)
        string = minidom.parse(buf).toprettyxml(indent=" " * 4)
        with open(self.output_file, mode="w+", encoding="utf-8") as file_:
            file_.write(string)

    def process_xml_extension(self, file_name):
        return file_name + ".xml" if not file_name.endswith(".xml") else file_name


class XMLImporter:
    def __init__(self, input_file):
        if not input_file.endswith(".xml"):
            raise ValueError("The input file must be a .xml file")
        self.input_file = input_file
        self._cards_list = self.parse_xml(self.input_file)

    def parse_xml(self, input_file):
        tree = ET.parse(input_file)
        root = tree.getroot()
        cards_list = []
        for card in root.iter("card"):
            tmp_list = []
            for child in list(card):
                # print(ET.tostring(child))
                print(child.text)
                tmp_list.append(child.text)
            while len(tmp_list) < 4:
                tmp_list.append("")
            cards_list.append(tuple(tmp_list))
        cards_list = tuple(cards_list)
        return cards_list

    def get_parsed_data(self):
        return self._cards_list
