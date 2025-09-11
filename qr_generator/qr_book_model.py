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
        self.book_id = str(book_id)
        self.name = str(name)
        self.author = str(author)
        self.link = str(link)  # we add the link
