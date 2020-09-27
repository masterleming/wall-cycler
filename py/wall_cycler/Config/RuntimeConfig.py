# RuntimeConfig

from ..Interval import Intervals
from ..Wallpapers.Updaters import UpdaterTypes
from ..exceptions import InvalidSortOrderException
from ..Init.Log import levelFromName, nameFromLevel

import enum
from copy import deepcopy
from logging import getLogger

_logger = getLogger(__name__)


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
        logDir = 'log dir'
        logLevel = 'log level'
        forceRefresh = 'force refresh'

    def __init__(self,
                 order="",
                 wallpaperPaths=[],
                 interval=None,
                 cacheDir="",
                 backend="",
                 configFiles=[],
                 mode=None,
                 logDir="",
                 logLevel=None,
                 forceRefresh=None):
        self.order = order
        self.wallpaperPaths = wallpaperPaths
        self.interval = interval
        self.cacheDir = cacheDir
        self.backend = backend
        self.configFiles = configFiles
        self.mode = mode
        self.logDir = logDir
        self.logLevel = logLevel
        self.forceRefresh = forceRefresh

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

        if other.logDir != default.logDir:
            self.logDir = other.logDir

        if other.logLevel != default.logLevel:
            self.logLevel = other.logLevel

        if other.forceRefresh != default.forceRefresh:
            self.forceRefresh = other.forceRefresh

        return self

    @classmethod
    def fromCfgFile(cls, parsed):
        _logger.info("Producing RuntimeConfig from configuration file.")
        ret = RuntimeConfig()
        appConf = parsed[cls._ConfigFileKeys.rootSection.value]

        val = appConf.get(cls._ConfigFileKeys.order.value)
        if val is not None:
            if val not in UpdaterTypes.choices():
                raise InvalidSortOrderException(val, UpdaterTypes.choices())
            ret.order = val

        val = appConf.get(cls._ConfigFileKeys.wallpaperPaths.value)
        if val is not None:
            ret.wallpaperPaths = [p.strip() for path in val.split('\n') for p in path.split(':')]

        val = appConf.get(cls._ConfigFileKeys.interval.value)
        if val is not None:
            ret.interval = Intervals.Interval(val)

        val = appConf.get(cls._ConfigFileKeys.cacheDir.value)
        if val is not None:
            ret.cacheDir = val

        val = appConf.get(cls._ConfigFileKeys.backend.value)
        if val is not None:
            ret.backend = val

        val = appConf.get(cls._ConfigFileKeys.logDir.value)
        if val is not None:
            ret.logDir = val

        val = appConf.get(cls._ConfigFileKeys.logLevel.value)
        if val is not None:
            ret.logLevel = levelFromName(val)

        val = appConf.get(cls._ConfigFileKeys.forceRefresh.value)
        if val is not None:
            ret.forceRefresh = _properBoolFromString(val)

        return ret

    @staticmethod
    def fromProgramArgs(argsConf):
        _logger.info("Producing RuntimeConfig from runtime arguments.")
        ret = RuntimeConfig()

        if argsConf.order is not None and argsConf.order != "":
            ret.order = argsConf.order

        if argsConf.img_path is not None and argsConf.img_path != []:
            ret.wallpaperPaths = argsConf.img_path

        if argsConf.interval is not None:
            ret.interval = argsConf.interval

        if argsConf.cache_dir is not None and argsConf.cache_dir != "":
            ret.cacheDir = argsConf.cache_dir

        if argsConf.backend is not None and argsConf.backend != "":
            ret.backend = argsConf.backend

        if argsConf.config is not None and argsConf.config != []:
            ret.configFiles = [argsConf.config]

        if argsConf.generate_config is not None:
            ret.mode = Modes.GenerateConfig

        if argsConf.log_dir is not None:
            ret.logDir = argsConf.log_dir

        if argsConf.log_level is not None:
            ret.logLevel = levelFromName(argsConf.log_level)

        if argsConf.force_refresh is not None:
            ret.forceRefresh = bool(argsConf.force_refresh)

        return ret

    def __eq__(self, other):
        return (self.order == other.order and self.wallpaperPaths == other.wallpaperPaths
                and self.interval == other.interval and self.cacheDir == other.cacheDir
                and self.backend == other.backend and self.configFiles == other.configFiles
                and self.mode == other.mode and self.logDir == other.logDir
                and self.logLevel == other.logLevel and self.forceRefresh == other.forceRefresh)

    def __str__(self):
        ret = "[{root}]\n".format(root=self._ConfigFileKeys.rootSection.value)
        if self.order != "":
            ret += self.__strPrep(self._ConfigFileKeys.order.value, self.order)
        if self.wallpaperPaths != []:
            ret += self.__strPrep(self._ConfigFileKeys.wallpaperPaths.value,
                                  ":".join(self.wallpaperPaths))
        if self.interval is not None:
            ret += self.__strPrep(self._ConfigFileKeys.interval.value, str(self.interval))
        if self.cacheDir != "":
            ret += self.__strPrep(self._ConfigFileKeys.cacheDir.value, self.cacheDir)
        if self.backend != "":
            ret += self.__strPrep(self._ConfigFileKeys.backend.value, self.backend)
        if self.logDir != "":
            ret += self.__strPrep(self._ConfigFileKeys.logDir.value, self.logDir)
        if self.logLevel is not None:
            ret += self.__strPrep(self._ConfigFileKeys.logLevel.value, nameFromLevel(self.logLevel))
        if self.forceRefresh is not None:
            ret += self.__strPrep(self._ConfigFileKeys.forceRefresh.value, self.forceRefresh)
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

def _properBoolFromString(val):
    return val.lower() in ['true', '1', 't', 'y', 'yes']

