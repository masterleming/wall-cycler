# test_Interval_Custom

import unittest
import unittest.mock as mock
from datetime import timedelta, datetime

from wall_cycler.Interval.Intervals import CustomInterval


class Test_TestCustomInterval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.minutes = 10 * 24 * 60
        cls.now = datetime(year=2019, month=12, day=29, hour=15, minute=40, second=20)

    def test_create(self):
        for days, hours, minutes in self._getTimeSpecs(self.minutes):
            diff = timedelta(days=days, hours=hours, minutes=minutes)
            proto = self._createPrototype(days=days, hours=hours, minutes=minutes)

            uut = CustomInterval(proto)
            self.assertEqual(uut.timeDelta, diff)

    def test_expirationCheckLastChangeInTheFuture(self):
        with mock.patch("datetime.datetime", mock.Mock()) as fakeDateTime:
            fakeDateTime.now = lambda: self.now
            for days, hours, minutes in self._getTimeSpecs(self.minutes, self.minutes // 177):
                proto = self._createPrototype(days=days, hours=hours, minutes=minutes)
                uut = CustomInterval(proto)

                seconds = self.minutes * 60
                for timeDiff in self._getTimeDiff(seconds, seconds // 177):
                    self.assertFalse(uut.isExpired(self.now + timeDiff))

    def test_expirationCheckLastChangeGoingBackInTime(self):
        with mock.patch("datetime.datetime", mock.Mock()) as fakeDateTime:
            fakeDateTime.now = lambda: self.now
            for days, hours, minutes in self._getTimeSpecs(48 * 60, 11):
                proto = self._createPrototype(days=days, hours=hours, minutes=minutes)
                intervalInTimeDelta = timedelta(days=days, hours=hours, minutes=minutes)

                uut = CustomInterval(proto)

                seconds = int(intervalInTimeDelta.total_seconds() * 2)
                for timeDiff in self._getTimeDiff(seconds, seconds // 117):
                    lastChange = self.now - timeDiff
                    expired = uut.isExpired(lastChange)
                    self.assertEqual(expired, timeDiff > intervalInTimeDelta)

    def test_expirationFromNow(self):
        for days, hours, minutes in self._getTimeSpecs(self.minutes, self.minutes // 177):
            proto = self._createPrototype(days=days, hours=hours, minutes=minutes)
            uut = CustomInterval(proto)

            self.assertFalse(uut.isExpired(datetime.now()))

    def test_mark(self):
        for days, hours, minutes in self._getTimeSpecs(self.minutes, self.minutes // 177):
            proto = self._createPrototype(days=days, hours=hours, minutes=minutes)
            uut = CustomInterval(proto)

            self.assertEqual(uut.mark(), "custom")

    def test_getNext(self):
        for days, hours, minutes in self._getTimeSpecs(self.minutes, self.minutes // 177):
            proto = self._createPrototype(days=days, hours=hours, minutes=minutes)
            expectedNext = self.now + timedelta(days=days, hours=hours, minutes=minutes)

            uut = CustomInterval(proto)

            self.assertEqual(uut.getNext(self.now), expectedNext)

    def test_string(self):
        for days, hours, minutes in self._getTimeSpecs(self.minutes, self.minutes // 177):
            proto = self._createPrototype(days=days, hours=hours, minutes=minutes)
            uut = CustomInterval(proto)

            self.assertEqual(str(uut), proto)

    @staticmethod
    def _createPrototype(days=0, hours=0, minutes=0):
        parts = []
        if days > 0:
            parts.append("{}d".format(days))
        if hours > 0:
            parts.append("{}h".format(hours))
        if minutes > 0:
            parts.append("{}m".format(minutes))
        if parts == []:
            raise Exception("Empty prototype is not allowed!")

        return " ".join(parts)

    @staticmethod
    def _getTimeSpecs(limitInMinutes, step=37):
        for i in range(1, limitInMinutes, step):
            minutes = i % 60
            hours = (i // 60) % 24
            days = i // (60 * 24)
            yield days, hours, minutes

    @staticmethod
    def _getTimeDiff(limitInSeconds, step):
        for i in range(1, limitInSeconds, step):
            yield timedelta(seconds=i)


if __name__ == '__main__':
    unittest.main()
