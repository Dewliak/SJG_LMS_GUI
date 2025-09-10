from dataclasses import dataclass


@dataclass
class QrBookModel:
    book_id: str
    name: str
    author: str
    link: str

    def __init__(
        self,
        book_id: str,
        name: str,
        author: str,
        link: str,
    ):
        self.book_id = book_id
        self.name = name
        self.author = author
        self.link = link  # we add the link
