import pandas as pd


from lmsapi import DataClient, SheetName, Book, LendClient, LendModel
from faker import Faker
from random import randint

if __name__ == "__main__":

    #fake = Faker()

    #api_client = DataClient()

    #api_client.add_book(SheetName.BOOK, fake.name(), "test name", "test-" + randint(100,1000),randint(1,20))

    #df = api_client.sheets[SheetName.BOOK]
    #df.set_index("ID", inplace=True)
    #df.drop("2aad1asd4ca43", inplace=True)
    #print(df)

    #client = DataClient()

    #client.add_book("test name", "test book", '123-12311',15)

    #api_client.update_book(Book("2aad14ca43"  ,"a",'b','c',3,1))

    from datetime import datetime

    #client = LendClient()

    #lend_model = LendModel("Peter Parker", "II.A", "bob.ross@gmail.com", "c1283b768e", datetime.now(), datetime.now())
    #client.lend_book(lend_model)

    client = DataClient()
    lend_model = LendModel()
    lend_model.id = "35f94bd773"
    lend_model.book_id = "62e6b95f43"
    client.return_book(lend_model)


