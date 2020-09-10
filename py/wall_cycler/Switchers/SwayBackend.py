# SwayBackend

import subprocess
import re
from enum import Enum
from logging import getLogger

from .CmdSwitcher import CmdSwitcher, SubstitutionKeywords
from ..exceptions import SwitcherException

_logger = getLogger(__name__)


class _Scaling(Enum):
    stretch = "stretch"
    fill = "fill"
    fit = "fit"
    center = "center"
    tile = "tile"
    color = "color"


class _Options(Enum):
    scaling = "scaling"
    color = "color"


class SwayBackend(CmdSwitcher):
    class __CommandFields(Enum):
        Utility = "swaymsg"
        Target = "output"
        Command = "bg"


    __pattern = re.compile(r"^#[a-f0-9]{6}$")

    def __init__(self, options):
        self._scaling = _Scaling.fit
        self._color = "#000000"

        if options:
            self._getOptions(options)

        cmd = [
            self.__CommandFields.Utility.value,
            self.__CommandFields.Target.value,
            "*",  # TODO: replace with configuration of displays
            self.__CommandFields.Command.value,
            SubstitutionKeywords.WALLPAPER,
            self._scaling.value,
            self._color,
        ]
        if self._scaling is _Scaling.color:
            cmd[6:6] = [_Scaling.fill.value]

        super().__init__(cmd)

    def _getOptions(self, options):
        _logger.debug("Parsing sway:options '{}'.".format(options))
        optList = options.split(':')

        for opt in optList:
            key, *value = opt.split('=', maxsplit=1)
            _logger.debug("key: '{}', value: {}.".format(key, value))
            key = _Options(key.strip())

            if key is _Options.scaling:
                self._scaling = _Scaling(value[0].strip())

            if key is _Options.color:
                self._color = self.__validateColor(value[0])

    @classmethod
    def __validateColor(cls, color):
        orig = color
        color = color.strip()
        if cls.__pattern.match(color) is not None:
            return color

        else:
            raise SwitcherException(
                "Invalid color specified: '{}'; the value must be RGB color expressed as hex value '#rrggbb'."
                .format(orig))
