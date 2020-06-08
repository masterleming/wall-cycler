# test_CollectionChecker

import unittest
import unittest.mock as mock
from itertools import chain, islice
from copy import deepcopy

from wall_cycler.Wallpapers.WallCollection import WallCollection
from wall_cycler.Wallpapers.CollectionChecker import CollectionChecker


class CollectionCheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.fileList = [
            "Lorem.jpg", "ipsum.jpg", "dolor.jpg", "sit.jpg", "amet.jpg", "adipiscing.jpg",
            "elit.jpg", "Nunc.jpg", "consequat.jpg", "ultricies.jpg", "Suspendisse.jpg",
            "consectetur.jpg", "nisl.jpg", "sed.jpg", "metus.jpg", "convallis.jpg", "efficitur.jpg",
            "Integer.jpg", "non.jpg", "commodo.jpg", "dui.jpg", "potenti.jpg", "Pellentesque.jpg",
            "interdum.jpg", "at.jpg", "purus.jpg"
        ]

    def test_doesNotChangeOrderIfNoFileIsMissing(self):

        with mock.patch("os.path.exists", _OsPathExistMock(self.fileList).exists):
            referenceCollection = WallCollection(self.fileList)
            wallCollection = deepcopy(referenceCollection)

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

            referenceCollection.nextWall = len(self.fileList) // 2
            wallCollection = deepcopy(referenceCollection)

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

            referenceCollection.nextWall = len(self.fileList) - 1
            wallCollection = deepcopy(referenceCollection)

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_filtersFiles(self):
        halfTheFiles = [file for i, file in enumerate(self.fileList) if i % 2 == 0]
        with mock.patch("os.path.exists", _OsPathExistMock(halfTheFiles).exists):
            wallCollection = WallCollection(self.fileList)

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self.assertEquals(sorted(wallCollection.collection), sorted(halfTheFiles))

    def test_preservesOrderWhenFiltering(self):
        halfTheFiles = [file for i, file in enumerate(self.fileList) if i % 2 == 0]
        with mock.patch("os.path.exists", _OsPathExistMock(halfTheFiles).exists):
            referenceCollection = WallCollection(halfTheFiles)
            wallCollection = WallCollection(self.fileList)

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

            referenceCollection.nextWall = len(referenceCollection.collection) // 2
            wallCollection = WallCollection(self.fileList)
            wallCollection.nextWall = wallCollection.collection.index(
                referenceCollection.collection[referenceCollection.nextWall])

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

            referenceCollection.nextWall = len(referenceCollection.collection) - 1
            wallCollection = WallCollection(self.fileList)
            wallCollection.nextWall = wallCollection.collection.index(
                referenceCollection.collection[referenceCollection.nextWall])

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_whatHappensWhenNextWallIsFilteredOut_wasFirst(self):
        filtered = self.fileList[1:]
        with mock.patch("os.path.exists", _OsPathExistMock(filtered).exists):
            referenceCollection = WallCollection(filtered)
            referenceCollection.nextWall = 0
            wallCollection = WallCollection(self.fileList)
            wallCollection.nextWall = 0

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_whatHappensWhenNextWallIsFilteredOut_wasInTheMiddle(self):
        pos = len(self.fileList) // 2
        filtered = self.fileList[:pos] + self.fileList[pos + 1:]
        with mock.patch("os.path.exists", _OsPathExistMock(filtered).exists):
            referenceCollection = WallCollection(filtered)
            referenceCollection.nextWall = pos
            wallCollection = WallCollection(self.fileList)
            wallCollection.nextWall = pos

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_whatHappensWhenNextWallIsFilteredOut_wasLast(self):
        pos = len(self.fileList) - 1
        filtered = self.fileList[:pos]
        with mock.patch("os.path.exists", _OsPathExistMock(filtered).exists):
            referenceCollection = WallCollection(filtered)
            referenceCollection.nextWall = 0
            wallCollection = WallCollection(self.fileList)
            wallCollection.nextWall = pos

            with CollectionChecker(wallCollection) as uut:
                uut.check()
            self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_chunkWasDeleted_inFront(self):
        start = 0
        stop = len(self.fileList) // 3
        filtered = self.fileList[stop:]
        with mock.patch("os.path.exists", _OsPathExistMock(filtered).exists):
            for i in range(start, stop):
                referenceCollection = WallCollection(filtered)
                referenceCollection.nextWall = 0
                wallCollection = WallCollection(self.fileList)
                wallCollection.nextWall = i

                with CollectionChecker(wallCollection) as uut:
                    uut.check()
                self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_chunkWasDeleted_inTheMiddle(self):
        start = len(self.fileList) // 3
        stop = 2 * start
        filtered = self.fileList[:start] + self.fileList[stop:]
        with mock.patch("os.path.exists", _OsPathExistMock(filtered).exists):
            for i in range(start, stop):
                referenceCollection = WallCollection(filtered)
                referenceCollection.nextWall = start
                wallCollection = WallCollection(self.fileList)
                wallCollection.nextWall = i

                with CollectionChecker(wallCollection) as uut:
                    uut.check()
                self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_chunkWasDeleted_inTheBack(self):
        start = (2 * len(self.fileList)) // 3
        stop = len(self.fileList) - 1
        filtered = self.fileList[:start]
        with mock.patch("os.path.exists", _OsPathExistMock(filtered).exists):
            for i in range(start, stop):
                referenceCollection = WallCollection(filtered)
                referenceCollection.nextWall = start
                wallCollection = WallCollection(self.fileList)
                wallCollection.nextWall = i

                with CollectionChecker(wallCollection) as uut:
                    uut.check()
                self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def test_chunkWasDeleted_spansFromBackToFront(self):
        length = len(self.fileList)
        start = (5 * length) // 6
        stop = length // 6
        filtered = self.fileList[stop:start]
        checkRange = list(range(start, length)) + list(range(0, stop))
        with mock.patch("os.path.exists", _OsPathExistMock(filtered).exists):
            for i in checkRange:
                referenceCollection = WallCollection(filtered)
                referenceCollection.nextWall = start
                wallCollection = WallCollection(self.fileList)
                wallCollection.nextWall = i

                with CollectionChecker(wallCollection) as uut:
                    uut.check()
                self._assertWallCollectionsAreEqual(wallCollection, referenceCollection)

    def _assertWallCollectionsAreEqual(self, first, second):
        firstNormalised = list(self.__collectionIterator(first))
        secondNormalised = list(self.__collectionIterator(second))

        self.assertEquals(firstNormalised, secondNormalised)

    @staticmethod
    def __collectionIterator(wallCollection):
        start = wallCollection.nextWall
        return chain(islice(wallCollection.collection, start, None),
                     islice(wallCollection.collection, start))


class _OsPathExistMock:
    def __init__(self, existingList):
        self._existingList = existingList

    def exists(self, path):
        return path in self._existingList


if __name__ == '__main__':
    unittest.main()
