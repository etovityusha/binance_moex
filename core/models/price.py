from decimal import Decimal

from pydantic.main import BaseModel


class Price(BaseModel):
    value: Decimal
    timestamp: int
