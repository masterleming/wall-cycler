from .SwayBackend import SwayBackend


def Switcher(definition):
    if definition == "sway":
        return SwayBackend().switch

    raise NotImplementedError("Given switcher ('{}') is not yet implemented!".format(definition))
