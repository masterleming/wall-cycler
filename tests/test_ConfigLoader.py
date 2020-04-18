# test_ConfigLoader

import unittest

import os.path
from tempfile import TemporaryDirectory

from wall_cycler.Config.ConfigLoader import ConfigLoader, DefaultConfig
from wall_cycler.Config.RuntimeConfig import RuntimeConfig

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

_TestConfig1 = RuntimeConfig(order="sorted",
                             wallpaperPaths=["testPath1", "testPath2"],
                             interval="boot",
                             cacheDir=".cache/test",
                             backend="test backend")

_TestConfig2 = RuntimeConfig(wallpaperPaths=["otherPath1", "otherPath2"],
                             interval="2h")

_CombinedConfig = RuntimeConfig(order="sorted",
                                wallpaperPaths=["otherPath1", "otherPath2"],
                                interval="2h",
                                cacheDir=".cache/test",
                                backend="test backend")


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

    def test_defaultFromRuntimeIsTheSameAsFromString(self):
        fromIni = DefaultConfig.getIni()
        fromStr = DefaultConfig.defaultConfig.value
        self.assertEqual(fromIni, fromStr)

    def test_loadFromDefaultConfigFile(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX,
                                dir=TEST_CONFIG_ROOT) as testDir:
            testConfigFile = self._prepareConfig(testDir)

            uut = ConfigLoader()
            self._overrideDefaultConfigPath(uut, testConfigFile)

            conf = uut.loadConfig()

            self.assertEqual(conf, _TestConfig1)

    def test_loadSingleFile(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX,
                                dir=TEST_CONFIG_ROOT) as testDir:
            testConfigFile = self._prepareConfig(testDir)

            uut = ConfigLoader(configPath=testConfigFile)
            self._removeDefaultConfig(uut)

            conf = uut.loadConfig()

            self.assertEqual(conf, _TestConfig1)

    def test_loadMultipleFiles(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX,
                                dir=TEST_CONFIG_ROOT) as testDir:
            defaultConfig = self._prepareConfig(testDir,
                                                TEST_CONFIG_DEFAULT_NAME,
                                                str(_TestConfig1))
            testConfigFile = self._prepareConfig(testDir, TEST_CONFIG_FILE,
                                                 str(_TestConfig2))

            uut = ConfigLoader(configPath=testConfigFile)
            self._overrideDefaultConfigPath(uut, defaultConfig)

            conf = uut.loadConfig()

            self.assertEqual(conf, _CombinedConfig)

    def _ensureConfigDoesNotExist(self, path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    @staticmethod
    def _getDefaultConfig():
        return DefaultConfig.getRuntime()

    @staticmethod
    def _prepareConfig(testDir,
                       configName=TEST_CONFIG_FILE,
                       configString=str(_TestConfig1)):
        testConfName = os.path.join(testDir, configName)
        with open(testConfName, 'w') as testFile:
            testFile.write(configString)
        return testConfName

    @staticmethod
    def _overrideDefaultConfigPath(uut, path):
        uut.configPaths[0] = path

    @staticmethod
    def _removeDefaultConfig(uut):
        uut.configPaths.remove(DefaultConfig.userConfigPath.value)
