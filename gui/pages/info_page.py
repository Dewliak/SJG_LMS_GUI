from nicegui import ui
from gui.components import header

from datetime import date, datetime
from lmsapi import DataClient, SheetName, Book
from gui.services import DataClientSingleton

@ui.page("/info")
def info_page():
    header.create_header()

    ui.add_head_html("""
    <style>
    /* Increase vertical spacing between markdown headings */
    .markdown-body h1, 
    .markdown-body h2, 
    .markdown-body h3, 
    .markdown-body h4, 
    .markdown-body h5, 
    .markdown-body h6 {
        margin-top: 4rem;   /* space before */
        margin-bottom: 3rem; /* space after */
    }
    </style>
    """)

    with open("gui/static/info_text.md") as text_file:
        ui.markdown(text_file.read())

        