# test_ConfigLoader

import unittest
import os.path
from tempfile import TemporaryDirectory

from ConfigLoader import ConfigLoader, DefaultConfig
from RuntimeConfig import RuntimeConfig

TEST_CONFIG_ROOT = '/tmp'
TEST_CONFIG_TEMP_PREFIX = 'test-'
TEST_CONFIG_DEFAULT_NAME = 'default.cfg'
TEST_CONFIG_FILE = 'test.cfg'
TEST_CONFIG = """
[wloop]
order = sorted
wallpaper paths = testPath1:testPath2
change time = boot
cache dir = .test/cache
wallpaper backend = 'bash -c test'
"""

_TestConfig = RuntimeConfig(order="sorted",
                            wallpaperPaths=["testPath1", "testPath2"],
                            interval="boot",
                            cacheDir=".cache/test",
                            backend='test backend')


class Test_TestConfigLoader(unittest.TestCase):
    def test_createDefaultConfig(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX,
                                dir=TEST_CONFIG_ROOT) as testDir:
            defaultConfPath = os.path.join(testDir, TEST_CONFIG_DEFAULT_NAME)
            self._ensureConfigDoesNotExist(defaultConfPath)

            uut = ConfigLoader()
            uut.createDefaultConfig(defaultConfPath)

            self.assertTrue(os.path.exists(defaultConfPath))

            writtenConf = ConfigLoader(defaultConfPath).loadConfig()

            defC = self._getDefaultConfig()
            self.assertEqual(writtenConf, defC)

    def test_loadSingleFile(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX,
                                dir=TEST_CONFIG_ROOT) as testDir:
            testConfigFile = self._prepareConfig(testDir)

            uut = ConfigLoader(configPath=testConfigFile)
            conf = uut.loadConfig()

            self.assertEqual(conf, _TestConfig)

    def test_defaultFromRuntimeIsTheSameAsFromString(self):
        fromIni = DefaultConfig.getIni()
        fromStr = DefaultConfig.defaultConfig.value
        self.assertEqual(fromIni, fromStr)

    def _ensureConfigDoesNotExist(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    @staticmethod
    def _getDefaultConfig():
        return DefaultConfig.getRuntime()

    @staticmethod
    def _prepareConfig(testDir):
        testConfName = os.path.join(testDir, TEST_CONFIG_FILE)
        with open(testConfName, 'w') as testFile:
            testFile.write(str(_TestConfig))
        return testConfName
