# Intervals

import datetime
import uptime
import re

from wall_cycler.exceptions import InvalidTimeIntervalSpecificationException

__intervalPattern = re.compile(r"(?:\d+[dhm]\s*)+|boot|daily")


def Interval(prototype):
    if not __intervalPattern.search(prototype):
        raise InvalidTimeIntervalSpecificationException(prototype)

    if prototype == "boot":
        return BootInterval()

    if prototype == "daily":
        return DailyInterval()

    return CustomInterval(prototype)


class BaseInterval:
    def __init__(self):
        pass

    def isExpired(self, lastChange):
        return NotImplemented

    def mark(self):
        return NotImplemented

    def getNext(self, lastChange):
        return None

    def __eq__(self, other):
        return str(self) == str(other)


class BootInterval(BaseInterval):
    def __init__(self):
        self.lastBoot = uptime.boottime()

    def isExpired(self, lastChange):
        return lastChange < self.lastBoot

    def mark(self):
        return "boot"

    def __str__(self):
        return "boot"


class DailyInterval(BaseInterval):
    def __init__(self):
        today = datetime.date.today()
        dayDelta = datetime.timedelta(days=1)
        self.nextChange = datetime.datetime.combine(today + dayDelta, datetime.time(0))

    def isExpired(self, lastChange):
        return lastChange.date() < datetime.date.today()

    def mark(self):
        self.__init__()
        return "daily"

    def getNext(self, lastChange):
        return self.nextChange

    def __str__(self):
        return "daily"


class CustomInterval(BaseInterval):

    __pattern = re.compile(r"(\d+)(d|h|m)")

    def __init__(self, prototype):
        self.timeDelta = self._timeDelta(prototype)

    def isExpired(self, lastChange):
        return datetime.datetime.now() > (lastChange + self.timeDelta)

    def mark(self):
        return "custom"

    def getNext(self, lastChange):
        return lastChange + self.timeDelta

    @classmethod
    def _timeDelta(cls, prototype):
        timeDelta = {'d': 0, 'h': 0, 'm': 0}

        specs = prototype.split()
        for sp in specs:
            match = cls.__pattern.match(sp)
            val, unit = match.groups()
            if unit not in timeDelta or timeDelta[unit] != 0:
                raise InvalidTimeIntervalSpecificationException(prototype)
            timeDelta[unit] = int(val)

        return datetime.timedelta(days=timeDelta['d'], hours=timeDelta['h'], minutes=timeDelta['m'])

    def __str__(self):
        tmp = []
        if self.timeDelta.days > 0:
            tmp.append("{}d".format(self.timeDelta.days))
        minutes = int(self.timeDelta.seconds // 60)
        hours = minutes // 60
        minutes = minutes - hours * 60
        if hours > 0:
            tmp.append("{}h".format(hours))
        if minutes > 0:
            tmp.append("{}m".format(minutes))
        return " ".join(tmp)
