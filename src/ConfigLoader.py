# ConfigLoader

import configparser
import os.path
from exceptions import MissingConfigFileException

import argparse

"""
[xyz]
order = shuffle | sorted
wallpaper paths = multiple paths allowed in either unix format (path1:path2) or multiline in separate lines
change time = 1d 4h 30m | boot | daily
cache dir = path to the cache folder
wallpaper backend = sway | $(expression)
"""

__defaultConfig = """
[xyz]
order = shuffle
wallpaper paths = $HOME/Pictures
change time = daily
cache dir = $HOME/.cache/xyz
wallpaper backend = sway
"""

class Config:
    def __init__(self):
        self.order = ""
        self.wallpaperPaths = []
        self.interval = None # TODO
        self.cacheDir = ""
        self.backend = ""

    def __iadd__(self, other):
        default = Config()
        if other.order != default.order:
            self.order = other.order

        if other.wallpaperPaths != default.wallpaperPaths:
            self.wallpaperPaths = other.wallpaperPaths

        if other.interval != default.interval:
            self.interval = other.interval

        if other.cacheDir != default.cacheDir:
            self.cacheDir = other.cacheDir

        if other.backend != default.backend:
            self.backend = other.backend

        return self

    @staticmethod
    def fromParsedConfig(parsed):
        ret = Config()
        xyzConf = parsed['xyz']

        val = xyzConf.get('order')
        if val is not None:
            ret.order = val

        val = xyzConf.get('wallpaper paths')
        if val is not None:
            ret.wallpaperPaths = [p.strip() for path in val.split('\n') for p in path.split(':') ]

        val = xyzConf.get('change time')
        if val is not None:
            ret.interval = None # TODO:

        val = xyzConf.get('cache dir')
        if val is not None:
            ret.cacheDir = val

        val = xyzConf.get('wallpaper backend')
        if val is not None:
            ret.backend = val

    @staticmethod
    def fromRuntimeConfig(runtime):
        ret = Config()
        runtime = argparse.ArgumentParser().parse_args()

        if runtime.order is not None and runtime.order is not "":
            ret.order = runtime.order

        if runtime.img_path is not None and runtime.img_path is not []:
            ret.wallpaperPaths = runtime.wallpaperPaths

        if runtime.interval is not None:
            ret.interval = None # TODO:

        if runtime.cache_dir is not None and runtime.cache_dir is not "":
            ret.cacheDir = runtime.cache_dir

        if runtime.backend is not None and runtime.backend is not "":
            ret.backend = runtime.backend

        return ret

class ConfigLoader:

    __userConfigPath = "$HOME/.config/xyz/xyz.conf"

    def __init__(self, configPath=None, runtimeConf=None):
        self.configPaths = [self.__userConfigPath]
        if configPath is not None:
            self.configPaths.append(configPath)
        self.runtimeConf = runtimeConf
        self.configParser = None
        self.config = Config()

    def loadConfig(self):
        self.configParser = configparser.ConfigParser()
        self.configParser.read_string(__defaultConfig)

        success = self.configParser.read(self.configPaths)

        if len(success) != len(self.configPaths):
            failed = self.configPaths - success
            if len(failed) == 1 and failed[0] == self.__userConfigPath:
                #TODO: log
                pass
            else:
                strList = ', '.join(["'{}'".format(f) for f in failed])
                raise MissingConfigFileException(
                    "These configuration file paths are invalid: {}!".format(
                        strList.strip))

        self.config = Config.fromParsedConfig(self.configParser)
        self._combineWithRuntimeArgs()

        return self.config

    def createDefaultConfig(self, path=None):
        if path is None:
            path = self.__userConfigPath

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
        defaultConf.read_string(__defaultConfig)
        with open(path, 'w') as confFile:
            defaultConf.write(confFile)

    def _combineWithRuntimeArgs(self):
        runtime = Config.fromRuntimeConfig(self.runtimeConf)
        self.config += runtime

    @staticmethod
    def __expandPath(path):
        return os.path.expanduser(os.path.expandvars(path))
