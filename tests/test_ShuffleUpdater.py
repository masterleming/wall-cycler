# test_ShuffleUpdater

from wall_cycler.Wallpapers.Updaters import ShuffleUpdater
from wall_cycler.Wallpapers.WallCollection import WallCollection

import unittest
import random

PROTO_FILE_LIST = "Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima Mike " \
    "November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu"
FILE_LIST = PROTO_FILE_LIST.split(' ')

TEST_ITERATIONS = 1000


class ShuffleUpdaterTests(unittest.TestCase):
    def setUp(self):
        self.walls = WallCollection()

    def test_updateEmptyCollectionWithSortedFiles(self):
        images = self._getSortedFiles()

        for _ in range(TEST_ITERATIONS):
            self.walls = WallCollection()

            uut = ShuffleUpdater()
            uut.update(self.walls, images)

            self.assertNotEqual(self.walls.collection, images)
            self.assertEqual(sorted(self.walls.collection), images)

    def test_updateEmptyCollectionWithRandomFiles(self):
        images = self._getRandomFiles()

        for _ in range(TEST_ITERATIONS):
            self.walls = WallCollection()

            uut = ShuffleUpdater()
            uut.update(self.walls, images)

            self.assertNotEqual(self.walls.collection, images)
            self.assertNotEqual(sorted(self.walls.collection), images)
            self.assertNotEqual(self.walls.collection, sorted(images))
            self.assertEqual(sorted(self.walls.collection), sorted(images))

    def test_updatingDoesNotAlterOriginalList(self):
        images = self._getSortedFiles()
        backupImages = images[:]

        for _ in range(TEST_ITERATIONS):
            self.walls = WallCollection()

            uut = ShuffleUpdater()
            uut.update(self.walls, images)

            self.assertEqual(images, backupImages)
            self.assertNotEqual(images, self.walls.collection)
            self.assertEqual(images, sorted(self.walls.collection))

    def test_updateExisting(self):
        images = self._getSortedFiles()
        size = len(images)
        partSize = size // 2
        part1 = images[:partSize]
        part2 = images[partSize:]

        for _ in range(TEST_ITERATIONS):
            self.walls = WallCollection()
            self.walls.collection = part1[:]
            self.walls.nextWall = 0

            uut = ShuffleUpdater()
            uut.update(self.walls, part2)

            self.assertEqual(sorted(self.walls.collection), images)
            self._assertInitialPartHasNewItemsInserted(part1)
            self._assertInitialPartIsInOriginalOrder(part1)

    def test_updatingDoesAffectNextWall(self):
        images = self._getSortedFiles()
        count = len(images)
        partSize = count - count // 5
        self.assertGreater(partSize, 0)
        self.assertLess(partSize, count)
        part1 = images[partSize:]
        part2 = images[:partSize]

        for _ in range(TEST_ITERATIONS):
            self.walls = WallCollection()
            self.walls.collection = part1[:]
            self.walls.nextWall = random.randrange(len(self.walls.collection))
            nextWallVal = self.walls.collection[self.walls.nextWall]

            uut = ShuffleUpdater()
            uut.update(self.walls, part2)

            self.assertEqual(sorted(self.walls.collection), images)
            self.assertTrue(next(self.walls) in part2)
            self.assertEqual(next(self.walls), nextWallVal)

    def test_updatingEmptyDoesNotAffectNextWall(self):
        images = self._getSortedFiles()

        for _ in range(TEST_ITERATIONS):
            self.walls = WallCollection()
            self.walls.nextWall = 0

            uut = ShuffleUpdater()
            uut.update(self.walls, images)

            self.assertEqual(sorted(self.walls.collection), images)
            self.assertEqual(self.walls.nextWall, 0)

    def test_addOnlyUniqueEntries(self):
        images = self._getSortedFiles()
        tmpImages = images[:]
        count = len(tmpImages)
        selectionCnt = count // 5
        self.assertGreater(selectionCnt, 0)
        selection = tmpImages[:selectionCnt]
        tmpImages[:selectionCnt] = []
        selection += tmpImages[:selectionCnt]
        random.shuffle(selection)

        for _ in range(TEST_ITERATIONS):
            self.walls = WallCollection()
            self.walls.collection = tmpImages[:]
            self.walls.nextWall = 0

            uut = ShuffleUpdater()
            uut.update(self.walls, selection)

            self.assertEqual(sorted(self.walls.collection), images)

    def test_insertEmptyListToEmptyCollection(self):
        images = []

        for _ in range(TEST_ITERATIONS):
            uut = ShuffleUpdater()
            uut.update(self.walls, images)

            self.assertEqual(self.walls.collection, [])
            self.assertEqual(self.walls.nextWall, 0)

    def test_insertEmptyListToExistingCollection(self):
        images = self._getSortedFiles()
        empty = []
        self.walls.collection = images[:]

        for _ in range(TEST_ITERATIONS):
            self.walls.nextWall = random.randrange(len(self.walls.collection))
            nextWall = self.walls.nextWall

            uut = ShuffleUpdater()
            uut.update(self.walls, empty)

            self.assertEqual(self.walls.collection, images)
            self.assertEqual(self.walls.nextWall, nextWall)

    def _assertInitialPartHasNewItemsInserted(self, part):
        partStr = ' '.join(part)
        collectionStr = ' '.join(self.walls.collection)
        self.assertTrue(partStr not in collectionStr)

    def _assertInitialPartIsInOriginalOrder(self, part):
        lastPos = -1
        for p in part:
            pos = self.walls.collection.index(p)
            self.assertGreater(pos, lastPos)
            lastPos = pos

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
