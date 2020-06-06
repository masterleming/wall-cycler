# GlobalConfig

# TODO remove the file as it is unused!


class GlobalConfig:

    __instance = None

    @classmethod
    def get(cls):
        return cls.__instance

    @classmethod
    def set(cls, config):
        cls.__instance = config

    def __init__(self):
        pass
