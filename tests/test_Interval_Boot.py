# test_Interval_Boot

import unittest
import unittest.mock as mock
from datetime import datetime, timedelta

from TestSuite import TestSuite

from wall_cycler.Interval.Intervals import BootInterval


class BootIntervalTests(TestSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.boottime = datetime(year=2019,
                                month=12,
                                day=29,
                                hour=10,
                                minute=0,
                                second=0,
                                microsecond=0)

    def test_create(self):
        with mock.patch("uptime.boottime", lambda: self.boottime):
            uut = BootInterval()
            self.assertEqual(uut.lastBoot, self.boottime)

    def test_afterBootExpirationCheck(self):
        with mock.patch("uptime.boottime", lambda: self.boottime):
            uut = BootInterval()

            for days in range(1, 1000):
                lastChangeTimestamp = self._timeAfterBoot(timedelta(days=days))
                self.assertFalse(uut.isExpired(lastChangeTimestamp))

            for hours in range(1, 1000):
                lastChangeTimestamp = self._timeAfterBoot(timedelta(hours=hours))
                self.assertFalse(uut.isExpired(lastChangeTimestamp))

            for minutes in range(1, 1000):
                lastChangeTimestamp = self._timeAfterBoot(timedelta(minutes=minutes))
                self.assertFalse(uut.isExpired(lastChangeTimestamp))

            for seconds in range(1, 1000):
                lastChangeTimestamp = self._timeAfterBoot(timedelta(seconds=seconds))
                self.assertFalse(uut.isExpired(lastChangeTimestamp))

            for milliseconds in range(1, 1000):
                lastChangeTimestamp = self._timeAfterBoot(timedelta(milliseconds=milliseconds))
                self.assertFalse(uut.isExpired(lastChangeTimestamp))

            for microseconds in range(1, 1000):
                lastChangeTimestamp = self._timeAfterBoot(timedelta(microseconds=microseconds))
                self.assertFalse(uut.isExpired(lastChangeTimestamp))

    def test_beforeBootExpirationCheck(self):
        with mock.patch("uptime.boottime", lambda: self.boottime):
            uut = BootInterval()

            for days in range(1, 1000):
                lastChangeTimestamp = self._timeBeforeBoot(timedelta(days=days))
                self.assertTrue(uut.isExpired(lastChangeTimestamp))

            for hours in range(1, 1000):
                lastChangeTimestamp = self._timeBeforeBoot(timedelta(hours=hours))
                self.assertTrue(uut.isExpired(lastChangeTimestamp))

            for minutes in range(1, 1000):
                lastChangeTimestamp = self._timeBeforeBoot(timedelta(minutes=minutes))
                self.assertTrue(uut.isExpired(lastChangeTimestamp))

            for seconds in range(1, 1000):
                lastChangeTimestamp = self._timeBeforeBoot(timedelta(seconds=seconds))
                self.assertTrue(uut.isExpired(lastChangeTimestamp))

            for milliseconds in range(1, 1000):
                lastChangeTimestamp = self._timeBeforeBoot(timedelta(milliseconds=milliseconds))
                self.assertTrue(uut.isExpired(lastChangeTimestamp))

            for microseconds in range(1, 1000):
                lastChangeTimestamp = self._timeBeforeBoot(timedelta(microseconds=microseconds))
                self.assertTrue(uut.isExpired(lastChangeTimestamp))

    def test_expirationFromNow(self):
        uut = BootInterval()
        self.assertFalse(uut.isExpired(datetime.now()))

    def test_mark(self):
        uut = BootInterval()
        self.assertEqual(uut.mark(), "boot")

    def test_getNext(self):
        uut = BootInterval()
        self.assertEqual(uut.getNext(datetime.now()), None)

    def test_string(self):
        uut = BootInterval()
        self.assertEqual(str(uut), "boot")

    @classmethod
    def _timeAfterBoot(cls, diff=timedelta(days=0, hours=2, minutes=30)):
        return cls.boottime + diff

    @classmethod
    def _timeBeforeBoot(cls, diff=timedelta(days=1, hours=6, minutes=15, seconds=3)):
        return cls.boottime - diff


if __name__ == '__main__':
    unittest.main()
