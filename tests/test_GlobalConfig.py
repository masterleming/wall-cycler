# test_GlobalConfig

import unittest

from wall_cycler.Config.GlobalConfig import GlobalConfig


class GlobalConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testInstance = "Test config instance!"

    def setUp(self):
        GlobalConfig._GlobalConfig__instance = None

    def test_000_gettingWithoutSetting(self):
        uut = GlobalConfig.get()
        self.assertIsNone(uut)

    def test_setConfig(self):
        GlobalConfig.set(self.testInstance)
        self._assertConfig(GlobalConfig._GlobalConfig__instance)

    def test_gettingConfig(self):
        GlobalConfig._GlobalConfig__instance = self.testInstance

        uut = GlobalConfig.get()

        self._assertConfig(uut)

    def test_setGetConfig(self):
        conf = GlobalConfig()
        conf.set(self.testInstance)
        self._assertConfig(conf.get())
        self._assertConfig(GlobalConfig.get())

    def test_overwriteConfig(self):
        uut1 = GlobalConfig()
        uut1.set(self.testInstance)
        self._assertConfig(GlobalConfig.get())

        newConfig = "something new!"
        uut2 = GlobalConfig()
        uut2.set(newConfig)
        self._assertConfig(GlobalConfig.get(), newConfig)

        self.assertIs(uut1.get(), uut2.get())

    def _assertConfig(self, otherInstance, correct=None):
        if correct is None:
            self.assertIs(otherInstance, self.testInstance)
        else:
            self.assertIs(otherInstance, correct)


if __name__ == '__main__':
    unittest.main()
