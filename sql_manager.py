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
        self.query("""
        CREATE TABLE IF NOT EXISTS stats (
    attempt INTEGER UNIQUE
                    NOT NULL,
    result  INTEGER NOT NULL
);
""")
        if not len(self.get_settings()):
            self.query("INSERT INTO settings ('volume', 'level') VALUES (50, 1)")

    def get_settings(self):
        return self.query("SELECT * FROM settings")[0]

    def get_stats(self):
        return self.query("SELECT * FROM stats")

    def get_attempts(self):
        return [i[0] for i in self.query("SELECT attempt FROM stats")]

    def set_stats(self, attempt=1, result=3):
        if attempt in self.get_attempts():
            self.query(f"UPDATE stats SET 'result'={result} WHERE 'attempt' = {attempt}")
        else:
            self.query(f"INSERT INTO stats ('attempt', 'result') VALUES ({attempt}, {result})")

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
    print(Database().set_stats(8, 16))
    print(Database().get_difficulty())
