import pymysql


class ConnectDB():
    def __init__(self, host, user, password):
        self.host, self.user, self.password = host, user, password
        self.conn = pymysql.connect(host=host, user=user, password=password)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.conn.close()

    def create_table(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS cheese_project")
        self.cursor.execute("USE cheese_project")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS words(
            id INT NOT NULL AUTO_INCREMENT,
            word VARCHAR(100) NOT NULL,
            meaning VARCHAR(250),
            PRIMARY KEY(id));
            """)
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS subtitle(
            id INT NOT NULL AUTO_INCREMENT,
            percent FLOAT NOT NULL,
            count_words INT NOT NULL,
            PRIMARY KEY(id));
            """)

    def insert_words_table(self, word, meanings):
        meaning = ", ".join(meanings)
        sql = """INSERT INTO words(word, meaning) SELECT %s, %s FROM dual\
        WHERE NOT EXISTS (SELECT * FROM words where word=%s);"""
        val = (word, meaning, word)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def insert_subdata_table(self, percent, words):
        sql = """INSERT INTO subtitle(percent, count_words)\
        VALUES(%s, %s)"""
        val = (percent, words)
        self.cursor.execute(sql, val)
        self.conn.commit()

    def search_exiting_dict(self, word):
        sql = "SELECT word, meaning FROM words WHERE word=%s"
        val = (word)
        self.cursor.execute(sql, val)
        result_word = self.cursor.fetchone()
        return result_word
