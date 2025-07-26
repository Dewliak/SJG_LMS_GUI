import pandas as pd


from lmsapi import DataClient, SheetName, Book
from faker import Faker
from random import randint

from lmsapi.book import serialize_book

if __name__ == "__main__":

    fake = Faker()

    api_client = DataClient()

    #api_client.add_book(SheetName.BOOK, fake.name(), "test name", "test-" + randint(100,1000),randint(1,20))

    df = api_client.sheets[SheetName.BOOK]
    df.set_index("ID", inplace=True)
    df.drop("2aad1asd4ca43", inplace=True)
    print(df)

    #api_client.update_book(Book("2aad14ca43","a",'b','c',3,1))