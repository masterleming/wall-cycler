# test_Interval_Daily

import unittest
import unittest.mock as mock
from datetime import datetime, timedelta, date, time

from Interval.Intervals import DailyInterval

class Test_TestDailyInterval(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.today = datetime(year=2019, month=12, day=29)
        cls.hoursInADay = 24
        cls.minutesInADay = cls.hoursInADay * 60
        cls.secondsInADay = cls.minutesInADay * 60
        cls.millisecondsInADay = cls.secondsInADay * 1000
        cls.microsecondsInADay = cls.millisecondsInADay * 1000
        cls.iterations = 177

    def test_create(self):
        with mock.patch("datetime.date", mock.Mock()) as fakeDate:
            fakeDate.today.return_value = self.today.date()
            uut = DailyInterval()
            self.assertEqual(uut.nextChange, self.today + timedelta(days=1))

    def test_expirationCheckAfterMidnight(self):
        with mock.patch("datetime.date", mock.Mock()) as fakeDate:
            fakeDate.today.return_value = self.today.date()
            uut = DailyInterval()

            for microseconds in range(
                    0, self.microsecondsInADay,
                    self.microsecondsInADay // self.iterations):
                lastChange = self._timeAfterToday(timedelta(microseconds=microseconds))
                self.assertFalse(uut.isExpired(lastChange))

            for milliseconds in range(0, self.millisecondsInADay, self.millisecondsInADay // self.iterations):
                lastChange = self._timeAfterToday(timedelta(milliseconds=milliseconds))
                self.assertFalse(uut.isExpired(lastChange))

            for seconds in range(0, self.secondsInADay, self.secondsInADay // self.iterations):
                lastChange = self._timeAfterToday(timedelta(seconds=seconds))
                self.assertFalse(uut.isExpired(lastChange))

            for minutes in range(0, self.minutesInADay, self.minutesInADay // self.iterations):
                lastChange = self._timeAfterToday(timedelta(minutes=minutes))
                self.assertFalse(uut.isExpired(lastChange))

            for hours in range(self.hoursInADay):
                lastChange = self._timeAfterToday(timedelta(hours=hours))
                self.assertFalse(uut.isExpired(lastChange))

    def test_expirationCheckBeforeToday(self):
        with mock.patch("datetime.date", mock.Mock()) as fakeDate:
            fakeDate.today.return_value = self.today.date()
            uut = DailyInterval()

            for microseconds in range(
                    1, self.microsecondsInADay,
                    self.microsecondsInADay // self.iterations):
                lastChange = self._timeBeforeToday(timedelta(microseconds=microseconds))
                self.assertTrue(uut.isExpired(lastChange))

            for milliseconds in range(1, self.millisecondsInADay, self.millisecondsInADay // self.iterations):
                lastChange = self._timeBeforeToday(timedelta(milliseconds=milliseconds))
                self.assertTrue(uut.isExpired(lastChange))

            for seconds in range(1, self.secondsInADay, self.secondsInADay // self.iterations):
                lastChange = self._timeBeforeToday(timedelta(seconds=seconds))
                self.assertTrue(uut.isExpired(lastChange))

            for minutes in range(1, self.minutesInADay, self.minutesInADay // self.iterations):
                lastChange = self._timeBeforeToday(timedelta(minutes=minutes))
                self.assertTrue(uut.isExpired(lastChange))

            for hours in range(1, self.hoursInADay):
                lastChange = self._timeBeforeToday(timedelta(hours=hours))
                self.assertTrue(uut.isExpired(lastChange))

    def test_expirationCheckFromNow(self):
        uut = DailyInterval()
        self.assertFalse(uut.isExpired(datetime.now()))

    def test_mark(self):
        uut = DailyInterval()
        self.assertEqual(uut.mark(), "daily")

    def test_getNext(self):
        with mock.patch("datetime.date", mock.Mock()) as fakeDate:
            tomorrow = datetime.combine(date.today() + timedelta(days=1), time(0))
            fakeDate.today.return_value = self.today.date()
            uut = DailyInterval()
            self.assertEqual(uut.getNext(datetime.now()), tomorrow)

    @classmethod
    def _timeAfterToday(cls, diff):
        return cls.today + diff

    @classmethod
    def _timeBeforeToday(cls, diff):
        return cls.today - diff


if __name__ == '__main__':
    unittest.main()
