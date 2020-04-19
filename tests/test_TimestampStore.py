# test_TimestampStore

import unittest
import unittest.mock as mock
from datetime import datetime
from tempfile import TemporaryDirectory

from wall_cycler.DataStore import DataStore
from wall_cycler.Config.RuntimeConfig import RuntimeConfig
from wall_cycler.Interval.TimestampStore import TimestampStore

TEST_CACHE_ROOT = '/tmp'
TEST_CACHE_TEMP_PREFIX = 'test-timestamp-'

TEST_MESSAGE = "lorem ipsum dolor sit, amet, consectetur, adipisci"


class Test_TestTimestampStore(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.minutes = 10 * 24 * 60
        cls.now = datetime(year=2019,
                           month=12,
                           day=29,
                           hour=15,
                           minute=40,
                           second=20)

    def test_timestampStore(self):
        with mock.patch("wall_cycler.Interval.TimestampStore.datetime", mock.Mock()) as fakeDateTime, \
            TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX,dir=TEST_CACHE_ROOT) as testDir:

            fakeDateTime.now = lambda: self.now

            uut = TimestampStore(RuntimeConfig(cacheDir=testDir))

            uut.writeTimestamp(TEST_MESSAGE)
            timestamp, msg = uut.readTimestamp()

            self.assertEqual(timestamp, self.now)
            self.assertEqual(msg, TEST_MESSAGE)

    def test_inDistinctDbInstances(self):
        with mock.patch("wall_cycler.Interval.TimestampStore.datetime", mock.Mock()) as fakeDateTime, \
            TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX,dir=TEST_CACHE_ROOT) as testDir:

            fakeDateTime.now = lambda: self.now
            conf = RuntimeConfig(cacheDir=testDir)

            uut1 = TimestampStore(conf)
            uut1.writeTimestamp(TEST_MESSAGE)

            uut2 = TimestampStore(conf)
            timestamp, msg = uut2.readTimestamp()

            self.assertEqual(timestamp, self.now)
            self.assertEqual(msg, TEST_MESSAGE)


if __name__ == '__main__':
    unittest.main()
