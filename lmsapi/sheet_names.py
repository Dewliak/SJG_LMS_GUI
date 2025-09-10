from enum import Enum


class SheetName(Enum):
    BOOK = "BOOK_DATA"
    LEND = "LEND_DATA"

    @classmethod
    def list(cls):
        """
        Returns a list of all sheet names in the ENUM
        """
        return list(map(lambda s: s, cls))
