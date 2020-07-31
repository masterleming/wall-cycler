# SwayBackend

import subprocess
from enum import Enum

from logging import getLogger

from .CmdSwitcher import CmdSwitcher, SubstitutionKeywords

_logger = getLogger(__name__)


class WallpaperOptions(Enum):
    Stretch = "stretch"
    Fill = "fill"
    Fit = "fit"
    Center = "center"
    Tile = "tile"


class SwayBackend(CmdSwitcher):
    class __CommandFields(Enum):
        Utility = "swaymsg"
        Target = "output"
        Command = "bg"

    def __init__(self):
        cmd = [
            self.__CommandFields.Utility.value,
            self.__CommandFields.Target.value,
            "*",  # TODO: replace with configuration of displays
            self.__CommandFields.Command.value,
            SubstitutionKeywords.WALLPAPER,
            WallpaperOptions.Fill.value  # TODO: make it configurable
        ]
        super().__init__(cmd)
