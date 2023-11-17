import sqlite3


class SQLiteModule:
    def __init__(self, base):
        self.base = base
        self.con = sqlite3.connect(self.base)
        self.cursor = self.con.cursor()


    def create(self):
        self.cursor.execute("""CREATE TABLE UserData(user TEXT, email TEXT, url TEXT)""")

    def add(self, values):
        users = self.cursor.execute("SELECT * FROM UserData").fetchall()
        for user in users:
            if values[0] == user[0]:
                return
        values = ["'" + el + "'" for el in values]
        values = ", ".join(values)
        self.cursor.execute(f"INSERT INTO UserData(user, email, url) VALUES ({values})")
        self.con.commit()

    def read(self):
        users = self.cursor.execute("SELECT * FROM UserData").fetchall()
        return users


"""lib = SQLiteModule("users.db")
print(lib.read())"""