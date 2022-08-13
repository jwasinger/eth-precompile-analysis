import sqlite3
import os

DB_NAME='precompiles.db'

class DB():
    def __init__(self):
        pass

    @staticmethod
    def create_or_new():
        already_exists = False
        if os.path.exists(DB_NAME):
            already_exists = True

        db = DB()
        db.connection = sqlite3.connect(DB_NAME)
        db.cursor = db.connection.cursor()

        if not already_exists:
            print("creating new db")
            db.createHeadBlockTable()
            db.createCallTable()
            db.SetHeadBlockNumber(0)
        else:
            print("opened existing db")

        return db

    def createCallTable(self):
        self.cursor.execute('CREATE TABLE CALLS(to TEXT, from TEXT, input TEXT, gasUsed TEXT)')

    def createHeadBlockTable(self):
        self.cursor.execute('CREATE TABLE HEADBLOCK(id TEXT NOT NULL, number TEXT NOT NULL, PRIMARY KEY (id) )')

    def SetHeadBlockNumber(self, number: int):
        self.head_number = number
        self.cursor.execute('INSERT INTO HEADBLOCK ("headblock", {})'.format(number))
        # TODO self.cursor.execute('....')

    def HeadBlockNumber(self):
        result = self.cursor.execute('SELECT * from HEADBLOCK')
        import pdb; pdb.set_trace()

    def SetPrecompileCall(self, block_number: int, tx_hash: str, to: str, input_data: str, result: str, gas_used: int):
        pass
