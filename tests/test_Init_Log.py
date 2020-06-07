# test_Init_Log

import unittest
import unittest.mock as mock
from tempfile import TemporaryDirectory
import os.path
import random
import time

from TestSuite import TestSuite

from wall_cycler.Init.Log import Log, logLevels, levelFromName, LOG_FILE_NAME
import logging

EPOCH = 1591448293


@mock.patch("wall_cycler.Init.Log._logger", mock.Mock())
class Test_TestInit_Log(TestSuite):
    @classmethod
    def setUpClass(cls):
        pass

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
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log()
            uut.init(level=logging.DEBUG, logDir=tmpDir)

            self._logDeterministicMessages()

            self.assertTrue(os.path.exists(logFileName))

    def test_logFileContents(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log()
            uut.init(level=logging.DEBUG, logDir=tmpDir)

            expectedLogs = self._logDeterministicMessages()

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs)

    def test_levelFiltering(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log()
            uut.init(level=logging.ERROR, logDir=tmpDir)

            expectedLogs = self._logDeterministicMessages(timeAdjustment=-30)

            self.assertTrue(os.path.exists(logFileName))
            filteredExpected = [l for l in expectedLogs if "ERROR" in l or "CRITICAL" in l]
            self._assertLogFileContents(logFileName, filteredExpected)

    def test_formatOverriding(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log()
            uut.init(level=logging.DEBUG,
                     logDir=tmpDir,
                     formatDetails={
                         "string": "%(asctime)s%(levelname)s%(name)s%(message)s",
                         "style": "%"
                     })

            expectedLogs = self._logDeterministicMessages(formatStr="{}{}{}{}\n")

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs)

    def test_differentLogger(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log()
            uut.init(level=logging.ERROR, logDir=tmpDir)

            expectedLogs = self._logDeterministicMessages(name="ABCDE", timeAdjustment=-30)

            self.assertTrue(os.path.exists(logFileName))
            filteredExpected = [l for l in expectedLogs if "ERROR" in l or "CRITICAL" in l]
            self._assertLogFileContents(logFileName, filteredExpected)

    def test_bootLogging(self):
        expectedFormat = "{}-{}-{}-{}\n"
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log()
            bootLogs = self._logDeterministicMessages(formatStr=expectedFormat)

            self.assertFalse(os.path.exists(logFileName))

            uut.init(level=logging.ERROR,
                     logDir=tmpDir,
                     formatDetails={
                         "string": "%(asctime)s-%(levelname)s-%(name)s-%(message)s",
                         "style": "%"
                     })
            expectedLogs = self._logDeterministicMessages(name="ABCDE",
                                                          timeAdjustment=-30,
                                                          formatStr=expectedFormat)
            expectedLogs = bootLogs + [l for l in expectedLogs if "ERROR" in l or "CRITICAL" in l]

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs)

    def _assertLogFileContents(self, logFileName, expectedLogs):
        with open(logFileName) as logFile:
            logLines = logFile.readlines()
            self.assertEqual(logLines, expectedLogs)

    @classmethod
    def _logDeterministicMessages(cls, formatStr=None, name="root", timeAdjustment=0):
        if formatStr is None:
            formatStr = "{:s} | {:8s} | {:s} | {:s}\n"

        levelsList = [levelFromName(level) for level in logLevels()]

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
