"""
This is book model for working with book types between the API and program
"""
from dataclasses import dataclass
import pandas as pd
from datetime import datetime
from .misc import cheaphash

from base_logger import logger


@dataclass
class Book:

    book_id: str
    title: str
    author: str
    isbn: str
    quantity: int
    used: int

    def __init__(
        self,
        book_id: str = "",
        author: str = "",
        title: str = "",
        isbn: str = "",
        quantity: int = 0,
        used: int = 0,
    ):
        self.book_id = str(book_id)
        self.title = str(title)
        self.author = str(author)
        self.isbn = str(isbn)
        self.quantity = int(quantity)
        self.used = int(used)

    def serialize_book(self) -> pd.DataFrame:
        """
        serializes the itselfs data so it can be used in a pandas dataframe
        """
        time_now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        if self.book_id == "" or self.book_id is None:
            try:
                # TODO CHECK FOR UNIQUITY
                self.book_id = cheaphash(
                    str(time_now + self.author + self.title + str(self.isbn)).encode(
                        "utf-8"
                    )
                )
                logger.debug(f"[{__name__} - Add] Generated ID: {self.book_id}")
            except Exception as e:
                logger.error(
                    f"[{__name__} - Add] Error adding book, cheaphash error: \n + {e} "
                )

        serialized_book = {
            "ID": [self.book_id],
            "AUTHOR": [self.author],
            "TITLE": [self.title],
            "ISBN": [self.isbn],
            "QUANTITY": [self.quantity],
            "USED": [self.used],
        }

        return pd.DataFrame(
            serialized_book,
            columns=["ID", "AUTHOR", "TITLE", "ISBN", "QUANTITY", "USED"],
        )
