from datetime import time


class GetUpData(object):
    nick: str
    get_up_time: time
    get_up_log: str

    def __init__(self, nick: str, get_up_time: time, get_up_log: str):
        self.nick = nick
        self.get_up_time = get_up_time
        self.get_up_log = get_up_log

    def __str__(self):
        return f'nick: {self.nick}, ' \
               f'get_up_time: {self.get_up_time}, ' \
               f'get_up_log: {self.get_up_log}, '

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, GetUpData):
            return self.get_up_time == other.get_up_time
        else:
            raise TypeError("Unsupported types for comparison")

    def __lt__(self, other):
        if isinstance(other, GetUpData):
            return self.get_up_time < other.get_up_time
        else:
            raise TypeError("Unsupported types for comparison")

    def __gt__(self, other):
        if isinstance(other, GetUpData):
            return self.get_up_time > other.get_up_time
        else:
            raise TypeError("Unsupported types for comparison")
