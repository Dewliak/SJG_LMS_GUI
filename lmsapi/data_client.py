from google.api_core.exceptions import InvalidArgument

from .worksheet_client import WorksheetClient
from .context_api import Context
from .sheet_names import SheetName
from .book import Book, serialize_book

import pandas as pd
import hashlib
import gspread
from datetime import datetime

from base_logger import logger




def cheaphash(string,length=10):
    if length<len(hashlib.sha256(string).hexdigest()):
        return hashlib.sha256(string).hexdigest()[:length]
    else:
        raise Exception("Length too long. Length of {y} when hash length is {x}.".format(x=str(len(hashlib.sha256(string).hexdigest())),y=length))


class DataClient(WorksheetClient):
    def __init__(self, context = Context()):
        super().__init__(context)

    def add_book(self,sheet_name: SheetName, author, title, isbn='', quantity=1) -> bool:
        """
        Updates the dataframe, and updates the google sheet
        """

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
        new_row = serialize_book(Book(unique_id,author,title,isbn,quantity,used))
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

        self.sheets[SheetName.BOOK].loc[self.sheets[SheetName.BOOK].ID == book.book_id] = serialize_book(book).values

        self.update_sheet(sheet_name=SheetName.BOOK)

        logger.info(f"[{__name__} - Update] Book - id: {book.book_id} - updated successfully!")

    def remove_book(self,book:Book):
        # might raise keyerror
        self.sheets[SheetName.BOOK].set_index("ID", inplace=True)
        self.sheets[SheetName.BOOK].drop(book.book_id, inplace=True)
        self.sheets[SheetName.BOOK].reset_index(inplace=True)


