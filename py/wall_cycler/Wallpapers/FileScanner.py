# FileScanner

import os
import os.path
import magic
from logging import getLogger

_logger = getLogger(__name__)


class FileScanner:
    def __init__(self, path, subdirs=True):
        self.path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        self._origPath = path
        self.subdirs = subdirs
        self.mime = magic.Magic(mime=True)

    def scan(self):
        _logger.info("Scanning path '%s' for images.", self.path)
        if not os.path.exists(self.path):
            _logger.error("Path does not exist!")
            raise Exception(
                "Given path does not exist! Original path: '{}'; expanded path: '{}'.".format(
                    self._origPath, self.path))

        images = []
        if self.subdirs:
            _logger.debug("Scanning subdirectories.")
            for files in self._scan():
                images += self._filter(files)
        else:
            images = self._filter(next(self._scan()))

        _logger.info("Found %d image(s).", len(images))
        return images

    def _scan(self):
        for root, _, files in os.walk(self.path):
            _logger.debug("Walking path '%s'.", root)
            yield [os.path.join(root, f) for f in files]

    def _filter(self, files):
        return [f for f in files if "image" in self.mime.from_file(f)]
