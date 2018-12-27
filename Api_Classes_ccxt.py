from decimal import *
import ccxt
import sys
import requests
from ccxt.base.errors import BaseError, RequestTimeout


class ApiClassesCCXT(object):

    def __init__(self, pub, priv, name_exchange):
        self.name = name_exchange

        if name_exchange == 'bitfinex':
            self.exchange = getattr(ccxt, name_exchange)({
                'apiKey': pub,
                'secret': priv,
                'nonce': ccxt.Exchange.microseconds,
                'options': {'adjustForTimeDifference': True}
            })
        elif name_exchange == 'poloniex':
            self.exchange = getattr(ccxt, name_exchange)({
                'apiKey': pub,
                'secret': priv,
                'nonce': ccxt.Exchange.microseconds,
                'options': {'adjustForTimeDifference': True}
            })
        else:
            self.exchange = getattr(ccxt, name_exchange)({
                'apiKey': pub,
                'secret': priv,
                'options': {'adjustForTimeDifference': True}
            })

        self.bid = Decimal()
        self.bid_amount = Decimal()
        self.ask = Decimal()
        self.ask_amount = Decimal()

    def returnName(self):
        return self.name

    def fetch_balance(self):
        try:
            t_balance = self.exchange.fetch_balance()

            return t_balance

        except (KeyError, IndexError, BaseError, RequestTimeout) as e:
            print(e)
            pass
        return 0

    def get_trading_balance(self, coin):

        try:
            t_balance = self.exchange.fetch_balance()

            #print (t_balance)

            for x in range(0, len(t_balance['info'])):
                if coin in t_balance:
                    return t_balance[coin]['free']
                else:
                    return 0.0
        except (KeyError, IndexError) as e:
            print(e)
            sys.exit()


if __name__ == "__main__":

    # test stuff here
    a = ApiClassesCCXT('', '', 'BTC', 'binance')
    b = a.get_orderbook('TRX')
    #b = a.get_trading_balance('BTC')
    b = a.return_bid()
    print(b)
    # print(a.return_bid())
