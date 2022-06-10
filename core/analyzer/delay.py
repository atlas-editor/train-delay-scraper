from datetime import datetime

from core.parser.parser import ZSRParser


class Delay:
    def __init__(self, date : datetime.date, train, delay):
        """
        initializes a class with delay info

        :param date: the date(w/o time) of recorded delay
        :param train: the subject of the delay
        :param delay: the delay in minutes
        """
        self.date = date
        self.train = train
        self.delay = delay

    @classmethod
    def from_parser(cls, parser: ZSRParser):
        return cls(parser.actual_arrival.date(), parser.train, parser.delay)

    def get_list(self):
        return [self.date, self.train.id, self.delay]

    def __str__(self):
        return f"train {self.train.id} had delay {self.delay} minutes on {self.date}"