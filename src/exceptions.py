# exceptions

class MissingConfigFileException(Exception):
    pass

class MissingDirectoryException(Exception):
    pass

class InvalidSortOrderException(Exception):
    pass

class InvalidTimeIntervalSpecificationException(Exception):
    pass

class TransactionCollisionException(Exception):
    pass
