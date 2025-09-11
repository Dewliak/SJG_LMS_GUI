from nicegui import ui
from gui.components import header


@ui.page("/add_book")
def add_book_page():
    header.create_header()
    ui.label("Hello")