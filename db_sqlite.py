import sqlite3
from sqlite3 import Error
from datetime import datetime


def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    try:
        cur = conn.cursor()
        cur.execute(create_table_sql)
    except Error as e:
        print(e)


def create_tables():
    sql_create_table_providers = """ CREATE TABLE IF NOT EXISTS providers (
                                        id integer PRIMARY KEY,
                                        code text NOT NULL UNIQUE,
                                        name text
                                    ); """

    sql_create_table_currencies = """ CREATE TABLE IF NOT EXISTS currencies (
                                        id integer PRIMARY KEY,
                                        code text NOT NULL UNIQUE,
                                        name text,
                                        symbol text
                                    ); """

    sql_create_table_exchange_rates = """ CREATE TABLE IF NOT EXISTS exchange_rates (
                                        id integer PRIMARY KEY,
                                        providerId integer,
                                        datetime text,
                                        currencyFromId integer,
                                        currencyToId integer,
                                        exchangeRateBuy real,
                                        exchangeRateSell real
                                    ); """

    sql_create_table_bank_accounts = """ CREATE TABLE IF NOT EXISTS bank_accounts (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL UNIQUE,
                                        providerId integer,
                                        currencyId integer,
                                        note text
                                    ); """

    sql_create_table_transaction_types = """ CREATE TABLE IF NOT EXISTS transaction_types (
                                        id integer PRIMARY KEY,
                                        code text NOT NULL UNIQUE,
                                        name text NOT NULL UNIQUE,
                                        note text
                                    ); """

    sql_create_table_transactions = """ CREATE TABLE IF NOT EXISTS transactions (
                                        id integer PRIMARY KEY,
                                        typeId integer,
                                        note text
                                    ); """

    sql_create_table_movements = """ CREATE TABLE IF NOT EXISTS movements (
                                        id integer PRIMARY KEY,
                                        transactionId integer,
                                        datetime text,
                                        accountId integer,
                                        amount real,
                                        note text
                                    ); """

    conn = create_connection("database.db")

    if conn is not None:
        create_table(conn, sql_create_table_providers)
        create_table(conn, sql_create_table_currencies)
        create_table(conn, sql_create_table_exchange_rates)
        create_table(conn, sql_create_table_bank_accounts)
        create_table(conn, sql_create_table_transaction_types)
        create_table(conn, sql_create_table_transactions)
        create_table(conn, sql_create_table_movements)

    else:
        print("Error! cannot create the database connection.")

    conn.close()


def provider_insert(conn, values):
    sql = "INSERT INTO providers(code, name) VALUES(?, ?)"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        ret = cur.lastrowid
    except Error as e:
        print(e)

    return ret


def provider_select_all(conn):
    sql = "SELECT * FROM providers"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def provider_select_by_code(conn, code):
    sql = "SELECT * FROM providers WHERE code='" + code + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def provider_select_by_id(conn, id):
    sql = "SELECT * FROM providers WHERE id='" + str(id) + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def currency_insert(conn, values):
    sql = "INSERT INTO currencies(code, name, symbol) VALUES(?, ?, ?)"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        ret = cur.lastrowid
    except Error as e:
        print(e)

    return ret


def currency_select_all(conn):
    sql = "SELECT * FROM currencies"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def currency_select_by_code(conn, code):
    sql = "SELECT * FROM currencies WHERE code='" + code + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def currency_select_by_id(conn, id):
    sql = "SELECT * FROM currencies WHERE id='" + str(id) + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def exchange_rate_insert_p(conn, provider, currency_from, currency_to, datetime_str, exchange_buy, exchange_sell):
        provider_id = provider_select_by_code(conn, provider)[0][0]
        currency_from_id = currency_select_by_code(conn, currency_from)[0][0]
        currency_to_id = currency_select_by_code(conn, currency_to)[0][0]
        exchange_rate_insert(conn, [provider_id, datetime_str, currency_from_id, currency_to_id, exchange_buy, exchange_sell])


def exchange_rate_insert(conn, values):
    sql = "INSERT INTO exchange_rates(providerId, datetime, currencyFromId, currencyToId, exchangeRateBuy, exchangeRateSell) VALUES(?, ?, ?, ?, ?, ?)"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        ret = cur.lastrowid
    except Error as e:
        print(e)

    return ret


