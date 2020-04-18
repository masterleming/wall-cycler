# ArgumentsParser

import argparse

from .RuntimeConfig import RuntimeConfig
from wall_cycler.Interval import Intervals

"""
[wall_cycler]
order = shuffle | sorted
wallpaper paths = multiple paths allowed in either unix format (path1:path2) or multiline in separate lines
change time = 1d 4h 30m | boot | once a day
cache dir = path to the cache folder
wallpaper backend = sway | $(expression)

config = path to the (additional) config file
"""


class ArgumentsParser:
    def __init__(self):
        parser = argparse.ArgumentParser(description="Simple utility for changing the screen wallpaper.")
        parser.add_argument("--order", choices=["shuffle", "sorted"], type=str, help="select the order of the wallpapers.")
        parser.add_argument("--img-path", type=str, action="extend", nargs='+', help="path(s) to look for the wallpaper images.")
        parser.add_argument("--interval", type=self.__interval_choices, help="specifies the time at which the wallpaper is changed. See TIME for details.")
        parser.add_argument("--cache-dir", type=str, help="path used for storing cached data; note that clearing the cache _will reset the wallpaper cycle_.")
        parser.add_argument("--backend", type=str, choices=['sway', 'custom'], help="defines what backend shall be used for changing the wallpaper.")
        parser.add_argument("--config", type=str, help="points to the configuration file to be used; note however that whatever options are set in this file will override options from a default file; to surpress all default options the default file needs to be removed or all options overriden.")
        parser.add_argument("--generate-config", type=str, nargs='?', help="causes generation of default configuration file; if no argument is given, the file is created in default location.")
        self.parser = parser

    def parse(self):
        return RuntimeConfig.fromProgramArgs(self.parser.parse_args())

    @staticmethod
    def __interval_choices(arg):
        return Intervals.Interval(arg)
