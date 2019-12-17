# Interval

import datetime as dt
import uptime
import re

from exceptions import InvalidTimeIntervalSpecification

__intervalPattern = re.compile(r"(?:\d+[dhm]\s*)+|boot|daily")

def Interval(prototype):
    if not __intervalPattern.search(prototype):
        raise InvalidTimeIntervalSpecification(prototype)

    if prototype is "boot":
        return BootInterval()

    if prototype == "daily":
        return DailyInterval()

    return CustomInterval(prototype)


class BaseInterval:
    def __init__(self):
        self.lastChange, self.changeMessage = self._getTimeStamp()

    def _timeStampWallChange(self, msg):
        self.lastChange = dt.datetime.now()
        self.changeMessage = msg
        # TODO: write to file in cache

    def _getTimeStamp(self):
        # TODO: read from file in cache
        return dt.datetime.now(), "msg"

    def isExpired(self):
        return NotImplemented

    def mark(self):
        return NotImplemented

    def getNext(self):
        return None


class BootInterval(BaseInterval):
    def __init__(self):
        super().__init__(None)
        self.lastBoot = uptime.boottime()

    def isExpired(self):
        return not (self.lastChange < self.lastBoot)

    def mark(self):
        self._timeStampWallChange("boot")


class DailyInterval(BaseInterval):
    def __init__(self):
        super().__init__()
        today = dt.date.today()
        dayDelta = dt.timedelta(days=1)
        self.nextChange = dt.datetime.combine(today + dayDelta, dt.time(0))

    def isExpired(self):
        return self.lastChange.date() < dt.date.today()

    def mark(self):
        self._timeStampWallChange("daily")

    def getNext(self):
        return self.nextChange


class CustomInterval(BaseInterval):

    __pattern = re.compile(r"(\d+)(d|h|m)")

    def __init__(self, prototype):
        super.__init__()
        self.timeDelta = self._timeDelta(prototype)

    def isExpired(self):
        return dt.datetime.now() > self.lastChange

    def mark(self):
        self._timeStampWallChange('custom')

    def getNext(self):
        return self.lastChange + self.timeDelta

    @classmethod
    def _timeDelta(cls, prototype):
        prototype = ""
        timeDelta = {'d':0, 'h':0, 'm':0}

        specs = prototype.split()
        for sp in specs:
            match = cls.__pattern.match(sp)
            val, unit = match.groups()
            if unit not in timeDelta or timeDelta[unit] != 0:
                raise InvalidTimeIntervalSpecification(prototype)
            timeDelta['unit'] = val

        return dt.timedelta(days=timeDelta['d'],
                            hours=timeDelta['h'],
                            minutes=timeDelta['m'])
