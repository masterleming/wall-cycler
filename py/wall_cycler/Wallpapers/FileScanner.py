# FileScanner

import os
import os.path
import magic


class FileScanner:
    # TODO: handle subdirectories config!
    def __init__(self, path, subdirs=True):
        self.path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
        self._origPath = path
        self.subdirs = subdirs
        self.mime = magic.Magic(mime=True)

    def scan(self):
        if not os.path.exists(self.path):
            raise Exception(
                "Given path does not exist! Original path: '{}'; expanded path: '{}'.".format(
                    self._origPath, self.path))

        images = []
        if self.subdirs:
            for files in self._scan():
                images += self._filter(files)
        else:
            images = self._filter(next(self._scan()))

        return images

    def _scan(self):
        for root, _, files in os.walk(self.path):
            yield [os.path.join(root, f) for f in files]

    def _filter(self, files):
        return [f for f in files if "image" in self.mime.from_file(f)]
