from WallCollection import WallCollection

import unittest

class Test_TestWallCollection(unittest.TestCase):

    def setUp(self):
        self.wc = WallCollection()

    def test_updateEmptyCollection(self):
        print(self.wc)

if __name__ == '__main__':
    unittest.main()
