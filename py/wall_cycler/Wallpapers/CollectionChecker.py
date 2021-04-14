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

    def check(self, remove):
        _logger.info("Checking collection.")

        nextWall = self._collection.nextWall

        shiftedCollectionIterator = itertools.chain(
            itertools.islice(self._collection.collection, nextWall, None),
            itertools.islice(self._collection.collection, nextWall))

        def partition(iterable):
            hits = []
            misses = []

            for f in iterable:
                if os.path.exists(f):
                    hits.append(f)
                else:
                    misses.append(f)

            return hits, misses

        existing, missing = partition(shiftedCollectionIterator)

        if len(missing) != 0:
            _logger.info(
                "Check complete, %d files were not found on disk and were removed from the collection.",
                len(missing))

            print("Files missing on disk:")
            for f in sorted(missing):
                print(f)

            if remove:
                self._collection.collection = existing
                self._collection.nextWall = 0
        else:
            _logger.info("Check complete, no files are missing.")
