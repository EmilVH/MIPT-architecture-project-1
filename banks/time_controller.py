from datetime import datetime, timedelta
from typing import Optional

from utils import Singleton


class TimeController(metaclass=Singleton):
    def __init__(self):
        self.curr_time_: Optional[datetime] = None

    def get_curr_time(self):
        return self.curr_time_

    def set_time(self, set_datetime: datetime):
        self.curr_time_ = set_datetime

    def plus_day(self):
        self.curr_time_ = self.curr_time_ + timedelta(days=1)

    def minus_day(self):
        self.curr_time_ = self.curr_time_ - timedelta(days=1)


def get_time() -> datetime:
    return TimeController().get_curr_time()
