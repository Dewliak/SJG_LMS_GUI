from nicegui import ui

from gui.services import DataClientSingleton
from gui.components import header

@ui.page("/add_book")
def add_book_page():

    header.create_header()
    client = DataClientSingleton.get_instance()

    
