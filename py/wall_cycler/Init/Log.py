# Log

import logging
import enum
import sys


class Log:

    _defaultFormatStr = "{asctime:s} | {levelname:8s} | {name:s} | {message:s}"

    def __init__(self, level, logFilePath=None, formatDetails={"string": None, "style": None}):
        self._level = level
        self._logFilePath = logFilePath

        if formatDetails["string"] is None or formatDetails["style"] is None:
            formatDetails = {"string": self._defaultFormatStr, "style": '{'}
        self._format = formatDetails

    def init(self):
        logger = logging.getLogger()
        logger.setLevel(self._level)

        if self._logFilePath is not None:
            handler = logging.FileHandler(self._logFilePath)
        else:
            handler = logging.StreamHandler(sys.stderr)
        handler.setLevel(self._level)

        formatter = logging.Formatter(self._format["string"], style=self._format["style"])
        handler.setFormatter(formatter)

        logger.addHandler(handler)
