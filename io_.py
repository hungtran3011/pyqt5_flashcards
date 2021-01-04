import sqlite3 as sql
import os
from pathlib import Path
import sys

ROOT_DIR = Path(getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))))

class Input:
    def __init__(self, database):
        # Sometimes can be treated as the deck's name
        self.database = database
        file_name = f"{ROOT_DIR}/decks/{self.database}.db"
        self.conn = sql.connect(file_name)
        self.cursor = self.conn.cursor()


    def fetchDataFromDBDeck(self):
        try:
            self.cursor.execute("SELECT * FROM DECK")
            result = self.cursor.fetchall()
            return result
        except:
            return []

    def fetchDataFromDBDate_(self, condition:str=None):
        if condition == None:
            self.cursor.execute("SELECT * FROM DATE_")
        else:
            self.cursor.execute("SELECT * FROM DATE_ WHERE" + condition)
        result = self.cursor.fetchall()
        return result

    def getImgFile(self):
        try:
            tmp_list = self.fetchDataFromDBDeck()
            return tmp_list[3]
        except:
            return []

    def selectFromDBDeck(self, col_name, data_request):
        self.cursor.execute(f'SELECT * FROM DECK WHERE {col_name} = ?', (data_request,))
        return self.cursor.fetchall()


class Output:
    def __init__(self, database: str):
        self.database = database
        self.conn = sql.connect(f"{ROOT_DIR}/decks/{self.database}.db")
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
            self.cursor.execute("CREATE TABLE DATE_(ID INT PRIMARY KEY, CARD TEXT UNIQUE, LAST_REVIEW DATE, NEXT_REVIEW DATE)")
            self.conn.commit()

    def updateTable(self, table:str, column_to_change:str, data:str, condition:str):
        # The 'condition' argument requires a SQLite condition
        # E.g: FRONT = "text", ID > 1, etc.
        self.cursor.execute(f"UPDATE {table} SET {column_to_change} = ? WHERE " + condition, (data,))
        self.conn.commit()

    def deleteItem(self, table: str, item: str, ):
        pass