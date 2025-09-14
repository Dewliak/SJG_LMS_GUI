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
    #client.add_book("Lao ce", "Tao te king", "42", 20)
    #client.add_book("Formal languages and automats", "T. E. Colier", "11",14)
    from datetime import date, datetime
    df = client.get_sheet(SheetName.BOOK)
    lend_df = client.get_sheet(SheetName.LEND)
    print(df["QUANTITY"].sum(axis=0))
    print(len(df))
    #print(lend_df[(datetime.strptime(lend_df['END_DATE'], "%d/%m/Y") <= date.today()) ]  )
    late_lends = []
    for index,row in lend_df.iterrows():
        if datetime.strptime(row['END_DATE'], "%d/%m/%Y") <= datetime.now():
            late_lends.append(row)
    
    print(late_lends)
    
