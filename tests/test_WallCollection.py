# test_WallCollection

from WallCollection import WallCollection

import unittest


class Test_TestWallCollection(unittest.TestCase):
    def test_updateEmptyCollection(self):
        filesCnt = 50
        files = self._prepareSomeFileNames(filesCnt)

        wc = WallCollection()
        wc.update(files)

        self.assertEqual(wc.collection, files)

    def test_getNext(self):
        filesCnt = 50
        files = self._prepareSomeFileNames(filesCnt)

        wc = WallCollection()
        wc.update(files)
        for f in files:
            wall = wc.next()
            self.assertEqual(wall, f)

    def test_getUpdateNotEmpty(self):
        filesCnt = 100
        files = self._prepareSomeFileNames(filesCnt)
        filesA = files[:filesCnt // 2]
        filesB = files[filesCnt // 2:]
        filesAlen = len(filesA)

        wc = WallCollection()
        wc.update(filesA)
        for _ in range(len(filesA) // 2):
            wc.next()

        wc.update(filesB)

        expected = filesA[:filesAlen // 2] + filesB + filesA[filesAlen // 2:]
        self.assertEqual(wc.collection, expected)

    @staticmethod
    def _prepareSomeFileNames(count):
        return ["file-%02d.jpg" % n for n in range(1, count + 1)]


if __name__ == '__main__':
    unittest.main()
