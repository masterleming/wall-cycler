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
        _logger.debug("Raw cmd='{}', type={}".format(self._cmd, type(self._cmd)))
        if type(self._cmd) is str:
            self._cmd = self._cmd.strip().split()
            return self._getCmd(wallpaper)

        cmd = self._cmd[:]
        for i in range(len(cmd)):
            if cmd[i] is SubstitutionKeywords.WALLPAPER:
                cmd[i] = wallpaper
            else:
                cmd[i] = cmd[i].replace(SubstitutionKeywords.WALLPAPER.value, wallpaper)
        return cmd
