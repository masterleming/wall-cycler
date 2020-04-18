# RuntimeConfig

# TODO: substitute dotted submodule access with proper paths (top module name)
from wall_cycler.Interval import Intervals
import enum

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
                 backend=""):
        self.order = order
        self.wallpaperPaths = wallpaperPaths
        self.interval = interval
        self.cacheDir = cacheDir
        self.backend = backend

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

        return self

    @classmethod
    def fromCfgFile(cls, parsed):
        ret = RuntimeConfig()
        wloopConf = parsed[cls._ConfigFileKeys.rootSection.value]

        val = wloopConf.get(cls._ConfigFileKeys.order.value)
        if val is not None:
            ret.order = val

        val = wloopConf.get(cls._ConfigFileKeys.wallpaperPaths.value)
        if val is not None:
            ret.wallpaperPaths = [
                p.strip() for path in val.split('\n') for p in path.split(':')
            ]

        val = wloopConf.get(cls._ConfigFileKeys.interval.value)
        if val is not None:
            ret.interval = Intervals.Interval(val)

        val = wloopConf.get(cls._ConfigFileKeys.cacheDir.value)
        if val is not None:
            ret.cacheDir = val

        val = wloopConf.get(cls._ConfigFileKeys.backend.value)
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

        return ret

    def __eq__(self, other):
        return (self.order == other.order
                and self.wallpaperPaths == other.wallpaperPaths
                and self.interval == other.interval
                and self.cacheDir == other.cacheDir
                and self.backend == other.backend)

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

    @staticmethod
    def __strPrep(key, value):
        return "{key} = {value}\n".format(key=key, value=value)
