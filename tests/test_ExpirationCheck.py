# test_ExpirationCheck

import unittest
import unittest.mock as mock
from datetime import datetime, timedelta, time

from wall_cycler.Interval.ExpirationCheck import ExpirationCheck
from wall_cycler.Interval.Intervals import BaseInterval

TEST_NOW = datetime(year=2019, month=12, day=29, hour=15, minute=40, second=20)
TEST_MSG = "test message"


class test_ExpirationCheck(unittest.TestCase):
    def test_expirationCheck(self):
        mockIntervals = self._prepareTestIntervals()

        for interval in mockIntervals:
            timestampStore = _MockTimestampStore(TEST_NOW)
            uut = ExpirationCheck(interval, timestampStore)

            self.assertEqual(uut.isExpired(), interval._isExpired)
            self.assertEqual(interval._testedAgainstTimestamp, TEST_NOW)

    def test_mark(self):
        mockIntervals = self._prepareTestIntervals()

        for interval in mockIntervals:
            timestampStore = _MockTimestampStore(TEST_NOW)
            uut = ExpirationCheck(interval, timestampStore)

            uut.mark()

            self.assertTrue(interval._calledMark)
            self.assertEqual(timestampStore.timestamp, TEST_NOW)
            self.assertEqual(timestampStore.msg, TEST_MSG)

    def test_getNext(self):
        mockIntervals = self._prepareTestIntervals()

        for interval in mockIntervals:
            timestampStore = _MockTimestampStore(TEST_NOW)
            uut = ExpirationCheck(interval, timestampStore)

            nextChange = uut.getNext()

            self.assertEqual(nextChange, interval._next)
            self.assertTrue(timestampStore._calledRead)

    def test_alwaysTrueWhenNoTimestampInCache(self):
        mockIntervals = self._prepareTestIntervals()

        for interval in mockIntervals:
            timestampStore = _MockTimestampStore(None)
            uut = ExpirationCheck(interval, timestampStore)

            self.assertEqual(uut.isExpired(), True)
            self.assertEqual(interval._testedAgainstTimestamp, None)

    @staticmethod
    def _prepareTestIntervals():
        return [
            _MockInterval(False, TEST_NOW + timedelta(days=1)),
            _MockInterval(True, TEST_NOW + timedelta(days=1))
        ]


class _MockTimestampStore:
    def __init__(self, lastTimestamp):
        self.msg = None
        self.timestamp = lastTimestamp
        self._now = TEST_NOW
        self._calledRead = False

    def readTimestamp(self):
        self._calledRead = True
        return self.timestamp, self.msg

    def writeTimestamp(self, msg):
        self.timestamp = self._now
        self.msg = msg


class _MockInterval(BaseInterval):
    def __init__(self, isExpired, nextChange):
        self._isExpired = isExpired
        self._next = nextChange
        self._calledMark = False
        self._testedAgainstTimestamp = None

    def isExpired(self, lastChange):
        self._testedAgainstTimestamp = lastChange
        return self._isExpired

    def mark(self):
        self._calledMark = True
        return TEST_MSG

    def getNext(self, lastChange):
        self._testedAgainstTimestamp = lastChange
        return self._next

    def __str__(self):
        return "testInterval({}, {}, {}, {})".format(self._isExpired, self._next, self._calledMark,
                                                     self._testedAgainstTimestamp)


if __name__ == '__main__':
    unittest.main()
