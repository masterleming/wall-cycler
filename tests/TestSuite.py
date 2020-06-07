# TestSuite

import logging
import os.path
from unittest import TestCase

from wall_cycler.Init.Log import Log


class TestSuite(TestCase):
    @classmethod
    def setUpClass(cls):
        logInitialiser = Log()
        logInitialiser.init(logging.DEBUG, os.path.join("tmp/test-logs", cls.__name__))

        cls._logger = logging.getLogger(cls.__name__)
