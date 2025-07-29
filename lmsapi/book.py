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


    def serialize_book(self) -> pd.DataFrame:
        serialized_book = {"ID": [self.book_id], "AUTHOR": [self.author], "TITLE": [self.title], "ISBN": [self.isbn],
                           "QUANTITY": [self.quantity], "USED": [self.used]}
        return pd.DataFrame(serialized_book, columns=['ID', 'AUTHOR', 'TITLE', 'ISBN', 'QUANTITY', 'USED'])
