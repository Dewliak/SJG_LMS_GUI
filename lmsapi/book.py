from dataclasses import dataclass
import pandas as pd


@dataclass
class Book:
    book_id: str
    title: str
    author: str
    title: str
    isbn: str
    quantity: int
    used: int

    def __init__(self, book_id:str ="", author:str="", title:str ="", isbn:str ="", quantity:int =0, used:int =0):
        self.book_id = str(book_id)
        self.title = str(title)
        self.author = str(author)
        self.isbn = str(isbn)
        self.quantity = int(quantity)
        self.used = int(used)


def serialize_book(book: Book) -> pd.DataFrame:
    serialized_book = {"ID": [book.book_id], "AUTHOR": [book.author], "TITLE": [book.title], "ISBN": [book.isbn],
                       "QUANTITY": [book.quantity], "USED": [book.used]}
    return pd.DataFrame(serialized_book, columns=['ID', 'AUTHOR', 'TITLE', 'ISBN', 'QUANTITY', 'USED'])
