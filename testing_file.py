import pandas as pd


from lmsapi import DataClient, SheetName, Book, LendClient, LendModel
from faker import Faker
from random import randint

from qr_generator.qr_generator import QrBookModel, generate_qr_image
from lmsapi import Context


def qr_code_testing():
    
    data2 = [
        QrBookModel(book_id=1,name="ASD", author="1", link="http://127.0.0.1:5000/?=1"),
        QrBookModel(
            book_id=2,name="test", author="test", link="http://127.0.0.1:5000/?=562977095734"
        ),
    ]

    generate_qr_image(data2, context=Context(), bytes=False)
    

if __name__ == "__main__":

    client = DataClient(Context())

    #client.add_book("Obadovics Gyula", "Matematika", "",5)
    client.add_book("Lao ce", "Tao te king", "42", 20)
    client.add_book("Formal languages and automats", "T. E. Colier", "11",14)

    