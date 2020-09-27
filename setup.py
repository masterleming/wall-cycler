#!/usr/bin/env python3

import setuptools

setuptools.setup(
  name="wall_cycler",
  version="0.8",
  author="MasterLeming",
  author_email="",
  description="Utility for rotating desktop wallpapers.",
  url="",
  packages=setuptools.find_packages(exclude=["tests"], where="py"),
  package_dir={
        '': 'py',
    },
  scripts=['bin/wcycler'],
  python_requires='>=3.8',
  install_requires=['uptime>=3.0', 'python-magic>=0.4'])
