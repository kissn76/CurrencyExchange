import db_sqlite as db
import provider
import currency


class BankAccount:
    def __init__(self):
        self.id = None
        self.name = None
        self.provider = None
        self.currency = None
        self.note = None


    def load_by_id(self, id):
        conn = db.create_connection("database.db")
        p = db.bank_account_select_by_id(conn, id)
        self.id = p[0][0]
        self.name = p[0][1]
        providerId = p[0][2]
        currencyId = p[0][3]
        self.note = p[0][4]
        self.provider = provider.Provider()
        self.provider.load_by_id(providerId)
        self.currency = currency.Currency()
        self.currency.load_by_id(currencyId)
        conn.close()


    def getName(self):
        return self.name


    def getProvider(self):
        return self.provider


    def getCurrency(self):
        return self.currency


    def getNote(self):
        return self.note

