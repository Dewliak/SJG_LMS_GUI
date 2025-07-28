from enum import Enum

class SheetName(Enum):
    BOOK = "BOOK_DATA"
    LEND = "LEND_DATA"

    @classmethod
    def list(cls):
        return list(map(lambda s: s, cls))
