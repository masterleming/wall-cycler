# ArgumentsParser

import argparse
from logging import getLogger
from distutils.util import strtobool

from .RuntimeConfig import RuntimeConfig
from ..Interval import Intervals
from ..Wallpapers.Updaters import UpdaterTypes
from ..Init.Log import logLevels
"""
[wall_cycler]
order = shuffle | sorted
wallpaper paths = multiple paths allowed in either unix format (path1:path2) or multiline in separate lines
change time = 1d 4h 30m | boot | once a day
cache dir = path to the cache folder
wallpaper backend = sway | $(expression)

config = path to the (additional) config file
"""

_logger = getLogger(__name__)


class ArgumentsParser:
    def __init__(self):
        # yapf: disable
        parser = argparse.ArgumentParser(description="Simple utility for changing the screen wallpaper.")
        parser.add_argument("--order", choices=UpdaterTypes.choices(), type=str, help="select the order of the wallpapers.")
        parser.add_argument("--img-path", type=str, action="extend", nargs='+', help="path(s) to look for the wallpaper images.")
        parser.add_argument("--interval", type=self.__interval_choices, help="specifies the time at which the wallpaper is changed. See TIME for details.")
        parser.add_argument("--cache-dir", type=str, help="path used for storing cached data; note that clearing the cache _will reset the wallpaper cycle_.")
        parser.add_argument("--backend", type=str, choices=['sway'], help="defines what backend shall be used for changing the wallpaper.")
        parser.add_argument("--config", type=str, help="points to the configuration file to be used; note however that whatever options are set in this file will override options from a default file; to suppress all default options the default file needs to be removed or all options overridden.")
        parser.add_argument("--generate-config", type=str, nargs='?', help="causes generation of default configuration file; if no argument is given, the file is created in default location.", const=True)
        parser.add_argument("--log-dir", type=str, help="specifies a directory to log to.")
        parser.add_argument("--log-level", type=str, choices=logLevels(), help="limits logs to specified and higher level.")
        parser.add_argument("--force-refresh", type=strtobool, help="forces reloading of the wallpaper whenever the expiration check is made and it is not yet time for changing the wallpaper.")
        # yapf: enable
        self.parser = parser

    def parse(self):
        _logger.debug("Parsing command line arguments.")
        return RuntimeConfig.fromProgramArgs(self.parser.parse_args())

    @staticmethod
    def __interval_choices(arg):
        return Intervals.Interval(arg)
