import sqlite3


class DBConnector:
    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect('shiftDB.db')
        self.cursor = self.connection.cursor()
        try:
            self.cursor.executescript('''
            CREATE TABLE shifts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shift_name TEXT,
                shift_time TEXT,
                user TEXT);''')
        except sqlite3.Error:
            print("Database already exists, continuing without creating")

    def insert_shift(self, shift_name, shift_time, username):
        try:
            self.cursor.execute('INSERT INTO shifts(shift_name, shift_time, '
                                'user) VALUES (?,?,?);', [shift_name,
                                                          shift_time,
                                                          username])
        except sqlite3.Error:
            print(sqlite3.Error.__traceback__)


class Search:
    def __init__(self):
        self.db = DBConnector()
        self.shift = None
        self.currentTime = None
        self.textNumber = None
        self.replyDateTime = None

    def run(self):
        self.search_db()
        self.send_text()

    def search_db(self, username):
        query = 'SELECT * from shifts WHERE user=?'
        self.db.cursor.execute(query, username)
        results = self.db.cursor.fetchall()
        for row in results:
            print(row)

    def send_text(self):
        #TODO: Make this method send a text message to the supplied number
        #TODO: if it finds a shift that needs to be sent
        pass

