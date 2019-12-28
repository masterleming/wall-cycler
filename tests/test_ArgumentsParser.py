# test_ArgumentsParser

import unittest
import sys

from ArgumentsParser import ArgumentsParser

class Test_TestArgumentsParser(unittest.TestCase):

    def setUp(self):
        pass

    def test_parsingOrder(self):
        basicArgv = ["test_parsingOrder", "--order"]
        validOrders = ["shuffle", "sorted"]
        invalidOrders = ['truffle', 'reverse']

        for order in validOrders:
            sys.argv = basicArgv + [order]
            uut = ArgumentsParser()
            conf = uut.parse()
            self._checkConfig(conf, order=order)

        for order in invalidOrders:
            sys.argv = basicArgv + [order]
            uut = ArgumentsParser()
            # self.assertRaises()

    def _checkConfig(self,
                     config,
                     order=None,
                     imgDirs=None,
                     interval=None,
                     cacheDir=None,
                     backend=None,
                     configFile=None,
                     generateConfig=None):
        if order is not None:
            self.assertEqual(config.order, order)

        if imgDirs is not None:
            self.assertEqual(config.img_path, imgDirs)

        if interval is not None:
            self.assertEqual(config.interval, interval)

        if cacheDir is not None:
            self.assertEqual(config.cache_dir, cacheDir)

        if backend is not None:
            self.assertEqual(config.backend, backend)

        if configFile is not None:
            self.assertEqual(config.config, configFile)

        if generateConfig is not None:
            self.assertEqual(config.generate_config, generateConfig)


if __name__ == '__main__':
    unittest.main()
