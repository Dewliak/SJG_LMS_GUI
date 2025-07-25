import pandas as pd

from lmsapi import DataClient, SheetName
from faker import Faker
from random import randint

if __name__ == "__main__":

    fake = Faker()

    api_client = DataClient()

    api_client.add_book(SheetName.BOOK, fake.name(), "test name", randint(100,1000),randint(1,20))
