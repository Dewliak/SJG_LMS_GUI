"""
This modules works with communication and validating the data between the google sheet api and
the python program.
It is done in 3 layers with 4 modules:

1. Connection Client
2. Work Sheet Client
3. DataClient & LendClient

"""

from .connection_client import ConnectionClient
from .lend_client import LendClient
from .worksheet_client import WorksheetClient
from .data_client import DataClient
from .context_api import Context
from .sheet_names import SheetName
from .book import Book
from .lend_model import LendModel

__all__ = [
    "ConnectionClient",
    "WorksheetClient",
    "DataClient",
    "Context",
    "SheetName",
    "Book",
    "LendClient",
    "LendModel",
]

"""
New thing learnt, by doing this allows us at importing the module, to import these modules directly

so before:
from lmsapi.connection_client import ConnectionClient

then:
from lmsapi import ConnectionClient

"""
