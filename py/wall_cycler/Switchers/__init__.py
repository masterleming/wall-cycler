from .SwayBackend import SwayBackend
from .CmdSwitcher import CmdSwitcher

from ..exceptions import SwitcherException

def Switcher(definition):
    backend, *options = definition.split(':', maxsplit=1)

    if options:
        options = options[0].strip()

    if backend == "sway":
        return SwayBackend(options).switch

    if backend == "cmd":
        if len(options) == 0:
            raise SwitcherException("Command line switcher requires command line to work! Configuration given: '{}'.".format(definition))

        return CmdSwitcher(options).switch

    raise NotImplementedError("Given switcher ('{}') is not yet implemented!".format(definition))
