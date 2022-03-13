import datetime

import asyncio
from fastapi import APIRouter, Depends

from api.schemas import BinanceArgs
from config import BASE_URL
from core.models.price import Price
from core.prices.binance import P2PBinanceData
from core.prices.moex import get_usdrub_price
from core.requests import get_async

router = APIRouter(
    prefix="",
    dependencies=[],
)


@router.get("/prices/moex/usd_rub", response_model=Price, tags=["prices"])
async def usd_rub_moex():
    return get_usdrub_price()


@router.get("/prices/binance/p2p/", response_model=Price, tags=["prices"])
async def binance_data(
        args: BinanceArgs = Depends()
):
    return P2PBinanceData(asset=args.asset, fiat=args.fiat, trade_type=args.trade_type).get_best_offer()


@router.get('/scenarios/1', tags=["scenarios"])
async def async_scenario1():
    """
    Сценарий 1:  покупка USDT за рубли p2p на binance - вывод USD с бинанс p2p на Тинькофф - продажа USD на бирже MOEX
    """
    data = {}
    await asyncio.gather(
        get_async(f'{BASE_URL}/prices/binance/p2p?asset=USDT&fiat=RUB&trade_type=BUY', data, 'buy_usdt_rub_binance'),
        get_async(f'{BASE_URL}/prices/binance/p2p?asset=USDT&fiat=USD&trade_type=SELL', data, 'sell_usdt_usd_binance'),
        get_async(f'{BASE_URL}/prices/moex/usd_rub', data, 'usd_rub_moex'),
    )
    now_timestamp = int(datetime.datetime.utcnow().timestamp())
    return {
        'profit (percentage)': (100 / data['buy_usdt_rub_binance']['value'] *
                                data['sell_usdt_usd_binance']['value'] *
                                data['usd_rub_moex']['value']) - 100,
        'buy_usdt_rub_binance': {
            'price': data['buy_usdt_rub_binance']['value'],
            'updated': f"{now_timestamp - data['buy_usdt_rub_binance']['timestamp']} seconds ago"
        },
        'sell_usdt_usd_binance': {
            'price': data['sell_usdt_usd_binance']['value'],
            'updated': f"{now_timestamp - data['sell_usdt_usd_binance']['timestamp']} seconds ago"
        },
        'usd_rub_moex': {
            'price': data['usd_rub_moex']['value'],
            'updated': f"{now_timestamp - data['usd_rub_moex']['timestamp']} seconds ago"
        },
    }
