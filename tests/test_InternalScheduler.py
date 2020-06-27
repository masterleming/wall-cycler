# test_InternalScheduler

import unittest
import unittest.mock as mock
from datetime import datetime, timedelta
import time

from TestSuite import TestSuite

from wall_cycler.Schedulers.InternalScheduler import InternalScheduler

TEST_START = 30
TEST_THRESHOLD = 31


class InternalSchedulerTests(TestSuite):
    def test_blocksUntilScheduled(self):

        uut = InternalScheduler()

        for i in range(TEST_START, TEST_THRESHOLD, 2):
            delay = i / 10

            startTime = time.time()

            uut.wait(self._nowPlusSeconds(delay))

            stopTime = time.time()
            self.assertGreaterEqual(stopTime - startTime, delay)

    @staticmethod
    def _nowPlusSeconds(seconds):
        return datetime.now() + timedelta(seconds=seconds)


if __name__ == '__main__':
    unittest.main()
