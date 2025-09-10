from nicegui import ui
from gui.components import header


@ui.page("/")
def main_page():
    header.create_header()
    ui.label("Hello")
