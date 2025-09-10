"""
This is the data model for sending LENDings to the google-sheet DB
"""
from dataclasses import dataclass
from datetime import datetime
import pandas as pd

from .misc import cheaphash



@dataclass
class LendModel:
    id: str
    name: str
    class_number: str
    email: str
    book_id: str
    start_date: datetime
    end_date: datetime
    status: str

    def __init__(
        self,
        name="",
        class_number="",
        email="",
        book_id="",
        start_date=datetime.now(),
        end_date=datetime.now(),
    ):
        self.id = ""
        self.name = name
        self.class_number = class_number
        self.email = email
        self.book_id = book_id
        self.start_date = start_date
        self.end_date = end_date
        self.status = "LENT"

    def serialize(self) -> pd.DataFrame:
        t = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        code_str = str(
            t
            + self.name
            + self.class_number
            + self.email
            + str(self.book_id)
            + str(self.start_date)
            + str(self.end_date)
        )
        unique_id = cheaphash(code_str.encode("utf-8"))

        return pd.DataFrame(
            {
                "ID": [unique_id],
                "NAME": [self.name],
                "CLASS": [self.class_number],
                "EMAIL": [self.email],
                "BOOK_ID": [self.book_id],
                "START_DATE": [str(self.start_date)],
                "END_DATE": [str(self.end_date)],
                "STATUS": [self.status],
            },
            columns=[
                "ID",
                "NAME",
                "CLASS",
                "EMAIL",
                "BOOK_ID",
                "START_DATE",
                "END_DATE",
                "STATUS",
            ],
        )
