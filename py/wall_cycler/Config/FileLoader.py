# FileLoader

import configparser
import os.path
import enum
from collections.abc import Sequence

from .RuntimeConfig import RuntimeConfig
from wall_cycler.Interval.Intervals import Interval
from wall_cycler.Wallpapers.Updaters import UpdaterTypes
from wall_cycler.exceptions import MissingConfigFileException
from wall_cycler.Init.Log import levelFromName
"""
[wall_cycler]
order = shuffle | sorted
wallpaper paths = multiple paths allowed in either unix format (path1:path2) or multiline in separate lines
change time = 1d 4h 30m | boot | daily
cache dir = path to the cache folder
wallpaper backend = sway | $(expression)
"""


class DefaultConfig(enum.Enum):
    defaultOrder = UpdaterTypes.shuffle.name
    defaultWallpaperPaths = "$HOME/Pictures"
    defaultInterval = "daily"
    defaultCacheDir = "$HOME/.cache/wall_cycler"
    defaultBackend = "sway"
    userConfigPath = "$HOME/.config/wall_cycler/wall_cycler.conf"
    defaultLogDir = ""
    defaultLogLevel = "WARNING"

    @classmethod
    def getRuntime(cls):
        return RuntimeConfig(
            order=cls.defaultOrder.value,
            wallpaperPaths=[cls.defaultWallpaperPaths.value],
            interval=Interval(cls.defaultInterval.value),
            cacheDir=cls.defaultCacheDir.value,
            backend=cls.defaultBackend.value,
            logDir=cls.defaultLogDir.value,
            logLevel=levelFromName(cls.defaultLogLevel.value)
            #TODO: add missing default values! (left to periodically check and update if needed)
        )

    @classmethod
    def getIni(cls):
        return str(cls.getRuntime())


class FileLoader:
    def __init__(self, configPath=None):
        self.configPaths = [DefaultConfig.userConfigPath.value]
        if configPath is not None:
            if isinstance(configPath, str):
                self.configPaths.append(configPath)
            elif isinstance(configPath, Sequence):
                self.configPaths += configPath
            else:
                self.configPaths.append(configPath)

        self.configParser = None
        self.config = RuntimeConfig()

    def loadConfig(self):
        self.configParser = configparser.ConfigParser()
        self.configParser.read_string(DefaultConfig.getIni())

        success = self.configParser.read(self.configPaths)

        if len(success) != len(self.configPaths):
            failed = [confPath for confPath in self.configPaths if confPath not in success]
            if (len(failed) == 1 and failed[0] == DefaultConfig.userConfigPath.value):
                #TODO: log
                pass
            else:
                strList = ', '.join(["'{}'".format(f) for f in failed])
                raise MissingConfigFileException(
                    "These configuration file paths are invalid: {}!".format(strList.strip()))

        self.config = RuntimeConfig.fromCfgFile(self.configParser)
        return self.config

    def createDefaultConfig(self, path=None):
        if path is None:
            path = DefaultConfig.userConfigPath.value

        path = self.__expandPath(path)
        confDir = os.path.dirname(path)
        if confDir != "" and not os.path.exists(confDir):
            os.makedirs(confDir, exist_ok=True)
        elif os.path.exists(path):
            backup = path + ".bak"
            print("Configuration file '{file}' exists! Moving it to {backup}".format(file=path,
                                                                                     backup=backup))
            os.rename(path, backup)

        defaultConf = configparser.ConfigParser()
        defaultConf.read_string(DefaultConfig.getIni())
        with open(path, 'w') as confFile:
            defaultConf.write(confFile)

    @staticmethod
    def __expandPath(path):
        return os.path.expanduser(os.path.expandvars(path))
