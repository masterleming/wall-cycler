# TestSuite

import logging
import os.path
from unittest import TestCase
from datetime import datetime

from wall_cycler.Init.Log import Log

_logName = datetime.now().strftime("%Y%m%d-%H%M%S.%f_test.log")


class TestSuite(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        logInitialiser = Log()
        logInitialiser.init(logging.DEBUG, os.path.join("tmp/test-logs"), fileName=_logName)

        cls._logger = logging.getLogger(cls.__name__)
