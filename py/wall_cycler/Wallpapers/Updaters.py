# Updaters

from .WallCollection import WallCollection
from ..exceptions import InvalidSortOrderException

import bisect
import enum
import random
from logging import getLogger

_logger = getLogger(__name__)


class UpdaterTypes(enum.Enum):
    sorted = enum.auto()
    shuffle = enum.auto()

    @classmethod
    def choices(cls):
        return [e.name for e in cls]


def Updater(prototype):
    _logger.info("Creating updater.")
    updaterType = UpdaterTypes[prototype]
    if updaterType is UpdaterTypes.sorted:
        return SortedUpdater()
    elif updaterType is UpdaterTypes.shuffle:
        return ShuffleUpdater()

    _logger.error("Invalid updater specification: '%s'!", prototype)
    raise InvalidSortOrderException(prototype, UpdaterTypes.choices())


class BaseUpdater:
    def __init__(self):
        pass

    def update(self, walls, images):
        return NotImplemented


class ShuffleUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()
        _logger.info("ShuffleUpdater created.")

    def update(self, walls, images):
        _logger.info("ShuffleUpdater working.")

        tmpCollection = set(walls.collection)
        images = [i for i in images if i not in tmpCollection]
        if len(images) == 0:
            _logger.info("No new images found. Finished.")
            return

        _logger.info("Found %d new images.", len(images))
        random.shuffle(images)

        if len(walls.collection) == 0:
            _logger.info("Collection is empty. Overwriting collection.")
            walls.collection = images
            walls.nextWall = 0
            return

        _logger.info("Adding images to collection.")
        where = 0
        for i in images[:-1]:
            where = random.randrange(0, len(walls.collection))
            if (where <= walls.nextWall):
                walls.nextWall += 1
            walls.collection.insert(where, i)

        walls.collection.insert(walls.nextWall, images[-1])
        _logger.info("Collection updated.")


class SortedUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()
        _logger.info("SortedUpdater created.")

    def update(self, walls, images):
        _logger.info("SortedUpdater working.")

        sImages = sorted(images)
        if len(walls.collection) == 0:
            _logger.info("Collection is empty. Overwriting collection.")
            walls.collection = sImages
            walls.nextWall = 0
            return

        where = 0
        count = 0
        for img in sImages:
            where = bisect.bisect_left(walls.collection, img, lo=where)
            if where < len(walls.collection) and walls.collection[where] == img:
                _logger.debug("Image already in collection, skipping.")
                continue
            if (where <= walls.nextWall):
                walls.nextWall += 1
            walls.collection.insert(where, img)
            count += 1
        _logger.info("Inserted %d images.", count)
