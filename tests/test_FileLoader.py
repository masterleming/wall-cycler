# test_FileLoader

import unittest

import os.path
from tempfile import TemporaryDirectory
import logging

from TestSuite import TestSuite

from wall_cycler.Config.FileLoader import FileLoader, DefaultConfig
from wall_cycler.Config.RuntimeConfig import RuntimeConfig

TEST_CONFIG_ROOT = '/tmp'
TEST_CONFIG_TEMP_PREFIX = 'test-'
TEST_CONFIG_DEFAULT_NAME = 'default.cfg'
TEST_CONFIG_FILE = 'test.cfg'
TEST_BACKEDUP_CONFIG_FILE = TEST_CONFIG_FILE + ".bak"
TEST_CONFIG = """
[wall_cycler]
order = sorted
wallpaper paths = testPath1:testPath2
change time = boot
cache dir = .test/cache
wallpaper backend = 'bash -c test'
"""

import os

_TestConfig1 = RuntimeConfig(order="sorted",
                             wallpaperPaths=["testPath1", "testPath2"],
                             interval="boot",
                             cacheDir=".cache/test",
                             backend="test backend",
                             logDir=".cache/log/wall_cycler_test",
                             logLevel=logging.DEBUG,
                             forceRefresh=False,
                             externalScheduling=True)

_TestConfig2 = RuntimeConfig(wallpaperPaths=["otherPath1", "otherPath2"],
                             interval="2h",
                             logDir=".log/test",
                             logLevel=logging.CRITICAL,
                             forceRefresh=True,
                             externalScheduling=False)

_CombinedConfig = RuntimeConfig(order="sorted",
                                wallpaperPaths=["otherPath1", "otherPath2"],
                                interval="2h",
                                cacheDir=".cache/test",
                                backend="test backend",
                                logDir=".log/test",
                                logLevel=logging.CRITICAL,
                                forceRefresh=True,
                                externalScheduling=False)


class FileLoaderTests(TestSuite):
    def test_createDefaultConfig(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX, dir=TEST_CONFIG_ROOT) as testDir:
            defaultConfPath = os.path.join(testDir, TEST_CONFIG_DEFAULT_NAME)
            self._ensureConfigDoesNotExist(defaultConfPath)

            uut = FileLoader()
            uut.createDefaultConfig(defaultConfPath)

            self.assertTrue(os.path.exists(defaultConfPath))

            writtenConf = FileLoader(defaultConfPath).loadConfig()

            defC = self._getDefaultConfig()
            self.assertEqual(writtenConf, defC)

    def test_backingUpConfigBeforeGeneratingNewOne(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX, dir=TEST_CONFIG_ROOT) as testDir:
            confFile = os.path.join(testDir, TEST_CONFIG_FILE)
            backedConfFile = os.path.join(testDir, TEST_BACKEDUP_CONFIG_FILE)

            self._ensureConfigDoesNotExist(confFile)
            self._ensureConfigDoesNotExist(backedConfFile)

            uut = FileLoader()
            uut.createDefaultConfig(confFile)

            self.assertTrue(os.path.exists(confFile))
            self.assertFalse(os.path.exists(backedConfFile))

            uut.createDefaultConfig(confFile)

            self.assertTrue(os.path.exists(confFile))
            self.assertTrue(os.path.exists(backedConfFile))

    def test_loadFromDefaultConfigFile(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX, dir=TEST_CONFIG_ROOT) as testDir:
            testConfigFile = self._prepareConfig(testDir)

            uut = FileLoader()
            self._overrideDefaultConfigPath(uut, testConfigFile)

            conf = uut.loadConfig()

            self.assertEqual(conf, _TestConfig1)

    def test_loadSingleFile(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX, dir=TEST_CONFIG_ROOT) as testDir:
            testConfigFile = self._prepareConfig(testDir)

            uut = FileLoader(configPath=testConfigFile)
            self._removeDefaultConfig(uut)

            conf = uut.loadConfig()

            self.assertEqual(conf, _TestConfig1)

    def test_loadMultipleFiles(self):
        with TemporaryDirectory(prefix=TEST_CONFIG_TEMP_PREFIX, dir=TEST_CONFIG_ROOT) as testDir:
            defaultConfig = self._prepareConfig(testDir, TEST_CONFIG_DEFAULT_NAME,
                                                str(_TestConfig1))
            testConfigFile = self._prepareConfig(testDir, TEST_CONFIG_FILE, str(_TestConfig2))

            uut = FileLoader(configPath=testConfigFile)
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
    def _prepareConfig(testDir, configName=TEST_CONFIG_FILE, configString=str(_TestConfig1)):
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


if __name__ == '__main__':
    unittest.main()
