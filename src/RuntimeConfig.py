# RuntimeConfig

from Interval import Interval

class RuntimeConfig:
    def __init__(self):
        self.order = ""
        self.wallpaperPaths = []
        self.interval = None
        self.cacheDir = ""
        self.backend = ""

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

    @staticmethod
    def fromCfgFile(parsed):
        ret = RuntimeConfig()
        wloopConf = parsed['wloop']

        val = wloopConf.get('order')
        if val is not None:
            ret.order = val

        val = wloopConf.get('wallpaper paths')
        if val is not None:
            ret.wallpaperPaths = [
                p.strip() for path in val.split('\n') for p in path.split(':')
            ]

        val = wloopConf.get('change time')
        if val is not None:
            ret.interval = Interval(val)

        val = wloopConf.get('cache dir')
        if val is not None:
            ret.cacheDir = val

        val = wloopConf.get('wallpaper backend')
        if val is not None:
            ret.backend = val

    @staticmethod
    def fromProgramArgs(argsConf):
        ret = RuntimeConfig()

        if argsConf.order is not None and argsConf.order is not "":
            ret.order = argsConf.order

        if argsConf.img_path is not None and argsConf.img_path is not []:
            ret.wallpaperPaths = argsConf.wallpaperPaths

        if argsConf.interval is not None:
            ret.interval = argsConf.interval

        if argsConf.cache_dir is not None and argsConf.cache_dir is not "":
            ret.cacheDir = argsConf.cache_dir

        if argsConf.backend is not None and argsConf.backend is not "":
            ret.backend = argsConf.backend

        return ret
