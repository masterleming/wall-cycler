# Log

import enum
import logging
import logging.handlers
import os.path
import sys

LOG_FILE_NAME = "wcycler.log"

_logger = logging.getLogger(__name__)


class Log:

    _defaultFormatStr = "{asctime:s} | {levelname:8s} | {name:s} | {message:s}"

    def __init__(self):
        self._level = None
        self._logFilePath = None
        self._format = None
        self._memHandler = None

        self.__preInit()

    def __preInit(self):
        _logger.info("Running Logger pre-init to start BOOT Logger.")
        rootLogger = logging.getLogger()
        rootLogger.setLevel(logging.DEBUG)

        self._memHandler = logging.handlers.MemoryHandler(capacity=-1)
        self._memHandler.setFormatter(logging.Formatter(self._defaultFormatStr, style='{'))
        rootLogger.addHandler(self._memHandler)

    def init(self, level, logDir=None, formatDetails={"string": None, "style": None}):
        _logger.info("Configuration provided, running proper initialisation of Logger.")
        self._reinit(level, logDir, formatDetails)
        _logger.debug("Logging level: %s", nameFromLevel(self._level))

        logger = logging.getLogger()
        logger.setLevel(self._level)

        if self._logFilePath is not None:
            _logger.debug("Creating file logger; file '%s'.", self._logFilePath)
            handler = logging.FileHandler(self._logFilePath)
        else:
            _logger.debug("Creating STDERR logger.")
            handler = logging._StderrHandler()
        handler.setLevel(self._level)

        formatter = logging.Formatter(self._format["string"], style=self._format["style"])
        handler.setFormatter(formatter)

        logger.addHandler(handler)

        _logger.info("Switching BOOT logger to the target Logger.")
        if self._memHandler is not None:
            self._memHandler.setLevel(self._level)
            self._memHandler.setTarget(handler)
            self._memHandler.close()
            logger.removeHandler(self._memHandler)

    def _setLogFormat(self, formatDetails):
        if (formatDetails is None or formatDetails["string"] is None
                or formatDetails["style"] is None):
            formatDetails = {"string": self._defaultFormatStr, "style": '{'}
        self._format = formatDetails

    def _reinit(self, level=None, logDir=None, formatDetails=None):
        if level is not None:
            self._level = level

        self._setLogFilePath(logDir)
        self._setLogFormat(formatDetails)

    def _setLogFilePath(self, logDir):
        if logDir is not None and logDir != "":
            absDir = os.path.abspath(os.path.expandvars(os.path.expanduser(logDir)))
            os.makedirs(absDir, exist_ok=True)
            self._logFilePath = os.path.join(absDir, LOG_FILE_NAME)


def logLevels():
    levels = logging._levelToName.copy()
    del levels[logging.NOTSET]
    return [levels[key] for key in sorted(levels)]


def levelFromName(name):
    return logging._nameToLevel[name.upper()]


def nameFromLevel(level):
    return logging._levelToName[level]
