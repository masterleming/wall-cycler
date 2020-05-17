# exceptions

class MissingConfigFileException(Exception):
    pass


class MissingDirectoryException(Exception):
    pass


class InvalidSortOrderException(Exception):
    def __init__(self, order, valid):
        super().__init__("Received invalid sort order type: '{}'! Allowed types are: {}.".
        format(order, valid))


class InvalidTimeIntervalSpecificationException(Exception):
    pass


class TransactionCollisionException(Exception):
    pass
