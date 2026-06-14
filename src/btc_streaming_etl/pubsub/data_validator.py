# Standard libraries
# 3rd party
from pydantic import BaseModel, ValidationError

# Custom modules


class YFinanceSocketMessage(BaseModel):
    id: str
    price: float
    time: str
    currency: str
    exchange: str
    quote_type: int
    market_hours: int
    change_percent: float
    day_volume: str
    day_high: float
    day_low: float
    change: float
    open_price: float
    last_size: str
    price_hint: str
    vol_24hr: str
    vol_all_currencies: str
    from_currency: str
    circulating_supply: float
    market_cap: float


class DataValidator:
    def validate_message(self, data: dict) -> bool:
        try:
            YFinanceSocketMessage.model_validate(data)
            return True
        except ValidationError as e:
            return False
