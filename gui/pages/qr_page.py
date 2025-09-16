from nicegui import ui, events
from gui.components import header

from lmsapi import Context, DataClient, SheetName, Book

from gui.services import DataClientSingleton
from gui.components import header
from gui.components.translation import Translator
from qr_generator.qr_generator import QrBookModel, generate_qr_image

import os

columns = [
    {'name': 'ID', 'label': Translator['ID'], 'field': 'ID', 'classes': 'w-5'},
    {'name': 'TITLE',  'label': Translator['TITLE'], 'field': 'TITLE', 'classes': 'w-30'},
    {"name": "AUTHOR", 'label': Translator["AUTHOR"], 'field': "AUTHOR", 'classes': 'w-20'},
    {'name': 'print_amount', 'label': Translator['Print Amount'], 'field': 'print_amount', 'classes': 'w-20'},
]

ROWS = []

def change_print_amount(e: events.GenericEventArguments, table) -> None:
    
    for row in table.rows:
        if row['ID'] == e.args['ID']:
            row['print_amount'] = e.args['print_amount']
    


async def handle_checked_rows(grid: ui.aggrid, table: ui.table):
    checked_rows = await grid.get_selected_rows()
    
    # add new
    for row in checked_rows:
        if not any(filter(lambda r: r["ID"] == row["ID"], table.rows)):
            #add 
            new_row = {"ID": row["ID"], "TITLE": row["TITLE"], "AUTHOR": row["AUTHOR"], 'print_amount':1}
            table.add_row(new_row)

    # delete not used

    table.rows = [r for r in table.rows if any(filter(lambda x: x["ID"] == r["ID"], checked_rows))]
    
    table.update()
        


def generate_qr_code(table:ui.table,client:DataClient,spinner: ui.spinner):
    spinner.set_visibility(True)

    link = client._secrets["link"] + "/?id="
    books = []
    for element in table.rows:
        for _ in range(element["print_amount"]):
            books.append(QrBookModel(element["ID"],element["TITLE"],element["AUTHOR"],link + element["ID"]))
    file_name = ""
    if len(books):
        file_name = generate_qr_image(books,Context())

        
    spinner.set_visibility(False)
    ui.notify(Translator["The QR-code document is being downloaded"],type='positive')
    ui.download.file(f"{file_name}")

def delete_files_in_qr_folder():
    qr_folder = "generated_qr_images"
    for root, dirs, files in os.walk('generated_qr_images'):
        for f in files:
            os.remove(qr_folder + "/" + f)

            


@ui.page("/qr")
def qr_page():
    header.create_header()
    client: DataClient = DataClientSingleton.get_instance()
    delete_files_in_qr_folder()
    with ui.row() as row:
        
        qr_button = ui.button(Translator["Print"],on_click=lambda _ : generate_qr_code(table,client,loading_spinner))
        loading_spinner = ui.spinner(size='lg')
        loading_spinner.set_visibility(False)

    with ui.splitter().classes('w-full') as splitter:
        with splitter.before:
            with ui.column().classes("w-full h-screen mx-auto"):
                grid = ui.aggrid.from_pandas(client.sync_sheet(SheetName.BOOK)).classes(
                "w-full flex-1"
                ).on('selectionChanged', lambda event: handle_checked_rows(grid, table))
                
                grid.options["rowSelection"] = 'multiple'
                grid.options['columnDefs'] =[
                                            {'field': 'ID', 'label':Translator["ID"],'flex': 3},
                                            {'field': 'AUTHOR', 'label':Translator["AUTHOR"],'flex': 5},
                                            {'field': 'TITLE', 'label':Translator["TITLE"],'flex': 7},
                                            {'field': 'ISBN', 'label':Translator["ISBN"],'flex': 3},
                                            {'field': 'QUANTITY', 'label':Translator["QUANTITY"],'flex': 2},
                                            {'field': 'USED', 'label':Translator["USED"],'flex': 2}
                                            ]
                
                for col in grid.options["columnDefs"]:
                    if col["field"] == "ID":
                        col["checkboxSelection"] = True
                        col["width"] = 200
                    

                    if col["field"] in ["ID", "AUTHOR", "TITLE", "ISBN"]:
                        col["filter"] = "agTextColumnFilter"
                        col["floatingFilter"] = True

                    if col["field"] in ["QUANTITY", "USED"]:
                        col["filter"] = "agNumberColumnFilter"
                        col["floatingFilter"] = True

                

#    grid.on("rowSelected", lambda event: change_variable(event))
    
        with splitter.after:
            table = ui.table(columns=columns, rows=ROWS).classes('w-full mx-auto')
            # Age column as a number input
            table.add_slot('body-cell-print_amount', r'''
                <q-td key="print_amount" :props="props">
                    <q-input
                        type="number"
                        v-model.number="props.row.print_amount"
                        @update:model-value="() => $parent.$emit('change_print_amount', props.row)"
                        style="max-width: 100px"
                        :min="1"
                    />
                </q-td>
            ''')
            table.on('change_print_amount', lambda e: change_print_amount(e, table))



    

        



    