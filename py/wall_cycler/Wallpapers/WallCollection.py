# WallCollection

from logging import getLogger

_logger = getLogger(__name__)


class WallCollection:
    def __init__(self, collection=[]):
        self.collection = collection
        self.nextWall = 0

    def __iter__(self):
        return self

    def __next__(self):
        _logger.info("Getting next wallpaper from collection.")
        if len(self.collection) == 0:
            _logger.warning("Empty collection.")
            raise StopIteration

        index = self.nextWall
        self.nextWall = (self.nextWall + 1) % len(self.collection)
        return self.collection[index]
