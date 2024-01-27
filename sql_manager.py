import sqlite3


class Database:
    def __init__(self, name='database.db'):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()
        self.query("""
CREATE TABLE IF NOT EXISTS "settings" (
"volume"	INTEGER DEFAULT 50,
"level"	INTEGER DEFAULT 1
);""")
        if not len(self.get_settings()):
            self.query("INSERT INTO settings ('volume', 'level') VALUES (50, 1)")

    def get_settings(self):
        return self.query("SELECT * FROM settings")[0]

    def save_settings(self, volume, level):
        self.query(f"UPDATE settings SET 'volume' = {volume}, 'level' = {level};")

    def query(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        self.connection.text_factory = str
        return self.cursor.fetchall()

    def __del__(self):
        self.connection.close()


if __name__ == "__main__":
    print(Database().get_settings())