# CmdSwitcher

import subprocess

from logging import getLogger
from enum import Enum

from ..exceptions import SwitcherException

_logger = getLogger(__name__)


class SubstitutionKeywords(Enum):
    WALLPAPER = "#WALLPAPER"


class CmdSwitcher:
    def __init__(self, cmd):
        self._cmd = cmd

    def switch(self, wallpaper):
        cmd = self._getCmd(wallpaper)

        _logger.info("Setting new wallpaper.")
        _logger.debug("Command template: '{cmd}', wallpaper: '{wallpaper}'.".format(
            cmd=self._cmd, wallpaper=wallpaper))
        _logger.debug("Substituted command: '{cmd}'.".format(cmd=cmd))

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            raise SwitcherException(
                "The wallpaper setting command returned non-zero exit code!\nError log:\n{}".format(
                    result.stderr))

    def _getCmd(self, wallpaper):
        if type(self._cmd) is str:
            return self._cmd.replace(SubstitutionKeywords.WALLPAPER.value, wallpaper).split(maxsplit=1)

        cmd = self._cmd[:]
        for i in range(len(cmd)):
            if cmd[i] is SubstitutionKeywords.WALLPAPER or cmd[i] == SubstitutionKeywords.WALLPAPER.value:
                cmd[i] = wallpaper
        return cmd
