# ShuffleUpdater

from src.detail.BaseUpdater import BaseUpdater
from WallCollection import WallCollection
import random


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
