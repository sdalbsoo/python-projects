import pymysql


class ConnectDB():
    def __init__(self, host, user, password):
        self.conn = pymysql.connect(host=host, user=user, password=password)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

    def create_table(self):
        with open("./schema.sql", "r") as f:
            stripped_lines = [s.rstrip() for s in f.readlines()]
            for command_line in stripped_lines:
                self.cursor.execute(command_line)

    def insert_words_table(self, word, meanings):
        self.cursor.execute("USE cheese_project")
        meaning = ", ".join(meanings)
        sql = """INSERT INTO words(word, meaning) SELECT %s, %s FROM dual\
        WHERE NOT EXISTS (SELECT * FROM words where word=%s);"""
        val = (word, meaning, word)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def insert_subdata_table(self, percent, words):
        self.cursor.execute("USE cheese_project")
        sql = """INSERT INTO subtitle(percent, count_words)\
        VALUES(%s, %s)"""
        val = (percent, words)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def search_exiting_dict(self, word):
        self.cursor.execute("USE cheese_project")
        sql = "SELECT word, meaning FROM words WHERE word=%s"
        val = (word)
        self.cursor.execute(sql, val)
        result_word = self.cursor.fetchone()
        return result_word
