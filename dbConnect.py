import sqlite3

class DbConnect:

    def __init__(self) -> None:
        self.db = sqlite3.connect('./ratings.db',)
        self.cursor = self.db.cursor()
        self.cursor.execute('pragma foreign_keys = on')

    def close(self) -> None:
        self.db.commit()
        self.cursor.close()

    def hasAdmins(self):
        self.cursor.execute('''select count(*) from usuario
                               where administrador = 1''')
        return self.cursor.fetchall()[0][0]