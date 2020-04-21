# RuntimeConfig

from wall_cycler.Interval import Intervals
from wall_cycler.Wallpapers.Updaters import UpdaterTypes
from wall_cycler.exceptions import InvalidSortOrderException

import enum
from copy import deepcopy


class Modes(enum.Enum):
    GenerateConfig = enum.auto()


class RuntimeConfig:
    class _ConfigFileKeys(enum.Enum):
        rootSection = 'wall_cycler'
        order = 'order'
        wallpaperPaths = 'wallpaper paths'
        interval = 'change time'
        cacheDir = 'cache dir'
        backend = 'wallpaper backend'

    def __init__(self,
                 order="",
                 wallpaperPaths=[],
                 interval=None,
                 cacheDir="",
                 backend="",
                 configFiles=[],
                 mode=None):
        self.order = order
        self.wallpaperPaths = wallpaperPaths
        self.interval = interval
        self.cacheDir = cacheDir
        self.backend = backend
        self.configFiles = configFiles
        self.mode = mode

    def __add__(self, other):
        ret = deepcopy(self)
        ret += other
        return ret

    def __iadd__(self, other):
        default = RuntimeConfig()
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

        if other.configFiles != default.configFiles:
            self.configFiles += other.configFiles

        if other.mode != default.mode:
            self.mode = other.mode

        return self

    @classmethod
    def fromCfgFile(cls, parsed):
        ret = RuntimeConfig()
        appConf = parsed[cls._ConfigFileKeys.rootSection.value]

        val = appConf.get(cls._ConfigFileKeys.order.value)
        if val is not None:
            if val not in UpdaterTypes.choices():
                raise InvalidSortOrderException(val, UpdaterTypes.choices())
            ret.order = val

        val = appConf.get(cls._ConfigFileKeys.wallpaperPaths.value)
        if val is not None:
            ret.wallpaperPaths = [
                p.strip() for path in val.split('\n') for p in path.split(':')
            ]

        val = appConf.get(cls._ConfigFileKeys.interval.value)
        if val is not None:
            ret.interval = Intervals.Interval(val)

        val = appConf.get(cls._ConfigFileKeys.cacheDir.value)
        if val is not None:
            ret.cacheDir = val

        val = appConf.get(cls._ConfigFileKeys.backend.value)
        if val is not None:
            ret.backend = val

        return ret

    @staticmethod
    def fromProgramArgs(argsConf):
        ret = RuntimeConfig()

        if argsConf.order is not None and argsConf.order is not "":
            ret.order = argsConf.order

        if argsConf.img_path is not None and argsConf.img_path is not []:
            ret.wallpaperPaths = argsConf.img_path

        if argsConf.interval is not None:
            ret.interval = argsConf.interval

        if argsConf.cache_dir is not None and argsConf.cache_dir is not "":
            ret.cacheDir = argsConf.cache_dir

        if argsConf.backend is not None and argsConf.backend is not "":
            ret.backend = argsConf.backend

        if argsConf.config is not None and argsConf.config is not []:
            ret.configFiles = [argsConf.config]

        if argsConf.generate_config is not None:
            ret.mode = Modes.GenerateConfig

        return ret

    def __eq__(self, other):
        return (self.order == other.order
                and self.wallpaperPaths == other.wallpaperPaths
                and self.interval == other.interval
                and self.cacheDir == other.cacheDir
                and self.backend == other.backend
                and self.configFiles == other.configFiles
                and self.mode == other.mode)

    def __str__(self):
        ret = "[{root}]\n".format(root=self._ConfigFileKeys.rootSection.value)
        if self.order != "":
            ret += self.__strPrep(self._ConfigFileKeys.order.value, self.order)
        if self.wallpaperPaths != []:
            ret += self.__strPrep(self._ConfigFileKeys.wallpaperPaths.value,
                                  ":".join(self.wallpaperPaths))
        if self.interval is not None:
            ret += self.__strPrep(self._ConfigFileKeys.interval.value,
                                  str(self.interval))
        if self.cacheDir != "":
            ret += self.__strPrep(self._ConfigFileKeys.cacheDir.value,
                                  self.cacheDir)
        if self.backend != "":
            ret += self.__strPrep(self._ConfigFileKeys.backend.value,
                                  self.backend)
        return ret

    def _toDebugStr(self):
        ret = str(self)
        if self.configFiles != []:
            ret += self.__strPrep("config", self.configFiles)
        if self.mode is not None:
            ret += self.__strPrep("mode", self.mode.name)
        return ret

    @staticmethod
    def __strPrep(key, value):
        return "{key} = {value}\n".format(key=key, value=value)
