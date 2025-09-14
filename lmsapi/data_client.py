"""
This class works with two main things:
1. adding/editing/deleting books
2. processing returnal of a book
"""
from google.api_core.exceptions import InvalidArgument

from .lend_model import LendModel
from .worksheet_client import WorksheetClient
from .context_api import Context
from .sheet_names import SheetName
from .book import Book
from .misc import cheaphash

import pandas as pd
from datetime import datetime

from base_logger import logger


class DataClient(WorksheetClient):


    def __init__(self, context=Context()):
        super().__init__(context)

    def add_book(self, author, title, isbn="", quantity=1, used=0) -> bool:
        """
        Updates the dataframe, and updates the google sheet
        """
        logger.info(f"[{__name__} - Add] Adding book to {SheetName.BOOK.value} ")

        # Generating the unique ID

        # Creating the entry in the DB
        new_row = Book("", author, title, isbn, quantity, used).serialize_book_to_list()

        logger.debug(f"[{__name__} - Add] New row:\n {new_row}")
        
        book_df = self.get_sheet(SheetName.BOOK)

        #book_df = pd.concat([book_df, new_row], ignore_index=True)
        
        if book_df is None:
            logger.error(
                f"[{__name__} - Add] Error adding book, couldn't find Sheetname.BOOK: \n + {e} "
            )
            return False
        
            # ! IMPORTANT -  Check if db is empty 
        if(len(book_df) == 0):
            logger.info("BOOK DB is empty")
            
            # create new DF + hacky workaround to reference inside client, cuz no set methods in the backend
            self.sheets[SheetName.BOOK.value] = pd.DataFrame(new_row)
        else:
            book_df.loc[len(book_df.index)] = new_row

        # UPDATING
        try:
            self.update_sheet(SheetName.BOOK)
        except Exception as e:
            logger.error(
                f"[{__name__} - Add] Error adding book, update error: \n + {e} "
            )
            return False

        logger.info(f"[{__name__} - Add] Book addition finished successfully!")
        return True

    def update_book(self, book: Book):
        """
        throwsa Invalid argument
        thows Value error

        TODO: logging
        TODO:
        """
        # find the row in the dataframe
        # update the row

        book_df = self.get_sheet(SheetName.BOOK)

        if book.book_id == "":
            raise InvalidArgument("Book id should not be empty")

        # check if id exists

        if book_df.loc[book_df.ID == book.book_id].empty:
            raise ValueError("No such book with this ID")

        book_df.loc[book_df.ID == book.book_id] = book.serialize_book()
        
        self.update_sheet(sheet_name=SheetName.BOOK)

        logger.info(
            f"[{__name__} - Update] Book - id: {book.book_id} - updated successfully!"
        )

    def remove_book(self, book: Book):
        # might raise keyerror
        book_df = self.get_sheet(SheetName.BOOK)

        book_df.set_index("ID", inplace=True)
        book_df.drop(book.book_id, inplace=True)
        book_df.reset_index(inplace=True)

        self.update_sheet(SheetName.BOOK)

    def return_book(self, lend_model: LendModel):
        # 1. find book if exists in the db
        # 2. lower the quantity max(0, current - 1)
        # 3. delete from the lend db
        book_df = self.get_sheet(SheetName.BOOK)
        lend_df = self.get_sheet(SheetName.LEND)
        book_row = book_df.loc[book_df["ID"] == lend_model.book_id]

        logger.debug(f"[{__name__} - BOOK_RETURN] BOOK_ROW: {book_row}")

        if book_row.empty:
            logger.error(f"[{__name__} - BOOK_RETURN] Book not found")
            raise InvalidArgument("Book not found")

        # TODO: resolve negative 
        amount: int = int(book_df.loc[book_df["ID"] == lend_model.book_id, "USED"]) 
        print("DEBUG: AMOUNT ", amount)
        book_df.loc[book_df["ID"] == lend_model.book_id, "USED"] = max(amount - 1,0)
        print("DEBUG: AMOUNT2 ", book_df.loc[book_df["ID"] == lend_model.book_id, "USED"])
        
        lend_df.set_index("ID", inplace=True)
        lend_df.drop(lend_model.id, inplace=True)
        lend_df.reset_index(inplace=True)

        self.update_sheet(SheetName.BOOK)
        self.update_sheet(SheetName.LEND)

        logger.info(f"[{__name__} - BOOK_RETURN] Book return was successful!")
