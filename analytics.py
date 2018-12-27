############
# By Michael Bjeski
# With motivation from B.L.O.C, finest in the crypto MOONING Industry
# Start: 04.10.2018
# Get coin-pair information from cryptocurrency exchanges and save that information into a csv or excel file
# while using pandas; ccxt-library, cryptocompare-api
############

"""
MIT License

Copyright (c) 05.11.2018 Michael Bjeski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import getpass
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

from cryptor import Decryptor

import json

from Api_Classes_ccxt import ApiClassesCCXT
from csv_executor import CSVExecutor


# Entry point for analytics.py -> if "python analytics.py" is called
if __name__ == '__main__':

    crypt = Decryptor()

    classes_exchanges_used = []
    exchanges_used = []
    d = []

    try:
        with open('exch_details.json') as json_data:
            #  with open('exchanges_details_ETH.json') as json_data:
            d = json.load(json_data)
            json_data.close()

        exchanges_used = d['exchanges_used']  # all exchanges being taken into account for loop
        print(exchanges_used)

        passwd = getpass.getpass('pass?:')  # (input("pass?"))
        saltwd = getpass.getpass('salt?:')  # (input("salt?"))

        c = False
        while not c:
            ask_price = input("Get price in USD? (y,n)")
            if ask_price == "y":
                c = True
                ask_price = True
            elif ask_price == "n":
                c = True
                ask_price = False

        for count in range(0, len(exchanges_used)):

            name_exchange = exchanges_used[count]
            pub = d[name_exchange]["pub_key_crypt"]
            priv = d[name_exchange]["priv_key_crypt"]

            decrypt_returner = crypt.decrypt(pub, priv, passwd, saltwd)

            pub_returner = bytes.decode(decrypt_returner[0])
            priv_returner = bytes.decode(decrypt_returner[1])

            x = ApiClassesCCXT(pub_returner, priv_returner, name_exchange)
            classes_exchanges_used.append(x)

    except ValueError:
        print('Critical need restart')

    #  Get balances from every coin from and use parameter -> exchanges_used
    dict_coins_exchanges = {'test': {'coin_1': 'amount', 'coin_2': 'amount'}}  # example
    list_final = []
    helper_dict = {'coin_1': 'amount'}  # example

    dict_coins_exchanges.clear()
    helper_dict.clear()

    for counter in range(0, len(exchanges_used)):

        balance_info = classes_exchanges_used[counter].fetch_balance()
        loop_name = 0
        if balance_info:
            loop_name = classes_exchanges_used[counter].returnName()
            print(loop_name)
        else:
            continue

        #####################   EXCEPTION HANDLING #################################
        if loop_name == 'liqui':
            var_balance = 'free'
        else:
            var_balance = 'total'
        #####################   EXCEPTION HANDLING #################################

        #  print(balance_info[var_balance].items())

        helper_dict.clear()

        for k, v in balance_info[var_balance].items():

            if v > 0.001:  # Minimum Amount on exchange

                helper_dict.update({str(k): str(v)})

        dict_coins_exchanges = {loop_name: helper_dict.copy()}
        list_final.append(dict_coins_exchanges)
        #  print(list_final)

    csv_class = CSVExecutor(list_final, ask_price)

    # print(list_final)

