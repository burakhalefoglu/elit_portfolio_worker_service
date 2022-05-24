from dataclasses import dataclass
from datetime import datetime


@dataclass
class BistHistoricalData:
    date: datetime
    code: str
    value: float
    status = True

