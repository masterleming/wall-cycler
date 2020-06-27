# WallCycler

from wall_cycler.Interval.ExpirationCheck import ExpirationCheck
from wall_cycler.Interval.TimestampStore import TimestampStore

from wall_cycler.Wallpapers.FileScanner import FileScanner
from wall_cycler.Wallpapers.WallCollection import WallCollection

import wall_cycler.exceptions as exceptions

import enum
from logging import getLogger

_logger = getLogger(__name__)


class _CacheKeys(enum.Enum):
    wallpapers = "wallpapers"


class WallCycler:
    def __init__(self, dataStore, interval, updater, scheduler, backend, scanPaths):
        self._dataStore = dataStore
        self._interval = interval
        self._updater = updater
        self._scheduler = scheduler
        self._backend = backend
        self._scanPaths = scanPaths
        self._wallpapers = None
        self._expiryChecker = self.__createExpirationChecker()

    def run(self):
        _logger.info("Executing WallCycler.")

        self._loadCachedWallpapers()

        while True:
            self._updateWallpapers()

            if self._checkExpiration():
                self._changeWallpaper()

            if not self._sleepOrBreak():
                break

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
        for path in self._scanPaths:
            # TODO add subdirs (somehow) to configuration
            wallpapers += FileScanner(path, subdirs=True).scan()

        self._updater.update(self._wallpapers, wallpapers)
        self.__updateWallpaperCache()

    def _checkExpiration(self):
        _logger.info("Checking expiration.")
        return self._expiryChecker.isExpired()

    def _changeWallpaper(self):
        wallpaper = next(self._wallpapers)
        _logger.info("Changing wallpaper to: '{}'".format(wallpaper))
        # TODO: change the wallpaper
        # TODO: implement changing wallpaper backends!

        self.__updateWallpaperCache()
        self._expiryChecker.mark()

    def _sleepOrBreak(self):
        _logger.info("Setting scheduler.")

        nextChange = self._expiryChecker.getNext()
        if nextChange is None:
            _logger.info("Time of next change is unknown. Quitting.")
            return False

        _logger.info("Scheduling next change.")
        self._scheduler.wait(nextChange)
        return True

    def __createExpirationChecker(self):
        return ExpirationCheck(self._interval, TimestampStore(self._dataStore))

    def __updateWallpaperCache(self):
        _logger.info("Updating cache of wallpapers collection.")
        with self._dataStore:
            self._dataStore[_CacheKeys.wallpapers.value] = self._wallpapers
