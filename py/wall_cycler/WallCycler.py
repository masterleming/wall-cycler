# WallCycler

from .Interval.ExpirationCheck import ExpirationCheck, AlwaysExpired, NeverExpires
from .Interval.TimestampStore import TimestampStore

from .Wallpapers.FileScanner import FileScanner
from .Wallpapers.WallCollection import WallCollection
from .Wallpapers.CollectionChecker import CollectionChecker

import enum
from logging import getLogger

_logger = getLogger(__name__)


class _CacheKeys(enum.Enum):
    wallpapers = "wallpapers"
    lastWallpaper = "last wallpaper"


class WallCycler:
    def __init__(self, dataStore, interval, updater, scheduler, backend, scanPaths, forceReload):
        self._dataStore = dataStore
        self._interval = interval
        self._updater = updater
        self._scheduler = scheduler
        self._backend = backend
        self._scanPaths = scanPaths
        self._forceReload = forceReload
        self._wallpapers = None
        self._expiryChecker = self.__createExpirationChecker()

    def run(self):
        _logger.info("Executing WallCycler.")

        self._loadCachedWallpapers()

        while True:
            self._updateWallpapers()

            if self._checkExpiration():
                self._changeWallpaper()
            else:
                self._reloadWallpaper()

            if not self._sleepOrBreak():
                break

        self.__updateWallpaperCache()
        return 0

    def check(self, remove=False):
        _logger.info("Checking collection for missing files.")

        self._loadCachedWallpapers()
        self._updateWallpapers()

        CollectionChecker(self._wallpapers).check(remove)

        if(remove):
            self.__updateWallpaperCache()

        return 0

    def _loadCachedWallpapers(self):
        _logger.info("Loading cached wallpaper collection.")
        with self._dataStore:
            self._wallpapers = self._dataStore.db.get(_CacheKeys.wallpapers.value,
                                                      default=WallCollection())

    def _updateWallpapers(self):
        _logger.info("Scanning configured paths for new wallpapers.")

        wallpapers = []
        for path, scanSubdirs in self._scanPaths:
            wallpapers += FileScanner(path, subdirs=scanSubdirs).scan()

        self._updater.update(self._wallpapers, wallpapers)
        self.__updateWallpaperCache()

    def _checkExpiration(self):
        _logger.info("Checking expiration.")
        return self._expiryChecker.isExpired()

    def _changeWallpaper(self, mark=True):
        wallpaper = next(self._wallpapers)
        _logger.info("Changing wallpaper to: '{}'".format(wallpaper))

        self._backend(str(wallpaper))

        self.__updateWallpaperCache(str(wallpaper))
        if mark:
            self._expiryChecker.mark()

    def _reloadWallpaper(self):
        if self._forceReload:
            _logger.debug("Reloading last wallpaper.")
            with self._dataStore:
                lastWallpaper = self._dataStore.db.get(_CacheKeys.lastWallpaper.value, default=None)

            if lastWallpaper is None:
                _logger.warning("Cannot reload wallpaper, no previous wallpaper is know.")
                self._changeWallpaper(False)
                return

            _logger.info("Reloading wallpaper '{}'.".format(lastWallpaper))
            self._backend(str(lastWallpaper))

    def _sleepOrBreak(self):
        _logger.info("Setting scheduler.")

        if self._scheduler is None:
            _logger.info("No scheduler present. Quitting.")
            return False

        nextChange = self._expiryChecker.getNext()
        if nextChange is None:
            _logger.info("Time of next change is unknown. Quitting.")
            return False

        _logger.info("Scheduling next change.")
        self._scheduler.wait(nextChange)
        return True

    def __createExpirationChecker(self):
        if self._scheduler is not None:
            return ExpirationCheck(self._interval, TimestampStore(self._dataStore))

        if self._forceReload:
            return NeverExpires(self._interval, TimestampStore(self._dataStore))

        return AlwaysExpired(self._interval, TimestampStore(self._dataStore))

    def __updateWallpaperCache(self, wallpaper=None):
        _logger.info("Updating cache of wallpapers collection.")
        with self._dataStore:
            self._dataStore[_CacheKeys.wallpapers.value] = self._wallpapers
            if wallpaper is not None:
                self._dataStore[_CacheKeys.lastWallpaper.value] = wallpaper
