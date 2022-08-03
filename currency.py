import db_sqlite as db

class Currency:
    def __init__(self):
        self.id = None
        self.code = None
        self.name = None
        self.symbol = None


    def load_by_id(self, id):
        conn = db.create_connection("database.db")
        p = db.currency_select_by_id(conn, id)
        self.id = p[0][0]
        self.code = p[0][1]
        self.name = p[0][2]
        self.symbol = p[0][3]
        conn.close()


    def getCode(self):
        return self.code


    def getName(self):
        return self.name


    def getSimbol(self):
        return self.symbol