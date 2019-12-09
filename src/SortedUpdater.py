# SortedUpdater

from src.detail.BaseUpdater import BaseUpdater
from WallCollection import WallCollection
import enum
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
            where = bisect.bisect(walls.collection, i, lo=where)
            if (where <= walls.nextWall):
                walls.nextWall += 1
            walls.collection.insert(where, i)
