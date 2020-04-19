# test_SortedUpdater

from wall_cycler.Wallpapers.SortedUpdater import SortedUpdater
from wall_cycler.Wallpapers.WallCollection import WallCollection

import unittest
import random

PROTO_FILE_LIST = "Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima Mike " \
    "November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu"
FILE_LIST = PROTO_FILE_LIST.split(' ')


class Test_TestSortedUpdater(unittest.TestCase):
    def setUp(self):
        self.walls = WallCollection()

    def test_updateEmptyCollectionWithSortedFiles(self):
        images = self._getSortedFiles()

        uut = SortedUpdater()
        uut.update(self.walls, images)

        self.assertEqual(self.walls.collection, images)

    def test_updateEmptyCollectionWithRandomFiles(self):
        images = self._getRandomFiles()

        uut = SortedUpdater()
        uut.update(self.walls, images)

        self.assertEqual(self.walls.collection, sorted(images))

    def test_updatingDoesNotAlterOriginalList(self):
        images = self._getRandomFiles()
        imagesCpy = images[:]

        uut = SortedUpdater()
        uut.update(self.walls, images)

        self.assertEqual(self.walls.collection, sorted(images))
        self.assertEqual(images, imagesCpy)
        self.assertNotEqual(self.walls.collection, images)

    def test_updateExisting(self):
        images = self._getRandomFiles()
        count = len(images)
        part1 = images[:count // 2]
        part2 = images[count // 2:]

        self.walls.collection = sorted(part1)

        uut = SortedUpdater()
        uut.update(self.walls, part2)

        self.assertEqual(self.walls.collection, sorted(part1 + part2))

    def test_updatingDoesNotAffectNextWall(self):
        images = self._getSortedFiles()
        count = len(images)
        partSize = count - count // 5
        self.assertGreater(partSize, 0)
        self.assertLess(partSize, count)
        part1 = images[partSize:]
        part2 = images[:partSize]
        self.walls.collection = part1[:]
        self.walls.nextWall = 0
        nextWallVal = self.walls.collection[self.walls.nextWall]

        uut = SortedUpdater()
        uut.update(self.walls, part2)

        self.assertEqual(self.walls.collection, images)
        self.assertEqual(next(self.walls), nextWallVal)

    def test_updatingEmptyDoesNotAffectNextWall(self):
        images = self._getRandomFiles()
        self.walls.nextWall = 0

        uut = SortedUpdater()
        uut.update(self.walls, images)

        self.assertEqual(self.walls.collection, sorted(images))
        self.assertEqual(self.walls.nextWall, 0)

    def test_addOnlyUniqueEntries(self):
        images = self._getRandomFiles()
        tmpImages = images[:]
        count = len(tmpImages)
        selectionCnt = count // 5
        self.assertGreater(selectionCnt, 0)
        selection = tmpImages[:selectionCnt]
        tmpImages[:selectionCnt] = []
        selection += tmpImages[:selectionCnt]
        random.shuffle(selection)

        self.walls.nextWall = 0
        self.walls.collection = sorted(tmpImages)

        uut = SortedUpdater()
        uut.update(self.walls, selection)

        self.assertEqual(self.walls.collection, sorted(images))

    def test_insertEmptyListToEmptyCollection(self):
        images = []

        uut = SortedUpdater()
        uut.update(self.walls, images)

        self.assertEqual(self.walls.collection, [])
        self.assertEqual(self.walls.nextWall, 0)

    def test_insertEmptyListToExistingCollection(self):
        images = self._getSortedFiles()
        empty = []
        self.walls.collection = images[:]

        for _ in range(1000):
            self.walls.nextWall = random.randrange(len(self.walls.collection))
            nextWall = self.walls.nextWall

            uut = SortedUpdater()
            uut.update(self.walls, empty)

            self.assertEqual(self.walls.collection, images)
            self.assertEqual(self.walls.nextWall, nextWall)

    @staticmethod
    def _getRandomFiles():
        f = FILE_LIST[:]
        random.shuffle(f)
        return f

    @staticmethod
    def _getSortedFiles():
        return sorted(FILE_LIST[:])


if __name__ == '__main__':
    unittest.main()
