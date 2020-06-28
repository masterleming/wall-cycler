# test_SwayBackend

from wall_cycler.Switchers.SwayBackend import SwayBackend
from wall_cycler.exceptions import SwitcherException, MissingDirectoryException

import unittest
import unittest.mock as mock
from subprocess import CompletedProcess

from TestSuite import TestSuite


class SwayBackendTests(TestSuite):

    __dummyWallpapers =[
        "Interdum/et/malesuada.jpg",
        "fames/ac/ante.jpg",
        "ipsum/primis/in.jpg",
        "faucibus/Proin/mattis.jpg",
        "bibendum/leo/id.jpg",
        "porttitor/Quisque/non.jpg",
        "nisl/non/magna.jpg",
        "fringilla/feugiat/Mauris.jpg",
        "convallis/ac/ipsum.jpg",
        "non/ornare/Quisque.jpg"
    ]

    def test_changeWallpaper(self):
        with mock.patch("subprocess.run", mock.Mock()) as mockedRunner:
            uut = SwayBackend()

            for image in self.__dummyWallpapers:
                mockedRunner.return_value = CompletedProcess(args="", returncode=0)

                uut.switch(image)

                mockedRunner.assert_called_once()
                commandCall = mockedRunner.call_args[0][0]
                self.assertEqual(commandCall[-2], image)

                mockedRunner.reset_mock()

    def test_failedToChange(self):
        errorMsg = "Dummy error"

        with mock.patch("subprocess.run", mock.Mock()) as mockedRunner:
            uut = SwayBackend()

            for image in self.__dummyWallpapers:
                mockedRunner.return_value = CompletedProcess(args="", returncode=1, stderr=errorMsg)

                with self.assertRaises(SwitcherException) as exceptionContext:
                    uut.switch(image)

                self.assertIn(errorMsg, str(exceptionContext.exception))

                mockedRunner.reset_mock()

