class Movement:
    def __init__(self):
        self.id = None
        self.transactionId = None
        self.datetime = None
        self.accountId = None
        self.amount = None
        self.note = None


    def load_by_id(self, id):
        conn = db.create_connection("database.db")
        p = db.movement_select_by_Id(conn, id)
        self.id = p[0][0]
        self.transactionId = p[0][1]
        self.datetime = p[0][2]
        self.accountId = p[0][3]
        self.amount = p[0][4]
        self.note = p[0][5]
        conn.close()


    def getId(self):
        return self.id


    def getDatetime(self):
        return self.datetime


    def getAmount(self):
        return self.amount


    def getNote(self):
        return self.note


def movements_by_transactionId(transactionId):
    conn = db.create_connection("database.db")
    movements = db.movement_select_by_transactionId(conn, transactionId)
    conn.close()
    ret = []
    for m in movements:
        tmp = Movement()
        tmp.load_by_id(m[0])
        ret.append(tmp)

    return ret


def movements_by_accountId(accountId):
    conn = db.create_connection("database.db")
    movements = db.movement_select_by_accountId(conn, accountId)
    conn.close()
    ret = []
    for m in movements:
        tmp = Movement()
        tmp.load_by_id(m[0])
        ret.append(tmp)

    return ret