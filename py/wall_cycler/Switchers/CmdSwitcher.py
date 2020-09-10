# CmdSwitcher

import subprocess

from logging import getLogger
from ..exceptions import SwitcherException

_logger = getLogger(__name__)


class CmdSwitcher:
    def __init__(self, cmd):
        self._cmd = cmd

    def switch(self, wallpaper):
        cmd = self._cmd.replace("$WALLPAPER", wallpaper)

        _logger.info("Setting new wallpaper.")
        _logger.debug("Command template: '{cmd}', wallpaper: '{wallpaper}'.".format(
            cmd=self._cmd, wallpaper=wallpaper))
        _logger.debug("Substituted command: '{cmd}'.".format(cmd=cmd))

        result = subprocess.run([cmd], capture_output=True)
        if result.returncode != 0:
            raise SwitcherException(
                "The wallpaper setting command returned non-zero exit code!\nError log:\n{}".format(
                    result.stderr))
