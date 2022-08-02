import requests
import datetime
import csv

def download_exchange_rate(date_from, date_to, currencies):
    deviza_veteli = {}
    deviza_eladasi = {}

    filename = ("-".join(currencies)) + "_" + date_from.replace("-", "") + "-" + date_to.replace("-", "") + ".csv"

    api_url = "https://www.otpbank.hu/apps/exchangerate/api/downloads/csv/" + date_from + "/" + date_to + "?currencies=" + (",".join(currencies)) + "&lang=HU"
    response = requests.get(api_url)
    responselines = response.text.split('\r\n')

    text_file = open(filename, "wt")
    text_file.write(response.text)
    text_file.close()

    newcurrencies = csv.reader(responselines, delimiter=';')
    newcurrencies = list(newcurrencies)
    del newcurrencies[0]
    del newcurrencies[0]

    for actcurrency in currencies:
        newestcurrency = None
        for newcurrency in newcurrencies:
            if len(newcurrency) > 0:
                if newcurrency[0] == actcurrency:   # currency Név
                    if newestcurrency is None:
                        newestcurrency = newcurrency
                    else:
                        if newcurrency[10] > newestcurrency[10]:    # currency Verzió
                            newestcurrency = newcurrency

        deviza_veteli.update({actcurrency:newestcurrency[8]})   # currency Deviza vételi
        deviza_eladasi.update({actcurrency:newestcurrency[9]})   # currency Deviza eladási

    return deviza_veteli, deviza_eladasi


def main():
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    currencies = ["EUR", "USD"]

    deviza_veteli, deviza_eladasi = download_exchange_rate(today, today, currencies)

    for currency in currencies:
        print(currency + ": " + deviza_veteli[currency] + " " + deviza_eladasi[currency])


if __name__ == '__main__':
    main()