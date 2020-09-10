from .SwayBackend import SwayBackend
from .CmdSwitcher import CmdSwitcher


def Switcher(definition):
    if definition == "sway":
        return SwayBackend().switch

    if definition.startswith("cmd:"):
        return CmdSwitcher(definition[4:].strip()).switch

    raise NotImplementedError("Given switcher ('{}') is not yet implemented!".format(definition))
