import sqlite3


class Database:
    def __init__(self, name='database.db'):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.text_factory = str
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()