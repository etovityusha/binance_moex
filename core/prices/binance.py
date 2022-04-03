import datetime

import requests

from core.models.price import Price


class NoOfferError(Exception):
    """Нет предложений"""
    pass


class P2PBinanceData:
    """
    Класс для получения лучших предложений по покупке и продаже на рынке p2p
    """

    def __init__(self, asset: str = 'USDT', fiat: str = 'RUB', trade_type: str = 'BUY', amount: int = None):
        self.body = {
            "page": 1,
            "rows": 1,
            "asset": asset,
            "fiat": fiat,
            "merchantCheck": False,
            "payTypes": ["Tinkoff"],
            "tradeType": trade_type
        }
        if amount:
            self.body['transAmount'] = str(amount)

    def get_best_offer(self) -> Price:
        try:
            data = requests.post(
                'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
                json=self.body
            ).json()['data'][0]
        except IndexError:
            raise NoOfferError
        return Price(
            value=data['adv']['price'],
            timestamp=int(datetime.datetime.utcnow().timestamp())
        )
