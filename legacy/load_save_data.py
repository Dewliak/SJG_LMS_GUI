import gspread
from google.oauth2.service_account import Credentials

from .sheet_names import SheetNames

import hashlib
import pandas as pd
from datetime import datetime


def cheaphash(string, length=10):
    if length < len(hashlib.sha256(string).hexdigest()):
        return hashlib.sha256(string).hexdigest()[:length]
    else:
        raise Exception(
            "Length too long. Length of {y} when hash length is {x}.".format(
                x=str(len(hashlib.sha256(string).hexdigest())), y=length
            )
        )


def load_sheets():
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    sheet_id = "1wxuoW-WmiAGxex0Doq6j1teeEL4TF0mFLRE4qCgPyAU"
    workbook = client.open_by_key(sheet_id)

    sheet = workbook.worksheet("BOOK_DATA")
    lend_sheet = workbook.worksheet("LEND_DATA")
    dataframe = pd.DataFrame(sheet.get_all_records())
    lend_dataframe = pd.DataFrame(lend_sheet.get_all_records())

    return dataframe, sheet, lend_dataframe, lend_sheet


def add_book(sheet_name: SheetName, dataframe, author, title, isbn="", quantity=1):
    """
    Updates the dataframe, and updates the google sheet
    """
    dataframe = self.sheets[sheet_name.value]
    t = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    print(t)
    used = 0
    unique_id = cheaphash(str(t + author + title + str(isbn)).encode("utf-8"))
    print(unique_id)
    # serialized_book = [unique_id, author, title, isbn, quantity, used]
    serialized_book = {
        "ID": [unique_id],
        "AUTHOR": [author],
        "TITLE": [title],
        "ISBN": [isbn],
        "QUANTITY": [quantity],
        "USED": [used],
    }
    df = pd.DataFrame(
        serialized_book, columns=["ID", "AUTHOR", "TITLE", "ISBN", "QUANTITY", "USED"]
    )
    dataframe = pd.concat([dataframe, df], ignore_index=True)

    #    dataframe.loc[len(dataframe.index)] = serialized_book
    update_sheet(sheet_name, dataframe)

    return dataframe


def update_sheet(sheet, dataframe):
    sheet.clear()
    sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())


# def

if __name__ == "__main__":
    a, b, c, d = load_sheets()
    print(a)
