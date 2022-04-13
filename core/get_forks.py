from typing import List

from pydantic import BaseModel
from core.prices.binance import P2PBinanceData
from core.prices.moex import get_usdrub_price


class NotTradableError(Exception):
    pass


class Exchange(BaseModel):
    symbol: str

    def __eq__(self, other):
        return all([
            isinstance(other, Exchange),
            self.symbol == other.symbol
        ])

    def __hash__(self):
        return hash(self.symbol)


moex = Exchange(symbol='moex')
binance = Exchange(symbol='binance')


class Currency(BaseModel):
    exchange: Exchange
    symbol: str

    def __eq__(self, other):
        return all([
            isinstance(other, Currency),
            other.exchange == self.exchange,
            other.symbol == self.symbol
        ])

    def __hash__(self):
        return hash(self.exchange) + hash(self.symbol)

    def __str__(self):
        return f"{self.exchange.symbol}:{self.symbol}"

    def is_tradable_with(self, other):
        if not isinstance(other, Currency):
            raise ValueError
        if self.exchange == binance and other.exchange == binance or self == other:
            return False
        return True

    def get_trade_rate(self, other):
        if not self.is_tradable_with(other):
            raise NotTradableError
        if other.exchange == binance or self.exchange == binance:
            return P2PBinanceData(asset=other.symbol, fiat=self.symbol,
                                  trade_type='BUY' if other.exchange == binance else 'SELL')
        if self.exchange == moex and other.exchange == moex:
            usdrub = get_usdrub_price().value
            return usdrub if self.symbol == 'RUB' else 1 / usdrub


rub_moex = Currency(exchange=moex, symbol='RUB')
usd_moex = Currency(exchange=moex, symbol='USD')

usdt_binance = Currency(exchange=binance, symbol='USDT')
btc_binance = Currency(exchange=binance, symbol='BTC')
busd_binance = Currency(exchange=binance, symbol='BUSD')
bnb_binance = Currency(exchange=binance, symbol='BNB')
eth_binance = Currency(exchange=binance, symbol='ETH')
dai_binance = Currency(exchange=binance, symbol='DAI')

all_currencies = [rub_moex, usd_moex, usdt_binance, btc_binance, busd_binance, bnb_binance, eth_binance, dai_binance]


def get_all_rates():
    rates = {}
    for currency in all_currencies:
        rates[currency] = {}
        for currency2 in all_currencies:
            if currency == currency2:
                continue
            if currency.is_tradable_with(currency2):
                rates[currency][currency2] = currency.get_trade_rate(currency2)
    return rates


def get_all_paths(default_currency: Currency, list_of_currencies: List[Currency]):
    pass