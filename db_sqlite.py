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


def main():
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

    sql_create_table_transactions = """ CREATE TABLE IF NOT EXISTS transactions (
                                        id integer PRIMARY KEY,
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

        provider_insert(conn, ["OTP", "OTP Bank NyRT"])
        currency_insert(conn, ["HUF", "Hungarian forint", "Ft"])
        currency_insert(conn, ["USD", "United States dollar", "$"])
        currency_insert(conn, ["EUR", "Euro", "€"])

        # all_provider = provider_select_all(conn)
        # if all_provider is not None:
        #     print(all_provider)

        # provider1 = provider_select_by_code(conn, "OTP")
        # print(provider1)

        # all_currencies = currency_select_all(conn)
        # if all_currencies is not None:
        #     print(all_currencies)

        # currency1 = currency_select_by_code(conn, "HUF")
        # print(currency1)

        # provider_id = provider_select_by_code(conn, "OTP")[0][0]
        # currency_from_id = currency_select_by_code(conn, "HUF")[0][0]
        # currency_to_id = currency_select_by_code(conn, "USD")[0][0]
        now = datetime.now()
        dt = now.strftime("%Y-%m-%d %H:%M:%S")
        # exchange_rate_insert(conn, [provider_id, dt, currency_from_id, currency_to_id, 390.12, 399.99])
        exchange_rate_insert_p(conn, "OTP", "HUF", "USD", dt, 390.12, 399.99)

        all_rates = exchange_rate_select_all(conn)
        if all_rates is not None:
            for rate in all_rates:
                print(rate)


    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()