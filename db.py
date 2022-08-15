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
            db.SetHeadBlockNumber(49000)
        else:
            print("opened existing db")

        return db

    def createCallTable(self):
        self.cursor.execute('CREATE TABLE calls (blockNumber TEXT, txHash TEXT, txIndex TEXT, recipient TEXT, sender TEXT, input TEXT, output TEXT, gasUsed TEXT, PRIMARY KEY (blockNumber, txHash, txIndex))')
        self.connection.commit()

    def createHeadBlockTable(self):
        self.cursor.execute('CREATE TABLE headblock (id TEXT NOT NULL, number TEXT NOT NULL, PRIMARY KEY (id) )')
        self.connection.commit()

    def SetHeadBlockNumber(self, number: int):
        self.head_number = number
        self.cursor.execute('REPLACE INTO headblock (id, number) values ("headblock", "{}")'.format(number))
        self.connection.commit()
        # TODO self.cursor.execute('....')

    def HeadBlockNumber(self):
        result = self.cursor.execute('SELECT * FROM headblock').fetchall()
        return int(result[0][1])

    def AddPrecompileCalls(self, block_number: int, precompiles_calls):
        pass
