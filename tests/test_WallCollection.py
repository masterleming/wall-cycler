# test_WallCollection

from wall_cycler.Wallpapers.WallCollection import WallCollection

import unittest

from TestSuite import TestSuite


class WallCollectionTests(TestSuite):
    def test_getNext(self):
        filesCnt = 50
        files = self._prepareSomeFileNames(filesCnt)

        wc = WallCollection(files[:])

        for f in files:
            self.assertEqual(wc.__next__(), f)

    def test_iterator(self):
        filesCnt = 50
        files = self._prepareSomeFileNames(filesCnt)

        wc = WallCollection(files[:])
        i = iter(wc)

        for f in files:
            self.assertEqual(next(i), f)

    def test_emptyIteration(self):
        wc = WallCollection()

        l = [w for w in wc]
        self.assertEqual(l, [])

    def test_infiniteIteration(self):
        filesCnt = 50
        files = self._prepareSomeFileNames(filesCnt)

        wc = WallCollection(files[:])

        i = 0
        for w in wc:
            f = files[i % filesCnt]
            self.assertEqual(w, f)
            i += 1
            if i == 2 * filesCnt:
                break

    @staticmethod
    def _prepareSomeFileNames(count):
        return ["file-{:02d}.jpg".format(n) for n in range(1, count + 1)]


if __name__ == '__main__':
    unittest.main()
