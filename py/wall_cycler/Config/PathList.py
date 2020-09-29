# PathList.py

import re
from logging import getLogger

from ..exceptions import PathSpecificationException
import os.path

_logger = getLogger(__name__)


class PathList:

    specRegex = re.compile(r"^(?:(\w+)@)?(.*)$")

    def __init__(self):
        self._paths = {}

    def addFromString(self, s):
        paths = self._parseConfigString(s)

        for spec, path in paths:
            if path in self._paths:
                _logger.warning("Path '%s' is specified multiple times.", path)
            self._paths[path] = spec

    def __iter__(self):
        for path, spec in self._paths.items():
            yield path, spec

    @classmethod
    def _parseConfigString(cls, s):
        def validateSpec(spec):
            if spec is None:
                return True
            spec = spec.lower()
            if spec in ["r", "rec", "recursive"]:
                return True
            if spec in ["s", "single"]:
                return False
            raise PathSpecificationException(
                "Path specification must be (S)ingle or (R)ecursive, not '{}'!".format(spec))

        def validatePath(path):
            path = os.path.abspath(os.path.expandvars(os.path.expanduser(path)))
            result = os.path.exists(path)
            if not result:
                _logger.warning("Path '%s' does not exist!", path)
                return None
            return path

        specList = s.split(':')
        pathList = []
        for spec in specList:
            spec, path = cls.specRegex.match(spec).groups()
            spec = validateSpec(spec)
            path = validatePath(path)
            if path is not None:
                pathList.append((spec, path))

        return pathList
