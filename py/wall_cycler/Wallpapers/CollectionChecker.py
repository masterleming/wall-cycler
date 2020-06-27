# CollectionChecker

from .WallCollection import WallCollection

import os.path
import itertools
from logging import getLogger

_logger = getLogger(__name__)


class CollectionChecker:
    def __init__(self, collection):
        self._collection = collection

    def __enter__(self):
        return self

    def __exit__(self, type, value, tb):
        pass

    def check(self):
        _logger.info("Checking collection.")
        originalSize = len(self._collection.collection)

        nextWall = self._collection.nextWall

        shiftedCollectionIterator = itertools.chain(
            itertools.islice(self._collection.collection, nextWall, None),
            itertools.islice(self._collection.collection, nextWall))

        self._collection.collection = list(filter(os.path.exists, shiftedCollectionIterator))
        self._collection.nextWall = 0

        filteredSize = len(self._collection.collection)
        if filteredSize != originalSize:
            _logger.warning(
                "Check complete, %d files were not found on disk and were removed from the collection.",
                originalSize - filteredSize)
        else:
            _logger.info("Check complete, no files are missing.")
