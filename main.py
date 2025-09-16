import multiprocessing
multiprocessing.set_start_method("spawn", force=True)

import pandas as pd

from gui.services import DataClientSingleton
from lmsapi import DataClient, SheetName, Book
from faker import Faker
from random import randint

from lmsapi.book import Book

from nicegui import ui, app
from gui.pages import main_page, crud_page, add_book_page, qr_page, book_return_page, info_page
if __name__ in {"__main__", "__mp_main__"}:

    client = DataClientSingleton.get_instance()

    ui.page_title('SJG - LMS')

    #main_page.main_page()
    crud_page.crud_page()
    add_book_page.add_book_page()
    qr_page.qr_page()
    book_return_page.book_return_page()
    info_page.info_page()

    ui.run(native=False)