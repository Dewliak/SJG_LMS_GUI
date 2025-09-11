import pandas as pd


from lmsapi import DataClient, SheetName, Book, LendClient, LendModel
from faker import Faker
from random import randint

from qr_generator.qr_generator import QrBookModel, generate_qr_image
from lmsapi import Context

if __name__ == "__main__":
    data2 = [
        QrBookModel(book_id=1,name="ASD", author="1", link="http://127.0.0.1:5000/?=1"),
        QrBookModel(
            book_id=2,name="test", author="test", link="http://127.0.0.1:5000/?=562977095734"
        ),
    ]

    generate_qr_image(data2, context=Context(), bytes=False)
