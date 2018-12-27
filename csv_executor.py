import requests
import sys
from datetime import datetime
import pandas as pd
from pandas import ExcelWriter
import copy


class CSVExecutor(object):

    @staticmethod
    def cryptocompare_api_call(coin_name):

        # get price (e.g. in USD) for certain coin_name from the cryptocompare API
        compare_url = 'https://min-api.cryptocompare.com/data/price?fsym='
        usd = requests.get(url=compare_url + coin_name + '&tsyms=USD')
        try:
            returner = float(usd.json()['USD'])
        except KeyError:
            print("failed cryptocompare API with coin: " + coin_name)
            return 0

        return returner

    def __init__(self, list_coins_exch, ask_price=None):

        dic_pd = {}
        max_length = 0
        # np.array(details_np)
        # build a pandas dataframe from list_coins_exch information
        for exch_element in list_coins_exch:
            details_np = []
            for key, value in exch_element.items():

                if len(value) > max_length:
                    max_length = len(value)

                for k, v in value.items():

                    if ask_price:
                        p = self.cryptocompare_api_call(k)
                        details_np.append(str(k + ' vol: ' + v + ' price: ' + str(p * float(v))))
                    else:
                        details_np.append(str(k + ': ' + v))
                dic_pd.update({key: details_np})

        # extend arrays to longest array length for pandas Dataframe conformity
        dic_copy = copy.copy(dic_pd)
        dic_pd = {}
        for key, value in dic_copy.items():

            if len(value) < max_length:

                rest = max_length-len(value)
                b = ['' for i in range(0, rest)]
                value.extend(b)

                dic_pd.update({key: value})

            else:

                dic_pd.update({key: value})

        df = pd.DataFrame(dic_pd)

        # get datetime
        now = datetime.now()
        # save information to an excel file with datetime as the name
        writer = ExcelWriter('./csv/' + str(now) + '.xlsx')
        df.to_excel(writer, 'Sheet1', index=False)
        writer.save()
