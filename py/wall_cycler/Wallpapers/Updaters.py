# Updaters

from .WallCollection import WallCollection
from wall_cycler.exceptions import InvalidSortOrderException

import bisect
import enum
import random


class UpdaterTypes(enum.Enum):
    sorted = enum.auto()
    shuffle = enum.auto()

    @classmethod
    def choices(cls):
        return [e.name for e in cls]


def Updater(prototype):
    updaterType = UpdaterTypes[prototype]
    if updaterType is UpdaterTypes.sorted:
        return SortedUpdater()
    elif updaterType is UpdaterTypes.shuffle:
        return ShuffleUpdater()
    raise InvalidSortOrderException(prototype, UpdaterTypes.choices())


class BaseUpdater:
    def __init__(self):
        pass

    def update(self, walls, images):
        return NotImplemented


class ShuffleUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()

    def update(self, walls, images):
        tmpCollection = set(walls.collection)
        images = [i for i in images if i not in tmpCollection]
        if len(images) == 0:
            return

        random.shuffle(images)
        if len(walls.collection) == 0:
            walls.collection = images
            walls.nextWall = 0
            return

        where = 0
        for i in images[:-1]:
            where = random.randrange(0, len(walls.collection))
            if (where <= walls.nextWall):
                walls.nextWall += 1
            walls.collection.insert(where, i)

        walls.collection.insert(walls.nextWall, images[-1])


class SortedUpdater(BaseUpdater):
    def __init__(self):
        super().__init__()

    def update(self, walls, images):
        sImages = sorted(images)
        if len(walls.collection) == 0:
            walls.collection = sImages
            walls.nextWall = 0
            return

        where = 0
        for img in sImages:
            where = bisect.bisect_left(walls.collection, img, lo=where)
            if where < len(walls.collection) and walls.collection[where] == img:
                continue
            if (where <= walls.nextWall):
                walls.nextWall += 1
            walls.collection.insert(where, img)
