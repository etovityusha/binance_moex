from decimal import Decimal

import requests
import dateutil.parser

from core.models.price import Price
from config import TINKOFF_TOKEN


def get_usdrub_price() -> Price:
    """
    Return usdrub last price from MOEX and price timestamp
    """
    headers = {
        "Authorization": f"Bearer {TINKOFF_TOKEN}"
    }
    base_url = 'https://invest-public-api.tinkoff.ru/rest/'
    data = requests.post(
        base_url + 'tinkoff.public.invest.api.contract.v1.MarketDataService/GetLastPrices', headers=headers,
        json={"figi": ["BBG0013HGFT4"]}
    ).json()
    price = Decimal(
        f"{data['lastPrices'][0]['price']['units']}.{data['lastPrices'][0]['price']['nano']}"
    )
    timestamp = int(dateutil.parser.isoparse(data['lastPrices'][0]['time']).timestamp())
    return Price(value=price, timestamp=timestamp)
