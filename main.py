import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

import pandas as pd

from gui.services import DataClientSingleton
from lmsapi import DataClient, SheetName, Book
from faker import Faker
from random import randint

from lmsapi.book import Book

from nicegui import ui
from gui.pages import main_page, crud_page

if __name__ in {"__main__", "__mp_main__"}:

    client = DataClientSingleton.get_instance()

    #main_page.main_page()
    crud_page.crud_page()

    ui.run(native=False)
