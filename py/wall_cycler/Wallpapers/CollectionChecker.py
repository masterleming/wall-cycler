# CollectionChecker

from .WallCollection import WallCollection

import os.path
import itertools


class CollectionChecker:
    def __init__(self, collection):
        self._collection = collection

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def check(self):
        nextWall = self._collection.nextWall

        shiftedCollectionIterator = itertools.chain(
            itertools.islice(self._collection.collection, nextWall, None),
            itertools.islice(self._collection.collection, nextWall))

        self._collection.collection = list(filter(os.path.exists, shiftedCollectionIterator))
        self._collection.nextWall = 0
