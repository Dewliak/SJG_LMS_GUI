from nicegui import ui
from gui.components import header
from gui.services import DataClientSingleton
from lmsapi import DataClient


loading_spinner = None

def submit_form(client: DataClient,title: str, author: str, isbn: str, quantity: int):
    global loading_spinner
    try:
        loading_spinner.set_visibility(True)
        client.add_book(title=title, author=author, isbn=isbn, quantity=quantity)
        ui.notify("Book added successfully", type='positive')
    except:
        ui.notify("There was an error when adding the book", type='negative')
    finally:
        loading_spinner.set_visibility(False)

@ui.page("/add_book")
def add_book_page():
    global loading_spinner
    header.create_header()
    client = DataClientSingleton.get_instance()

    with ui.row().classes('w-full h-screen flex justify-center pt-10'):
        with ui.column().classes('border border-gray-300 rounded-xl p-6 bg-white gap-4 items-center'):
            #title
            title_input = ui.input(placeholder="Title").classes('w-96').props('w-200 rounded outlined dense')
            #author
            author_input = ui.input(placeholder="Author").classes('w-96').props('rounded outlined dense')
            #ISBN
            isbn_input = ui.input(placeholder="ISBN").classes('w-96').props('rounded outlined dense')
            #quantity
            quantity_input = ui.number(label='Quantity',value=1,min=1).classes('text-right w-96').props('rounded outlined dense')

            with ui.row():

                submit_button = ui.button(text="Submit", on_click=lambda _: submit_form(client,
                                                                                    title_input.value,
                                                                                    author_input.value,
                                                                                    isbn_input.value,
                                                                                    quantity_input.value))
                loading_spinner = ui.spinner(size='lg')
                loading_spinner.set_visibility(False)
