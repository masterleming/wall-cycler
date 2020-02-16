# ConfigLoader

import configparser
import os.path
import enum

from exceptions import MissingConfigFileException
from RuntimeConfig import RuntimeConfig

"""
[wloop]
order = shuffle | sorted
wallpaper paths = multiple paths allowed in either unix format (path1:path2) or multiline in separate lines
change time = 1d 4h 30m | boot | daily
cache dir = path to the cache folder
wallpaper backend = sway | $(expression)
"""

class DefaultConfig(enum.Enum):
    defaultConfig = """
[wloop]
order = shuffle
wallpaper paths = $HOME/Pictures
change time = daily
cache dir = $HOME/.cache/wloop
wallpaper backend = sway
"""
    userConfigPath = "$HOME/.config/wloop/wloop.conf"


class GlobalConfig:

    __instance = None

    @classmethod
    def get(cls):
        return cls.__instance

    def __init__(self, config):
        GlobalConfig.__instance = config


class ConfigLoader:
    def __init__(self, configPath=None, runtimeConf=None):
        self.configPaths = [DefaultConfig.userConfigPath.value]
        if configPath is not None:
            self.configPaths.append(configPath)
        self.runtimeConf = runtimeConf
        self.configParser = None
        self.config = RuntimeConfig()

    def loadConfig(self):
        self.configParser = configparser.ConfigParser()
        self.configParser.read_string(DefaultConfig.defaultConfig.value)

        success = self.configParser.read(self.configPaths)

        if len(success) != len(self.configPaths):
            failed = [confPath for confPath in self.configPaths if confPath not in success]
            if len(failed) == 1 and failed[0] == DefaultConfig.userConfigPath.value:
                #TODO: log
                pass
            else:
                strList = ', '.join(["'{}'".format(f) for f in failed])
                raise MissingConfigFileException(
                    "These configuration file paths are invalid: {}!".format(
                        strList.strip))

        self.config = RuntimeConfig.fromCfgFile(self.configParser)
        self._combineWithRuntimeArgs()

        completeConfig = GlobalConfig(self.config)
        return completeConfig.get()

    def createDefaultConfig(self, path=None):
        if path is None:
            path = DefaultConfig.userConfigPath.value

        path = self.__expandPath(path)
        confDir = os.path.dirname(path)
        if not os.path.exists(confDir):
            os.makedirs(confDir, exist_ok=True)
        elif os.path.exists(path):
            backup = path + ".bak"
            print("Configuration file '{file}' exists! Moving it to {backup}".
                  format(file=path, backup=backup))
            os.rename(path, backup)

        defaultConf = configparser.ConfigParser()
        defaultConf.read_string(DefaultConfig.defaultConfig.value)
        with open(path, 'w') as confFile:
            defaultConf.write(confFile)

    def _combineWithRuntimeArgs(self):
        runtime = RuntimeConfig.fromProgramArgs(self.runtimeConf)
        self.config += runtime

    @staticmethod
    def __expandPath(path):
        return os.path.expanduser(os.path.expandvars(path))
