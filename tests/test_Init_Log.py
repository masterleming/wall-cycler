# test_Init_Log

import unittest
import unittest.mock as mock
from tempfile import TemporaryDirectory
import os.path
import random
import time

from wall_cycler.Init.Log import Log
import logging

EPOCH = 1591448293


class Test_TestInit_Log(unittest.TestCase):

    __loremIpsum = [
        "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
        "Suspendisse", "a", "tincidunt", "mauris", "quis", "maximus", "arcu", "Duis", "vestibulum",
        "lorem", "commodo", "varius", "aliquet", "Pellentesque", "sed", "diam", "vestibulum",
        "mollis", "felis", "quis", "bibendum", "lorem", "Etiam", "sed", "enim", "ut", "ligula",
        "efficitur", "euismod", "vitae", "id", "erat", "Duis", "in", "urna", "vitae", "tortor",
        "laoreet", "posuere", "Etiam", "eget", "eleifend"
    ]

    def test_settingLogFilePath(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, "test.log")

            uut = Log(level=logging.DEBUG, logFilePath=logFileName)
            uut.init()

            self._logDeterministicMessages()

            self.assertTrue(os.path.exists(logFileName))

    def test_logFileContents(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, "test.log")

            uut = Log(level=logging.DEBUG, logFilePath=logFileName)
            uut.init()

            expectedLogs = self._logDeterministicMessages()

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs)

    def test_levelFiltering(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, "test.log")

            uut = Log(level=logging.ERROR, logFilePath=logFileName)
            uut.init()

            expectedLogs = self._logDeterministicMessages(timeAdjustment=-30)

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(
                logFileName, [el for el in expectedLogs if "ERROR" in el or "CRITICAL" in el])

    def test_formatOverriding(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, "test.log")

            uut = Log(level=logging.DEBUG,
                      logFilePath=logFileName,
                      formatDetails={
                          "string": "%(asctime)s%(levelname)s%(name)s%(message)s",
                          "style": "%"
                      })
            uut.init()

            expectedLogs = self._logDeterministicMessages(formatStr="{}{}{}{}\n")

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs)

    def test_differentLogger(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, "test.log")

            uut = Log(level=logging.ERROR, logFilePath=logFileName)
            uut.init()

            expectedLogs = self._logDeterministicMessages(name="ABCDE", timeAdjustment=-30)

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(
                logFileName, [el for el in expectedLogs if "ERROR" in el or "CRITICAL" in el])

    def _assertLogFileContents(self, logFileName, expectedLogs):
        with open(logFileName) as logFile:
            logLines = logFile.readlines()
            self.assertEqual(logLines, expectedLogs)

    @classmethod
    def _logDeterministicMessages(cls, formatStr=None, name="root", timeAdjustment=0):
        if formatStr is None:
            formatStr = "{:s} | {:8s} | {:s} | {:s}\n"

        levelsList = [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]

        messages = []
        with mock.patch("time.time", timeMock().__next__):
            for i, level in zip(timeMock(EPOCH + timeAdjustment), levelsList):
                msg = random.choice(cls.__loremIpsum)
                expectedMsg = formatStr.format(
                    time.strftime("%Y-%m-%d %H:%M:%S,000", time.localtime(i)),
                    logging._levelToName[level], name, msg)
                messages.append(expectedMsg)

                if name != "root":
                    logger = logging.getLogger(name)
                    logger.log(level, msg)
                else:
                    logging.log(level, msg)

        return messages


def timeMock(startTime=EPOCH):
    time = startTime
    while True:
        tmp = time
        time += 10
        yield tmp


if __name__ == '__main__':
    unittest.main()
