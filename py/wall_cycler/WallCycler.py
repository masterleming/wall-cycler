# WallCycler

from wall_cycler.Interval.ExpirationCheck import ExpirationCheck
from wall_cycler.Interval.TimestampStore import TimestampStore

from wall_cycler.Wallpapers.FileScanner import FileScanner
from wall_cycler.Wallpapers.WallCollection import WallCollection

import wall_cycler.exceptions as exceptions

class WallCycler:
    def __init__(self, dataStore, interval, updater, backend, scanPaths):
        self._dataStore = dataStore
        self._interval = interval
        self._updater = updater
        self._backend = backend
        self._scanPaths = scanPaths
        self._wallpapers = None

    def run(self):
        self._loadCachedWallpapers()
        self._updateWallpapers()

        return 0

    def _loadCachedWallpapers(self):
        with self._dataStore:
            self._wallpapers = self._dataStore.db.get("wallpapers", default=WallCollection())

    def _updateWallpapers(self):
        wallpapers = []
        for path in self._scanPaths:
            # TODO add subdirs (somehow) to configuration
            wallpapers += FileScanner(path, subdirs=True).scan()

        self._updater.update(self._wallpapers, wallpapers)
        with self._dataStore:
            self._dataStore["wallpapers"] = self._wallpapers

    # def _checkExpiration(self):
    #     expiryChecker = ExpirationCheck(TimestampStore(self._config.cacheDir))  # TODO: think about using the data store rather than the path for initializing the TimestampStore
    #     expiryChecker.isExpired()
