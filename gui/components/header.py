from nicegui import ui
from gui.components.translation import Translator
from typing import Literal


def change_language(value: Literal["en",'hu'], dropdown: ui.dropdown_button):
    Translator.language = value
    dropdown.text = value
    ui.run_javascript('location.reload()')

def create_header():
    global DARK

    with ui.header().classes("bg-primary text-white"):
        with ui.row().classes('w-full items-center'):
                ui.button(Translator["Home"], on_click=lambda: ui.navigate.to("/"))
                ui.button(Translator["Books"], on_click=lambda: ui.navigate.to("/crud"))
                ui.button(Translator["Book returnal"], on_click=lambda: ui.navigate.to("/return"))
                ui.button(Translator["Add book"], on_click=lambda: ui.navigate.to("/add_book"))
                ui.button(Translator["QR Codes"], on_click=lambda: ui.navigate.to("/qr"))
                ui.button(Translator["Info"], on_click=lambda: ui.navigate.to("/info"))
                with ui.dropdown_button(Translator.language, auto_close=True).classes('font-bold ml-auto mr-5') as lang_dropdown:     
                    ui.item('hu', on_click=lambda: change_language("hu", lang_dropdown))
                    ui.item('en', on_click=lambda: change_language("en", lang_dropdown))
                ui.label("SJG LMS").classes('font-bold ml-5 mr-30 text-2xl')

                