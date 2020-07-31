# test_ArgumentsParser

import sys
import unittest
import unittest.mock as mock

from TestSuite import TestSuite

from wall_cycler.Config.ArgumentsParser import ArgumentsParser
from wall_cycler.Wallpapers.Updaters import UpdaterTypes


class ArgumentsParserTests(TestSuite):
    def test_parsingOrder(self):
        basicArgv = ["test_parsingOrder", "--order"]
        validOrders = UpdaterTypes.choices()
        invalidOrders = ['truffle', 'reverse']

        for order in validOrders:
            sys.argv = basicArgv + [order]
            uut = ArgumentsParser()
            conf = uut.parse()
            self._checkConfig(conf, order=order)

        for order in invalidOrders:
            sys.argv = basicArgv + [order]

            with mock.patch('argparse.ArgumentParser.exit', ArgumentsParserTests._MockExit.exit):
                uut = ArgumentsParser()
                with self.assertRaises(ArgumentsParserTests._MockExit) as raised:
                    uut.parse()
                self.assertNotEqual(raised.exception.status, 0)
                self.assertIn(order, raised.exception.message)

    def test_parsingImagePath(self):
        basicArgv = ["test_parsingImagePath", "--img-path"]
        paths = ['imgs/', '~/wallpapers', '$HOME/Pictures']

        for path in paths:
            sys.argv = basicArgv + [path]
            uut = ArgumentsParser()
            conf = uut.parse()
            self._checkConfig(conf, imgDirs=[path])

    def test_parsingMultipleImagePaths(self):
        basicArgv = ["test_parsingMultipleImagePaths"]
        paths = ['imgs/', '~/wallpapers', '$HOME/Pictures']

        argv = basicArgv[:]
        for path in paths:
            argv.append("--img-path")
            argv.append(path)

        sys.argv = argv
        uut = ArgumentsParser()
        conf = uut.parse()
        self._checkConfig(conf, imgDirs=paths)

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
            self.assertEqual(config.wallpaperPaths, imgDirs)

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

    class _MockExit(Exception):
        def __init__(self, status, message):
            self.status = status
            self.message = message

        @classmethod
        def exit(cls, status=0, message=None):
            raise cls(status, message)


if __name__ == '__main__':
    unittest.main()
