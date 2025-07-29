from nicegui import ui

from lmsapi.data_client import DataClient
from lmsapi.sheet_names import SheetName
from lmsapi.book import Book
from gui.services import DataClientSingleton
from gui.components import header

grid: ui.aggrid = None
row_data = {}
row_index = 0
book_author = None
book_title = None
book_quantity = None

def change_variable(event):
    global row_data, row_index
    if not event.args.get('selected', False):
        # Skip deselection event
        return
    global book_author, book_title, book_quantity

    row_index = event.args["rowIndex"]
    row_data = event.args['data']

    print("Row selected" )
    print(row_data)
    book_author.value = row_data["AUTHOR"]
    book_title.value = row_data["TITLE"]
    book_quantity.value = row_data["QUANTITY"]

def update_book(client):
    global book_author, book_title, book_quantity,grid, row_index, row_data

    book = Book(row_data["ID"], book_author.value, book_title.value, row_data["ISBN"], book_quantity.value, row_data["USED"])

    client.update_book(book)

    grid.options["rowData"][row_index]["AUTHOR"] = book_author.value
    grid.options["rowData"][row_index]["TITLE"] = book_title.value
    grid.options["rowData"][row_index]["QUANTITY"] = book_quantity.value

    grid.update()



@ui.page("/crud")
def crud_page():
    global book_author, book_title, book_quantity,grid

    header.create_header()
    client = DataClientSingleton.get_instance()





    with ui.left_drawer(value=False).classes('bg-blue-100') as left_drawer:
        ui.button(on_click=left_drawer.hide, icon='arrow_back_ios').props('fab')
        ui.label('Side menu')

        book_author_label = ui.label("Author")
        book_author = ui.input(label='Text', placeholder='start typing',
                 validation={'Input too long': lambda value: len(value) < 20})
        book_title_label = ui.label("Title")
        book_title = ui.input(label='Text', placeholder='start typing',
         validation={'Input too long': lambda value: len(value) < 20})

        book_quantity_label = ui.label("Quantity")
        book_quantity = ui.number(value=42)

        book_update = ui.button(text="Update book",on_click=lambda x: update_book(client))

    #with ui.left_drawer(value=True).classes('bg-red-30') as left_drawer_button:
    ui.button(on_click=left_drawer.toggle, icon='edit').props('fab')

    ui.separator()

    with ui.column().classes('w-full h-screen'):
        grid = ui.aggrid.from_pandas(client.sync_sheet(SheetName.BOOK)).classes('w-full flex-1')



    for col in grid.options['columnDefs']:
        if col['field'] == 'ID':
            col['checkboxSelection'] = True
            col['width'] = 200

        if col['field'] in ["ID",'AUTHOR', "TITLE", "ISBN"]:
            col['filter'] = 'agTextColumnFilter'
            col['floatingFilter'] = True

        if col['field'] in ["QUANTITY", "USED"]:
            col['filter'] = 'agNumberColumnFilter'
            col['floatingFilter'] = True

    grid.on('rowSelected', lambda event: change_variable(event))




