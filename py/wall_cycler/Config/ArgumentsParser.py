# ArgumentsParser

import argparse
from logging import getLogger
from distutils.util import strtobool
import shutil
import textwrap

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

_epilog = [
    ("BACKENDS:", 0),
    ("Options are passed to the backend after colon character, e.g. 'cmd:echo #WALLPAPER'. The backend must be recognised as a complete string even if there are spaces in the options (like in the example); escape white space to prevent splitting the command or use configuration file.", 2),
    ("", 0),
    ("Some backends may support variable substitutions like #WALLPAPER for the path to the wallpaper file to be set.", 2),
    ("", 0),
    ("Available backends and their options:", 2),
    ("sway", 4),
    ("no options", 6),
    ("", 0),
    ("cmd", 4),
    ("as the sole option it accepts the raw string with shell command to be executed; use '#WALLPAPER' as a placeholder for the actual wallpaper's file path in the command.", 6),
    ("", 0)
]


def _formatEpilog():
    cols, *_ = shutil.get_terminal_size((80, 25))
    tw = textwrap.TextWrapper(tabsize=4, width=cols - 1)

    def individualWrap(spec):
        text, indent = spec
        indent = indent * ' '
        tw.initial_indent = indent
        tw.subsequent_indent = indent
        return tw.fill(text)

    return "\n".join(map(individualWrap, _epilog))


_logger = getLogger(__name__)


class ArgumentsParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description="Simple utility for changing the screen wallpaper.",
            epilog=_formatEpilog(),
            formatter_class=argparse.RawDescriptionHelpFormatter)
        # yapf: disable
        parser.add_argument("--order", choices=UpdaterTypes.choices(), type=str, help="select the order of the wallpapers.")
        parser.add_argument("--img-path", type=str, action="extend", nargs='+', help="path(s) to look for the wallpaper images.")
        parser.add_argument("--interval", type=self.__interval_choices, help="specifies the time at which the wallpaper is changed. See TIME for details.")
        parser.add_argument("--cache-dir", type=str, help="path used for storing cached data; note that clearing the cache _will reset the wallpaper cycle_.")
        parser.add_argument("--backend", type=str, help="defines what backend shall be used for changing the wallpaper; currently only 'sway' and 'cmd' are supported. See BACKENDS for more info.")
        parser.add_argument("--config", type=str, help="points to the configuration file to be used; note however that whatever options are set in this file will override options from a default file; to suppress all default options the default file needs to be removed or all options overridden.")
        parser.add_argument("--generate-config", type=str, nargs='?', help="causes generation of default configuration file; if no argument is given, the file is created in default location.", const=True)
        parser.add_argument("--log-dir", type=str, help="specifies a directory to log to.")
        parser.add_argument("--log-level", type=str, choices=logLevels(), help="limits logs to specified and higher level.")
        parser.add_argument("--force-refresh", type=strtobool, help="forces reloading of the wallpaper whenever the expiration check is made and it is not yet time for changing the wallpaper.")
        parser.add_argument("--use-external-scheduling", type=strtobool, help="suppresses internal scheduling and expiration check in case external scheduling is used (e.g. `cron`).")
        # yapf: enable
        self.parser = parser

    def parse(self):
        _logger.debug("Parsing command line arguments.")
        return RuntimeConfig.fromProgramArgs(self.parser.parse_args())

    @staticmethod
    def __interval_choices(arg):
        return Intervals.Interval(arg)
