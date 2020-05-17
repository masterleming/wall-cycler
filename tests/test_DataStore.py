# test_DataStore

import unittest
from tempfile import TemporaryDirectory
import os.path

from wall_cycler.Config.RuntimeConfig import RuntimeConfig
from wall_cycler.DataStore import DataStore, DATASTORE_DB

TEST_CACHE_ROOT = '/tmp'
TEST_CACHE_TEMP_PREFIX = 'test-cache-'

TEST_DATA_PAIRS = [("number", 1234), ("text", "lorem ipsum"), ("object", {"A": 1, "B": 2})]


class Test_TestDataStore(unittest.TestCase):
    def test_storeAndRetrieve_explicitOpen(self):
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testDir:
            uut = DataStore(testDir)
            uut.open()
            for key, value in TEST_DATA_PAIRS:
                self.assertNotIn(key, uut.db)
                uut[key] = value

            for key, value in TEST_DATA_PAIRS:
                self.assertIn(key, uut.db)
                self.assertEqual(uut[key], value)
            uut.close()

            self._assertDbExists(testDir)

    def test_storeAndRetrieve_inDifferentExplicitOpens(self):
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testDir:
            uut1 = DataStore(testDir)
            uut1.open()
            for key, value in TEST_DATA_PAIRS:
                self.assertNotIn(key, uut1.db)
                uut1[key] = value
            uut1.close()

            self._assertDbExists(testDir)

            uut2 = DataStore(testDir)
            uut2.open()
            for key, value in TEST_DATA_PAIRS:
                self.assertIn(key, uut2.db)
                self.assertEqual(uut2[key], value)
            uut2.close()

            self._assertDbExists(testDir)

    def test_storeAndRetrieve_inContext(self):
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testDir:
            with DataStore(testDir) as uut:
                for key, value in TEST_DATA_PAIRS:
                    self.assertNotIn(key, uut.db)
                    uut[key] = value

                for key, value in TEST_DATA_PAIRS:
                    self.assertIn(key, uut.db)
                    self.assertEqual(uut[key], value)

            self._assertDbExists(testDir)

    def test_storeAndRetrieve_inDifferentContexts(self):
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testDir:
            with DataStore(testDir) as uut1:
                for key, value in TEST_DATA_PAIRS:
                    self.assertNotIn(key, uut1.db)
                    uut1[key] = value

            self._assertDbExists(testDir)

            with DataStore(testDir) as uut2:
                for key, value in TEST_DATA_PAIRS:
                    self.assertIn(key, uut2.db)
                    self.assertEqual(uut2[key], value)

            self._assertDbExists(testDir)

    def test_storeAndRetrieve_withoutExpliciteOpeningOrContextManager(self):
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testDir:
            uut = DataStore(testDir)
            self.assertEqual(uut.db, None)
            for key, value in TEST_DATA_PAIRS:
                uut[key] = value
            self.assertEqual(uut.db, None)

            self.assertEqual(uut.db, None)
            for key, value in TEST_DATA_PAIRS:
                self.assertEqual(uut[key], value)
            self.assertEqual(uut.db, None)

            self._assertDbExists(testDir)

    def test_storeAndRetrieve_withoutExpliciteOpeningOrContextManager_withDifferentInstances(self):
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testDir:
            uut1 = DataStore(testDir)
            self.assertEqual(uut1.db, None)
            for key, value in TEST_DATA_PAIRS:
                uut1[key] = value
            self.assertEqual(uut1.db, None)

            uut2 = DataStore(testDir)
            self.assertEqual(uut2.db, None)
            for key, value in TEST_DATA_PAIRS:
                self.assertEqual(uut2[key], value)
            self.assertEqual(uut2.db, None)

            self._assertDbExists(testDir)

    def test_creatingDirectoryIfDoesNotExistsBeforeOpeningCache(self):
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testBaseDir:

            testDir = os.path.join(testBaseDir, "very/long/extra/path/")
            self.assertFalse(os.path.exists(testDir))

            uut = DataStore(testDir)
            uut.open()

            self.assertTrue(os.path.exists(testDir))
            self._assertDbExists(testDir)

    def test_retrieveNonExistentEntry(self):
        testDefault = "I Solemnly Swear I Aim To Misbehave!"
        with TemporaryDirectory(prefix=TEST_CACHE_TEMP_PREFIX, dir=TEST_CACHE_ROOT) as testDir:
            with DataStore(testDir) as uut:
                for key, _ in TEST_DATA_PAIRS:
                    self.assertNotIn(key, uut.db)
                    try:
                        tmp = uut[key]
                    except KeyError as err:
                        self.assertIn(bytes(key, "ASCII"), err.args)

                for key, _ in TEST_DATA_PAIRS:
                    self.assertNotIn(key, uut.db)
                    tmp = uut.db.get(key, default=testDefault)
                    self.assertEqual(tmp, testDefault)

            self._assertDbExists(testDir)

    def _assertDbExists(self, cacheDir):
        cacheFile = os.path.join(cacheDir, DATASTORE_DB)
        self.assertTrue(os.path.exists(cacheFile))


if __name__ == '__main__':
    unittest.main()
