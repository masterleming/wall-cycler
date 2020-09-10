# FileLoader

import configparser
import os.path
import enum
from collections.abc import Sequence
from logging import getLogger

from .RuntimeConfig import RuntimeConfig
from ..Interval.Intervals import Interval
from ..Wallpapers.Updaters import UpdaterTypes
from ..exceptions import MissingConfigFileException
from ..Init.Log import levelFromName

_logger = getLogger(__name__)


class DefaultConfig(enum.Enum):
    defaultOrder = UpdaterTypes.shuffle.name
    defaultWallpaperPaths = "$HOME/Pictures"
    defaultInterval = "daily"
    defaultCacheDir = "$HOME/.cache/wall_cycler"
    defaultBackend = "sway"
    userConfigPath = "$HOME/.config/wall_cycler/wall_cycler.conf"
    defaultLogDir = ""
    defaultLogLevel = "WARNING"
    defaultWallpaperRefresh = False

    @classmethod
    def getRuntime(cls):
        _logger.debug("Creating default config.")
        return RuntimeConfig(
            order=cls.defaultOrder.value,
            wallpaperPaths=[cls.defaultWallpaperPaths.value],
            interval=Interval(cls.defaultInterval.value),
            cacheDir=cls.defaultCacheDir.value,
            backend=cls.defaultBackend.value,
            logDir=cls.defaultLogDir.value,
            logLevel=levelFromName(cls.defaultLogLevel.value),
            forceRefresh=cls.defaultWallpaperRefresh.value,
            #TODO: add missing default values! (left to periodically check and update if needed)
        )

    @classmethod
    def getIni(cls):
        _logger.debug("Creating INI default config.")
        return str(cls.getRuntime())


class FileLoader:
    def __init__(self, configPath=None):
        _logger.debug("Creating FileLoader instance.")

        self.configPaths = [DefaultConfig.userConfigPath.value]
        if configPath is not None:
            if isinstance(configPath, str):
                _logger.debug("Config path is string, adding configuration paths.")
                self.configPaths.append(configPath)
            elif isinstance(configPath, Sequence):
                _logger.debug(
                    "Config path is sequence of (assuming) strings, adding all to configuration paths."
                )
                self.configPaths += configPath
            else:
                _logger.debug(
                    "Different type of config path, assuming it can be used, adding to configuration paths."
                )
                self.configPaths.append(configPath)

        self.configParser = None
        self.config = RuntimeConfig()

    def loadConfig(self):
        _logger.info("Loading configuration files.")

        self.configParser = configparser.ConfigParser()
        self.configParser.read_string(DefaultConfig.getIni())

        success = self.configParser.read(self.configPaths)

        if len(success) != len(self.configPaths):
            failed = [confPath for confPath in self.configPaths if confPath not in success]
            if (len(failed) == 1 and failed[0] == DefaultConfig.userConfigPath.value):
                _logger.warning(
                    "Default user config path does not contain configuration file! Path is '%s'.",
                    DefaultConfig.userConfigPath.value)
                pass
            else:
                strList = ', '.join(["'{}'".format(f) for f in failed])
                _logger.error("Failed to load some configuration files! Files: %s.", strList)
                raise MissingConfigFileException(
                    "These configuration file paths are invalid: {}!".format(strList.strip()))

        self.config = RuntimeConfig.fromCfgFile(self.configParser)
        return self.config

    def createDefaultConfig(self, path=None):
        if path is None:
            path = DefaultConfig.userConfigPath.value

        path = self.__expandPath(path)
        _logger.info("Creating default configuration file at '%s'.", path)

        confDir = os.path.dirname(path)
        if confDir != "" and not os.path.exists(confDir):
            _logger.debug("Directory '%s' does not exist, creating.", confDir)
            os.makedirs(confDir, exist_ok=True)
        elif os.path.exists(path):
            backup = path + ".bak"
            _logger.warning("Configuration file '{file}' exists! Moving it to {backup}".format(
                file=path, backup=backup))
            os.rename(path, backup)

        defaultConf = configparser.ConfigParser()
        defaultConf.read_string(DefaultConfig.getIni())
        with open(path, 'w') as confFile:
            defaultConf.write(confFile)
        _logger.debug("Created configuration file.")

    @staticmethod
    def __expandPath(path):
        return os.path.expanduser(os.path.expandvars(path))
