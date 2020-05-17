#!/usr/bin/env python3

from wall_cycler.Config.ArgumentsParser import ArgumentsParser
from wall_cycler.Config.FileLoader import FileLoader
from wall_cycler.Config.RuntimeConfig import RuntimeConfig, Modes

from wall_cycler.WallCycler import WallCycler

from wall_cycler.DataStore import DataStore
from wall_cycler.Wallpapers.Updaters import Updater

# TODO: move it to config
from wall_cycler.Schedulers.InternalScheduler import InternalScheduler

if __name__ == '__main__':
    argConfig = ArgumentsParser().parse()
    if argConfig.mode == Modes.GenerateConfig:
        FileLoader().createDefaultConfig(argConfig.configFiles[0])
        exit(0)
    fileConfig = FileLoader(argConfig.configFiles).loadConfig()
    config = fileConfig + argConfig

    exit(
        WallCycler(
            DataStore(config.cacheDir),
            config.interval,
            Updater(config.order),
            InternalScheduler(),  # TODO: use config for this!
            None,  # TODO: provide implementation for different backends!
            config.wallpaperPaths).run())
