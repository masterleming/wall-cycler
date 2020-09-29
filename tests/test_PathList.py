# test_PathList.py

from wall_cycler.Config.PathList import PathList

from TestSuite import TestSuite

from tempfile import TemporaryDirectory
import os
import os.path
from random import shuffle


class PathListTests(TestSuite):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._prepareTestDirTree()

    @classmethod
    def tearDownClass(cls):
        cls._tempDir.cleanup()
        super().tearDownClass()

    def test_addSinglePathWithoutSpecs(self):
        testCases, _ = self._prepareTestCases(self._createdPaths, False)

        uut = PathList()
        for path in testCases:
            uut.addFromString(path)

        self._assertBasicPathList(uut)

    def test_addSinglePathWithSpecs(self):
        testCases, insertionSequence = self._prepareTestCases(self._createdPaths, True)

        uut = PathList()
        for path in testCases:
            uut.addFromString(path)

        self._assertPathList(uut, insertionSequence)

    def test_addMultiplePathsInOneStringWithoutSpecs(self):
        testCases, _ = self._prepareTestCases(self._createdPaths, False)
        bulkSpec = ":".join(testCases)
        uut = PathList()
        uut.addFromString(bulkSpec)

        self._assertBasicPathList(uut)

    def test_addMultiplePathsInOneStringWithSpecs(self):
        testCases, insertionSequence = self._prepareTestCases(self._createdPaths, True)
        bulkSpec = ":".join(testCases)
        uut = PathList()
        uut.addFromString(bulkSpec)

        self._assertPathList(uut, insertionSequence)

    def test_withErroneousPaths(self):
        correctPaths, expectedOutput = self._prepareTestCases(self._createdPaths, True)
        invalidPaths = ["X", "r@X/1" "Y", "s@Y/2"]
        testCases = correctPaths + invalidPaths
        shuffle(testCases)

        uut = PathList()
        uut.addFromString(":".join(testCases))

        self._assertPathList(uut, expectedOutput)

    def test_overwritingPaths(self):
        testCases = [os.path.join(self._tempDir.name, p) for p in ["A", "B"]]
        testSingle = ["s@" + case for case in testCases]
        singleExpected = {case: False for case in testCases}

        uut1 = PathList()
        uut1.addFromString(":".join(testSingle))
        self._assertPathList(uut1, singleExpected)

        testRecursive = ["r@" + case for case in testCases]
        recursiveExpected = {case: True for case in testCases}
        for case in testRecursive:
            uut1.addFromString(case)
        self._assertPathList(uut1, recursiveExpected)

        uut2 = PathList()
        for case in testRecursive:
            uut2.addFromString(case)
        self._assertPathList(uut2, recursiveExpected)

        uut2.addFromString(":".join(testSingle))
        self._assertPathList(uut2, singleExpected)

    def _assertBasicPathList(self, uut):
        for proto, inserted in zip(sorted(self._createdPaths), sorted(uut._paths.keys())):
            self.assertTrue(os.path.samefile(proto, inserted))

    def _assertPathList(self, uut, insertionSequence):
        self.assertEqual(len(insertionSequence), len(uut._paths))
        for path, specs in uut:
            self.assertIn(path, insertionSequence)
            self.assertEqual(specs, insertionSequence[path])

    @classmethod
    def _prepareTestCases(self, proto=[], withSpecs=False):
        insertionMemory = {}
        testCases = []
        for i, path in enumerate(proto):
            if withSpecs:
                if i % 2 == 0:
                    _path = "r@" + path
                else:
                    _path = "s@" + path
            else:
                _path = path
            testCases.append(_path)
            insertionMemory[os.path.normpath(path)] = (i % 2 == 0)

        return testCases, insertionMemory

    @classmethod
    def _prepareTestDirTree(cls):
        cls._tempDir = TemporaryDirectory()
        tempPaths = [
            "A", "A/1", "A/1/a", "A/1/b", "A/2", "A/3", "B/", "B/1/", "B/1/a/", "B/1/b/", "B/2/",
            "C"
        ]
        cls._createdPaths = [os.path.join(cls._tempDir.name, path) for path in tempPaths]

        for path in cls._createdPaths:
            os.makedirs(path, exist_ok=True)
