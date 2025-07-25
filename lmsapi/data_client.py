from .worksheet_client import WorksheetClient
from .context_api import Context
from .sheet_names import SheetName

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
            unique_id = cheaphash(str(t + author + title + str(isbn)).encode('utf-8'))
        except Exception as e:
            logger.error(f"[{__name__} - Add] Error adding book, cheaphash error: \n + {e} ")
            return False

        logger.debug(f"[{__name__} - Add] Generated ID: {unique_id}")

        # Creating the entry in the DB
        serialized_book = {"ID": [unique_id], "AUTHOR": [author], "TITLE": [title], "ISBN": [isbn],
                           "QUANTITY": [quantity], "USED": [used]}
        new_row = pd.DataFrame(serialized_book, columns=['ID', 'AUTHOR', 'TITLE', 'ISBN', 'QUANTITY', 'USED'])

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



