from nicegui import ui

from lmsapi.data_client import DataClient
from lmsapi.sheet_names import SheetName
from lmsapi.book import Book
from gui.services import DataClientSingleton
from gui.components import header
from gui.components.translation import Translator

grid: ui.aggrid = None
row_data = {}
row_index = 0
book_author = None
book_title = None
book_quantity = None


def change_variable(event):
    global row_data, row_index
    if not event.args.get("selected", False):
        # Skip deselection event
        return
    global book_author, book_title, book_quantity

    row_index = event.args["rowIndex"]
    row_data = event.args["data"]

    book_author.value = row_data["AUTHOR"]
    book_title.value = row_data["TITLE"]
    book_quantity.value = row_data["QUANTITY"]


def update_book(client: DataClient):
    global book_author, book_title, book_quantity, grid, row_index, row_data

    book = Book(
        row_data["ID"],
        book_author.value,
        book_title.value,
        row_data["ISBN"],
        book_quantity.value,
        row_data["USED"],
    )
    try:
        
        client.update_book(book)

        grid.options["rowData"][row_index]["AUTHOR"] = book_author.value
        grid.options["rowData"][row_index]["TITLE"] = book_title.value
        grid.options["rowData"][row_index]["QUANTITY"] = book_quantity.value

        grid.update()

        ui.notify(Translator["The book was edited successfully"],type='positive')
    except Exception as E:
        print(E)
        ui.notify(Translator["There was an error while editing the book"],type='negative')

    


@ui.page("/crud")
def crud_page():
    global book_author, book_title, book_quantity, grid

    header.create_header()
    client = DataClientSingleton.get_instance()

    with ui.left_drawer(value=False).classes("bg-blue-100") as left_drawer:
        ui.button(on_click=left_drawer.hide, icon="arrow_back_ios").props("fab")

        book_author = ui.input(
            label=Translator["Author"],
            placeholder=Translator["start typing"]
        ).classes("w-full m-2")
        
        book_title = ui.input(
            label=Translator["Title"],
            placeholder=Translator["start typing"]
        ).classes("w-full m-2")

        book_quantity = ui.number(value=1, label=Translator["Quantity"]).classes("w-full m-2")

        book_update = ui.button(
            text=Translator["Update book"], on_click=lambda x: update_book(client)
        )

    # with ui.left_drawer(value=True).classes('bg-red-30') as left_drawer_button:
    ui.button(on_click=left_drawer.toggle, icon="edit").props("fab")

    ui.separator()

    with ui.column().classes("w-full h-screen"):
        grid = ui.aggrid.from_pandas(client.sync_sheet(SheetName.BOOK)).classes(
            "w-full flex-1"
        )

        grid.options['columnDefs'] =[
        {'field': 'ID', 'label': Translator["ID"],'flex': 3},
        {'field': 'TITLE', 'label': Translator["TITLE"],'flex': 8},
        {'field': 'AUTHOR', 'label': Translator["AUTHOR"],'flex': 8},
        {'field': 'ISBN', 'label': Translator["ISBN"],'flex': 5},
        {'field': 'QUANTITY', 'label': Translator["QUANTITY"],'flex': 2},
        {'field': 'USED', 'label': Translator["USED"],'flex': 2}
        ]
    for col in grid.options["columnDefs"]:
        if col["field"] == "ID":
            col["checkboxSelection"] = True

        if col["field"] in ["ID", "AUTHOR", "TITLE", "ISBN"]:
            col["filter"] = "agTextColumnFilter"
            col["floatingFilter"] = True

        if col["field"] in ["QUANTITY", "USED"]:
            col["filter"] = "agNumberColumnFilter"
            col["floatingFilter"] = True

    grid.on("rowSelected", lambda event: change_variable(event))
