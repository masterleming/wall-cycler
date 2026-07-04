# test_Init_Log

import unittest
import unittest.mock as mock
from tempfile import TemporaryDirectory
import os.path
import random
import os

from TestSuite import TestSuite

from wall_cycler.Init.Log import Log, logLevels, levelFromName, LOG_FILE_NAME
import logging


class InitLogTests(TestSuite):

    @classmethod
    def setUpClass(cls):
        cls._pid = os.getpid()

    __loremIpsum = [
        "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
        "Suspendisse", "a", "tincidunt", "mauris", "quis", "maximus", "arcu", "Duis", "vestibulum",
        "lorem", "commodo", "varius", "aliquet", "Pellentesque", "sed", "diam", "vestibulum",
        "mollis", "felis", "quis", "bibendum", "lorem", "Etiam", "sed", "enim", "ut", "ligula",
        "efficitur", "euismod", "vitae", "id", "erat", "Duis", "in", "urna", "vitae", "tortor",
        "laoreet", "posuere", "Etiam", "eget", "eleifend"
    ]

    __noDateFormatStr = "{process:d} | {levelname:8s} | {name:s} | {message:s}"

    def test_settingLogFilePath(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log(self.__noDateFormatStr)
            uut.init(level=logging.DEBUG,
                     logDir=tmpDir,
                     formatDetails={
                         "string": self.__noDateFormatStr,
                         "style": "{"
                     })

            self._logDeterministicMessages()

            self.assertTrue(os.path.exists(logFileName))

    def test_logFileContents(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log(self.__noDateFormatStr)
            uut.init(level=logging.DEBUG,
                     logDir=tmpDir,
                     formatDetails={
                         "string": self.__noDateFormatStr,
                         "style": "{"
                     })

            expectedLogs = self._logDeterministicMessages()

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs, True)

    def test_levelFiltering(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log(self.__noDateFormatStr)
            uut.init(level=logging.ERROR,
                     logDir=tmpDir,
                     formatDetails={
                         "string": self.__noDateFormatStr,
                         "style": "{"
                     })

            expectedLogs = self._logDeterministicMessages(timeAdjustment=-30)

            self.assertTrue(os.path.exists(logFileName))
            filteredExpected = [l for l in expectedLogs if "ERROR" in l or "CRITICAL" in l]
            self._assertLogFileContents(logFileName, filteredExpected)

    def test_formatOverriding(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log(self.__noDateFormatStr)
            uut.init(level=logging.DEBUG,
                     logDir=tmpDir,
                     formatDetails={
                         "string": "%(process)s%(levelname)s%(name)s%(message)s",
                         "style": "%"
                     })

            expectedLogs = self._logDeterministicMessages(formatStr="{}{}{}{}\n")

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs, True)

    def test_differentLogger(self):
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log(self.__noDateFormatStr)
            uut.init(level=logging.ERROR,
                     logDir=tmpDir,
                     formatDetails={
                         "string": self.__noDateFormatStr,
                         "style": "{"
                     })

            expectedLogs = self._logDeterministicMessages(name="ABCDE", timeAdjustment=-30)

            self.assertTrue(os.path.exists(logFileName))
            filteredExpected = [l for l in expectedLogs if "ERROR" in l or "CRITICAL" in l]
            self._assertLogFileContents(logFileName, filteredExpected)

    def test_bootLogging(self):
        expectedFormat = "{}-{}-{}-{}\n"
        with TemporaryDirectory(prefix="log-test-") as tmpDir:
            logFileName = os.path.join(tmpDir, LOG_FILE_NAME)

            uut = Log(self.__noDateFormatStr)
            bootLogs = self._logDeterministicMessages(formatStr=expectedFormat)

            self.assertFalse(os.path.exists(logFileName))

            uut.init(level=logging.ERROR,
                     logDir=tmpDir,
                     formatDetails={
                         "string": "%(process)s-%(levelname)s-%(name)s-%(message)s",
                         "style": "%"
                     })
            expectedLogs = self._logDeterministicMessages(name="ABCDE",
                                                          timeAdjustment=-30,
                                                          formatStr=expectedFormat)
            expectedLogs = bootLogs + [l for l in expectedLogs if "ERROR" in l or "CRITICAL" in l]

            self.assertTrue(os.path.exists(logFileName))
            self._assertLogFileContents(logFileName, expectedLogs)

    def _assertLogFileContents(self, logFileName, expectedLogs, extended=False):
        with open(logFileName) as logFile:
            logLines = logFile.readlines()
            self._assertAndRemoveLogInitMessages(logLines, extended)
            self.assertEqual(logLines, expectedLogs)

    def _assertAndRemoveLogInitMessages(self, readLogs, extended):
        logInitMessages = [
            "Run Logger pre-init to start BOOT Logger.",
            "Configuration provided, running proper initialisation of Logger."
        ]
        if extended:
            logInitMessages += [
                "Logging level:", "Creating file logger; file",
                "Switched BOOT logger to the target Logger."
            ]
        for im in logInitMessages:
            found = False
            for i, rl in enumerate(readLogs):
                if im in rl:
                    readLogs[i:i + 1] = []
                    found = True
                    break
            self.assertTrue(found, "Log init message not found! Missing message '{}'.".format(im))

    @classmethod
    def _logDeterministicMessages(cls, formatStr=None, name="root", timeAdjustment=0):
        if formatStr is None:
            formatStr = "{:d} | {:8s} | {:s} | {:s}\n"

        levelsList = [levelFromName(level) for level in logLevels()]

        messages = []
        for level in levelsList:
            msg = random.choice(cls.__loremIpsum)
            expectedMsg = formatStr.format(cls._pid, logging._levelToName[level], name, msg)
            messages.append(expectedMsg)

            if name != "root":
                logger = logging.getLogger(name)
                logger.log(level, msg)
            else:
                logging.log(level, msg)

        return messages


if __name__ == '__main__':
    unittest.main()
