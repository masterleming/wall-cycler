# WALL_CYCLER #
===============

This is utility for automatic desktop wallpaper rotation.

It uses any graphic file it finds in specified directory (seeking recursively if
configured). It switches the wallpapers in alphabetic order by filename or
shuffles the wallpapers order. It automatically detects new images in the
directory. If the order used is "shuffle", it shuffles any new image into the
existing (cyclic) queue. Also, whenever new files are shuffled in, it is
guaranteed the next switch will use one of the new wallpapers. Optionally, it
can be also configured to remove from queue wallpapers which has been removed
from the directory.

There are several options for when or how often the wallpapers are switched.
Default options are: after every system boot and once a day. It also supports
user defined time intervals for the switches. Optionally, it can run in the
background and enforce the switch when the time comes or it can be called from
sysetm scheduler (e.g. variant of CRON).

It is preconfigured to work with sway/scroll window compositors, but it can also
call any user defined command (uses simple varialbe substitution syntax to embed
wallpaper path into the command).
