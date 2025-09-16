from nicegui import ui
from google.api_core.exceptions import InvalidArgument

from lmsapi import DataClient, SheetName, Book, LendModel

from gui.services import DataClientSingleton
from gui.components import header

from datetime import date

grid: ui.aggrid = None
return_model: LendModel| None = None

def change_variable(event):
    global return_model
    if not event.args.get("selected", False):
        # Skip deselection event
        return
    
    row_data = event.args["data"]

    return_model = LendModel(name=row_data["NAME"], 
                             class_number=row_data["CLASS"],
                             email=row_data["EMAIL"],
                             book_id=row_data["BOOK_ID"],
                             end_date=row_data["END_DATE"],
                             )
    return_model.set_id(row_data["ID"])


def return_book(client: DataClient):
    global return_model, grid

    if return_model is not None:
        try:
            client.return_book(return_model)
            ui.notify(f"Book return", type="positive")
            grid.options["row_data"] = client.get_sheet(SheetName.LEND).to_dict(orient='records')
            grid.update()
            return_model = None 
        except InvalidArgument:
            ui.notify(f"Book not found", type="negative")
    else:
        ui.notify(f"No lender was select", type="negative")

        
    return

@ui.page("/return")
def book_return_page():
    global  grid

    header.create_header()
    client = DataClientSingleton.get_instance()

    ui.separator()
    lend_df = client.get_sheet(SheetName.LEND)
    book_df = client.get_sheet(SheetName.BOOK)
    return_button = ui.button(text='Return book', on_click=lambda x: return_book(client))
    

    
    
    grid = ui.aggrid.from_pandas(lend_df).classes("w-full h-screen")

    grid.options['columnDefs'] =[
            {'field': 'ID', 'flex': 3},
            {'field': 'NAME', 'flex': 6},
            {'field': 'CLASS', 'flex': 2},
            {'field': 'EMAIL', 'flex': 5},
            {'field': 'BOOK_ID', 'flex': 3},
            {'field': 'STATUS', 'flex': 2}
            ]

    for col in grid.options["columnDefs"]:
        if col["field"] == "ID":
            col["checkboxSelection"] = True
            col["width"] = 200

        if col["field"] in ["ID", "NAME", "CLASS", "EMAIL", "BOOK_ID", "STATUS"]:
            col["filter"] = "agTextColumnFilter"
            col["floatingFilter"] = True

        

        if col["field"] in ["END_DATE"]:

            today = date.today().strftime("%m/%d/%Y")

            col["filter"] = "agDateColumnFilter"
            col["floatingFilter"] = True

            #col['cellClassRules'] = {'bg-red-300': ' ((new Date(x)) > (new Date()))'}
    
    grid.on("rowSelected", lambda event: change_variable(event))
    
    