def exchange_rate_select_all(conn):
    sql = "SELECT p.code, cf.code, ct.code, er.datetime, er.exchangeRateBuy, er.exchangeRateSell FROM exchange_rates er INNER JOIN providers p ON er.providerId = p.id INNER JOIN currencies cf ON er.currencyFromId = cf.id INNER JOIN currencies ct ON er.currencyToId = ct.id"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def bank_account_insert(conn, values):
    sql = "INSERT INTO bank_accounts(name, providerId, currencyId, note) VALUES(?, ?, ?, ?)"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        ret = cur.lastrowid
    except Error as e:
        print(e)

    return ret


def bank_account_select_all(conn):
    sql = "SELECT * FROM bank_accounts"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def bank_account_select_by_id(conn, id):
    sql = "SELECT * FROM bank_accounts WHERE id='" + str(id) + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def transaction_type_insert(conn, values):
    sql = "INSERT INTO transaction_types(code, name, note) VALUES(?, ?, ?)"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        ret = cur.lastrowid
    except Error as e:
        print(e)

    return ret


def transaction_type_select_all(conn):
    sql = "SELECT * FROM transaction_types"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def transaction_type_select_by_code(conn, code):
    sql = "SELECT * FROM transaction_types WHERE code='" + code + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def transaction_type_select_by_id(conn, id):
    sql = "SELECT * FROM transaction_types WHERE id='" + str(id) + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def transaction_insert(conn, values):
    sql = "INSERT INTO transactions(typeId, note) VALUES(?, ?)"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        ret = cur.lastrowid
    except Error as e:
        print(e)

    return ret


def transaction_select_all(conn):
    sql = "SELECT * FROM transactions"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def transaction_select_by_id(conn, id):
    sql = "SELECT * FROM transactions WHERE id='" + str(id) + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def movement_insert(conn, values):
    sql = "INSERT INTO movements(transactionId, datetime, accountId, amount, note) VALUES(?, ?, ?, ?, ?)"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        ret = cur.lastrowid
    except Error as e:
        print(e)

    return ret


def movement_select_all(conn):
    sql = "SELECT * FROM movements"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def movement_select_by_accountId(conn, accountId):
    sql = "SELECT * FROM movements WHERE accountId='" + str(accountId) + "' ORDER BY datetime ASC, id ASC"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def movement_select_by_transactionId(conn, transactionId):
    sql = "SELECT * FROM movements WHERE transactionId='" + str(transactionId) + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def movement_select_by_Id(conn, id):
    sql = "SELECT * FROM movements WHERE id='" + str(id) + "'"
    ret = None

    try:
        cur = conn.cursor()
        cur.execute(sql)
        ret = cur.fetchall()
    except Error as e:
        print(e)

    return ret


def deposite(conn, accountId, amount, date_time=None, note=None):
    # 1. create transaction
    # 2. create movement
    dt = None
    if date_time is None:
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt = date_time
    transaction_id = transaction_insert(conn, [1, None])
    movement_insert(conn, [transaction_id, dt, accountId, amount, note])


def withdraw(conn, accountId, amount, date_time=None, note=None):
    # 1. create transaction
    # 2. create movement
    dt = None
    if date_time is None:
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt = date_time
    transaction_id = transaction_insert(conn, [2, None])
    movement_insert(conn, [transaction_id, dt, accountId, (amount * -1), note])


def transfer(conn, movement_from, movement_to):
    transaction_id = transaction_insert(conn, [3, None])

    movement_from_datetime = movement_from[0]
    movement_from_accountId = movement_from[1]
    movement_from_amount = movement_from[2]
    movement_from_note = movement_from[3]
    movement_insert(conn, [transaction_id, movement_from_datetime, movement_from_accountId, (movement_from_amount * -1), movement_from_note])

    movement_to_datetime = movement_to[0]
    movement_to_accountId = movement_to[1]
    movement_to_amount = movement_to[2]
    movement_to_note = movement_to[3]
    movement_insert(conn, [transaction_id, movement_to_datetime, movement_to_accountId, movement_to_amount, movement_to_note])