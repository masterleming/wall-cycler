from FileScanner import FileScanner

import unittest
import os.path

TEST_IMAGES = ["test.jpg", "avatar/avatar_krzychu.png", "some_dir/test.png"]
TEST_IMAGES_BASE_DIR = "assets/tests/img"
TEST_IMAGES_IN_BASE_DIR = [TEST_IMAGES[0]]


class Test_TestFileScanner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.testDir = os.path.abspath(TEST_IMAGES_BASE_DIR)
        cls.testImages = [
            os.path.abspath(os.path.join(TEST_IMAGES_BASE_DIR, f))
            for f in TEST_IMAGES
        ]
        cls.testImages.sort()

    def setUp(self):
        self.assertTrue(os.path.exists(self.testDir))

    def test_scanWithSubdirs(self):
        uut = FileScanner(TEST_IMAGES_BASE_DIR)

        images = uut.scan()
        images.sort()

        self.assertEqual(images, self.testImages)
        for i in images:
            self.assertTrue(os.path.exists(i))

    def test_scanWithoutSubdirs(self):
        uut = FileScanner(TEST_IMAGES_BASE_DIR, False)

        images = uut.scan()
        images.sort()

        expectedFilesInBaseDir = [
            os.path.abspath(os.path.join(TEST_IMAGES_BASE_DIR, f))
            for f in TEST_IMAGES_IN_BASE_DIR
        ]
        self.assertEqual(images, expectedFilesInBaseDir)
        for i in images:
            self.assertTrue(os.path.exists(i))


if __name__ == '__main__':
    unittest.main()
