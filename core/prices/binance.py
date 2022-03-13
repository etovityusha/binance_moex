import datetime

import requests

from core.models.price import Price


class P2PBinanceData:
    """
    Класс для получения лучших предложений по покупке и продаже на рынке p2p
    """

    def __init__(self, asset: str = 'USDT', fiat: str = 'RUB', trade_type: str = 'BUY'):
        self.body = {
            "page": 1,
            "rows": 1,
            "asset": asset,
            "fiat": fiat,
            "merchantCheck": False,
            "payTypes": ["Tinkoff"],
            "tradeType": trade_type
        }

    def get_best_offer(self):
        data = requests.post(
            'https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search',
            json=self.body
        ).json()['data'][0]
        return Price(
            value=data['adv']['price'],
            timestamp=int(datetime.datetime.utcnow().timestamp())
        )
