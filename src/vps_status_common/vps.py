from dataclasses import dataclass
from datetime import datetime


@dataclass
class VPS:
    student: str
    date_time_batch: datetime
    ip: str
