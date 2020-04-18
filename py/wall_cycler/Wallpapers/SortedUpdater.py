# SortedUpdater

from .BaseUpdater import BaseUpdater
from .WallCollection import WallCollection

import bisect


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
        for i in sImages:
            where = bisect.bisect_left(walls.collection, i, lo=where)
            if where < len(walls.collection) and walls.collection[where] == i:
                continue
            if (where <= walls.nextWall):
                walls.nextWall += 1
            walls.collection.insert(where, i)
