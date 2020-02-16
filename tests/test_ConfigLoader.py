# test_ConfigLoader

import unittest
import os.path

from ConfigLoader import ConfigLoader

TEST_CONFIG_PATH = "/tmp/tests/tapeta.cfg"
TEST_DEFAULT_CONFIG_PATH = "/tmp/tests/default.cfg"

class Test_TestConfigLoader(unittest.TestCase):
    pass

    def test_createDefaultConfig(self):
        self._ensureConfigDoesNotExist(TEST_DEFAULT_CONFIG_PATH)

        uut = ConfigLoader()
        uut.createDefaultConfig(TEST_DEFAULT_CONFIG_PATH)

        self.assertTrue(os.path.exists(TEST_DEFAULT_CONFIG_PATH))

        defaultConf = uut.loadConfig()
        writtenConf = ConfigLoader(TEST_DEFAULT_CONFIG_PATH).loadConfig()

        self.assertEqual(defaultConf, writtenConf)

    def _ensureConfigDoesNotExist(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
