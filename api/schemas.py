from typing import Optional

from pydantic.main import BaseModel
from pydantic.types import Enum


class Asset(str, Enum):
    usdt = 'USDT'
    btc = 'BTC'
    busd = 'BUSD'
    bnb = 'BNB'
    rub = 'RUB'
    shib = 'SHIB'


class Currency(str, Enum):
    rub = 'RUB'
    usd = 'USD'


class TradeType(str, Enum):
    buy = 'BUY'
    sell = 'SELL'


class BinanceArgs(BaseModel):
    asset: Asset
    fiat: Currency
    trade_type: TradeType
    amount: Optional[int]


class ScenarioResponse(BaseModel):
    profit: float
    oldest_quote: int
    details: dict
