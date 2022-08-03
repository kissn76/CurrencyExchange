import db_sqlite as db
import bankaccount
import movement
from movement import movements_by_accountId, movements_by_transactionId


def account_movements_print(conn, accountId):
    account = bankaccount.BankAccount()
    account.load_by_id(accountId)
    account_provider = account.getProvider()
    account_currency = account.getCurrency()

    # print(account, account_provider, account_currency)
    print(f"{'Account name':16}: {account.getName()}")
    print(f"{'Provider name':16}: {account_provider.getName()}")
    print(f"{'Account currency':16}: {account_currency.getName()} ({account_currency.getCode()}, {account_currency.getSimbol()})\n")
    print(f"{'Date':<19}|{'Type':<12}|{'Amount':>16}|{'Balance':>16}|{'Connected movement':>35}|")
    print( "===================|============|================|================|===================================|")

    # account_movements = db.movement_select_by_accountId(conn, accountId)
    account_movements = movement.movements_by_accountId(accountId)
    balance = 0
    for movement in account_movements:
        balance += movement.getAmount()

        movement_transaction = db.transaction_select_by_id(conn, movement.getId())
        movement_transaction_typeId = movement_transaction[0][1]
        movement_transaction_note = movement_transaction[0][2]

        movement_transaction_type = db.transaction_type_select_by_id(conn, movement_transaction_typeId)
        movement_transaction_type_code = movement_transaction_type[0][1]
        movement_transaction_type_name = movement_transaction_type[0][2]
        movement_transaction_type_note = movement_transaction_type[0][3]

        movement_connected_movements = movement.movements_by_transactionId(movement.getId())
        connected_movements_str = ""
        for m in movement_connected_movements:
            m_account = bankaccount.BankAccount()
            m_account.load_by_id(m.getId())
            m_account_currency = m_account.getCurrency()

            if m.getId() != movement.getId():
                connected_movements_str += f"{m_account.getName()} {m.getAmount():16,.2f}{m_account_currency.getSimbol()}".replace(",", " ")
                # connected_movements_str += str(m)

        # print(movement, movement_transaction, movement_transaction_type, balance)
        print(f"{movement.getDatetime():19}|{movement_transaction_type_name:12}|{movement.getAmount():16,.2f}|{balance:16,.2f}|".replace(",", " "), f"{connected_movements_str:>34}|")

    print( "=================================================|================|====================================")
    print(f"                                                 |{balance:16,.2f}|".replace(",", " "))


def main():
    db.create_tables()

    conn = db.create_connection("database.db")

    if conn is not None:

        # provider_insert(conn, ["OTP", "OTP Bank NyRT"])
        # currency_insert(conn, ["HUF", "Hungarian forint", "Ft"])
        # currency_insert(conn, ["USD", "United States dollar", "$"])
        # currency_insert(conn, ["EUR", "Euro", "€"])
        # bank_account_insert(conn, ["OTP HUF account", 1, 1, None])
        # bank_account_insert(conn, ["OTP USD account", 1, 2, None])
        # bank_account_insert(conn, ["OTP EUR account", 1, 3, None])
        # transaction_type_insert(conn, ["DEP", "Deposit", "Deposit money from outside bank account or deposit cash"])
        # transaction_type_insert(conn, ["WIT", "Withdraw", "Withdraw money to outside bank account or withdraw cash"])
        # transaction_type_insert(conn, ["TRA", "Transfer", "Transfer money between inside bank accounts"])

        # deposite(conn, 1, 5000000)
        # withdraw(conn, 1, 1500000)
        # deposite(conn, 1, 8000000, date_time="2022-08-02 12:00:01")
        # transfer(conn, ["2022-08-02 12:01:01", 1, 1100000, None], ["2022-08-02 12:01:01", 2, 2820.15, None])
        # transfer(conn, ["2022-08-03 12:15:15", 1, 1100000, None], ["2022-08-03 12:15:15", 3, 2682.25, None])
        # transfer(conn, ["2022-08-02 12:04:31", 1, 1100000, None], ["2022-08-02 12:04:31", 2, 2819.85, None])
        # transfer(conn, ["2022-08-03 12:45:45", 1, 1100000, None], ["2022-08-03 12:45:45", 3, 2598.64, None])


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
        # now = datetime.now()
        # dt = now.strftime("%Y-%m-%d %H:%M:%S")
        # exchange_rate_insert(conn, [provider_id, dt, currency_from_id, currency_to_id, 390.12, 399.99])
        # exchange_rate_insert_p(conn, "OTP", "HUF", "USD", dt, 390.12, 399.99)

        # all_rates = exchange_rate_select_all(conn)
        # if all_rates is not None:
        #     for rate in all_rates:
        #         print(rate)

        # all_bank_accounts = bank_account_select_all(conn)
        # if all_bank_accounts is not None:
        #     print(all_bank_accounts)

        # all_transaction_types = transaction_type_select_all(conn)
        # if all_transaction_types is not None:
        #     print(all_transaction_types)

        # all_transactions = transaction_select_all(conn)
        # if all_transactions is not None:
        #     print(all_transactions)

        # all_movements = movement_select_all(conn)
        # if all_movements is not None:
        #     print(all_movements)

        account_movements_print(conn, 1)
        account_movements_print(conn, 2)
        account_movements_print(conn, 3)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()