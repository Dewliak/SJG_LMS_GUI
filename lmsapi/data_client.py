from google.api_core.exceptions import InvalidArgument

from .worksheet_client import WorksheetClient
from .context_api import Context
from .sheet_names import SheetName
from .book import Book
from .misc import cheaphash

import pandas as pd
from datetime import datetime

from base_logger import logger




class DataClient(WorksheetClient):
    """
    This class works with two main things:
    1. adding/editing/deleting books
    2. processing lend
    """
    def __init__(self, context = Context()):
        super().__init__(context)

    def add_book(self,sheet_name: SheetName, author, title, isbn='', quantity=1) -> bool:
        """
        Updates the dataframe, and updates the google sheet
        """
        # TODO: refactor for BOOK model
        logger.info(f"[{__name__} - Add] Adding book to {sheet_name.value} ")

        #Generating the unique ID
        t = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        used = 0

        try:
            # TODO CHECK FOR UNIQUITY
            unique_id = cheaphash(str(t + author + title + str(isbn)).encode('utf-8'))
        except Exception as e:
            logger.error(f"[{__name__} - Add] Error adding book, cheaphash error: \n + {e} ")
            return False

        logger.debug(f"[{__name__} - Add] Generated ID: {unique_id}")

        # Creating the entry in the DB
        new_row = Book(unique_id,author,title,isbn,quantity,used).serialize_book()
        logger.debug(f"[{__name__} - Add] New row:\n {new_row}")

        self.sheets[sheet_name] = pd.concat([self.sheets[sheet_name], new_row], ignore_index=True)

        # UPDATING
        try:
            self.update_sheet(sheet_name)
        except Exception as e:
            logger.error(f"[{__name__} - Add] Error adding book, update error: \n + {e} ")
            return False

        logger.info(f"[{__name__} - Add] Book addition finished successfully!")
        return True

    def update_book(self, book:Book):
        """
        throwsa Invalid argument
        thows Value error

        TODO: logging
        TODO:
        """
        # find the row in the dataframe
        # update the row



        if book.book_id == "":
            raise InvalidArgument("Book id should not be empty")

        # check if id exists

        if self.sheets[SheetName.BOOK].loc[self.sheets[SheetName.BOOK].ID == book.book_id].empty:
            raise ValueError("No such book with this ID")

        self.sheets[SheetName.BOOK].loc[self.sheets[SheetName.BOOK].ID == book.book_id] = (book.serialize_book()).values

        self.update_sheet(sheet_name=SheetName.BOOK)

        logger.info(f"[{__name__} - Update] Book - id: {book.book_id} - updated successfully!")

    def remove_book(self,book:Book):
        # might raise keyerror
        self.sheets[SheetName.BOOK].set_index("ID", inplace=True)
        self.sheets[SheetName.BOOK].drop(book.book_id, inplace=True)
        self.sheets[SheetName.BOOK].reset_index(inplace=True)

    def return_book(self):
        raise NotImplementedError


if __name__ == "__main__":
    client = DataClient()

    client.add_book()
