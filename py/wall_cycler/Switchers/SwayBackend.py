# SwayBackend

import subprocess
from enum import Enum

from logging import getLogger
from ..exceptions import SwitcherException

_logger = getLogger(__name__)


class WallpaperOptions(Enum):
    Stretch = "stretch"
    Fill = "fill"
    Fit = "fit"
    Center = "center"
    Tile = "tile"


class SwayBackend:
    class __CommandFields(Enum):
        Utility = "swaymsg"
        Target = "output"
        Command = "bg"

    def __init__(self):
        pass

    def switch(self, wallpaper):
        cmd = [
            self.__CommandFields.Utility.value,
            self.__CommandFields.Target.value,
            "*",  # TODO: replace with configuration of displays
            self.__CommandFields.Command.value,
            str(wallpaper),
            WallpaperOptions.Fill.value  # TODO: make it configurable
        ]

        _logger.info("Setting new wallpaper.")
        _logger.debug("Command to be used: '{cmd}'.".format(cmd=" ".join(cmd)))

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            raise SwitcherException(
                "The wallpaper setting command returned non-zero exit code!\nError log:\n{}".format(
                    result.stderr))
