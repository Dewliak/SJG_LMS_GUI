from nicegui import ui
from gui.components import header

from datetime import date, datetime
from lmsapi import DataClient, SheetName, Book
from gui.services import DataClientSingleton
from gui.components.translation import Translator

@ui.page("/")
def main_page():
    header.create_header()

    
    client = DataClientSingleton.get_instance()

    # get all distinct books
    # get books amount
    # get books due

    
    book_df = client.get_sheet(SheetName.BOOK)
    lend_df = client.get_sheet(SheetName.LEND)
    print()
    print()
    #print(lend_df[(datetime.strptime(lend_df['END_DATE'], "%d/%m/Y") <= date.today()) ]  )
    late_lends = []
    for index,row in lend_df.iterrows():
        if datetime.strptime(row['END_DATE'], "%d/%m/%Y") <= datetime.now():
            late_lends.append(row.to_dict())
    
    print(late_lends)
    

 
    with ui.row().classes('w-full h-screen flex-nowrap'):
        # LEFT HALF
        with ui.column().classes(
            'w-1/3 h-full flex justify-start items-center bg-gray-100 pt-[2vh]'
        ):
            with ui.row().classes(
                    'bg-white rounded-2xl shadow-xl aspect-square w-full max-w-[500px] flex-nowrap border border-gray-300'
            ):
                stats = [
                    (Translator['All books'], book_df["QUANTITY"].sum(axis=0)),
                    (Translator['Unique books'], len(book_df)),
                    (Translator['Late books'], len(late_lends)),
                ]

                for title, number in stats:
                    with ui.column().classes(
                        'flex-1 h-full flex items-center justify-center'
                    ):
                        ui.label(title).classes(
                            'text-xl font-semibold text-gray-600'
                        )
                        ui.label(number).classes(
                            'text-7xl font-extrabold text-gray-800'
                        )

        # Right half (empty)
        with ui.column().classes('w-2/3 h-full p-10'):
            ui.label(Translator['Late book lends']).classes('text-2xl font-bold mb-4 text-gray-700')
            
            ui.table(
                columns=[
                    {'name': 'ID', 'label': Translator['ID'], 'field': 'ID', 'align': 'left'},
                    {'name': 'NAME', 'label': Translator['NAME'], 'field': 'NAME', 'align': 'left'},
                    {'name': 'CLASS', 'label': Translator['CLASS'], 'field': 'CLASS', 'align': 'left'},
                    {'name': 'EMAIL', 'label': Translator['EMAIL'], 'field': 'EMAIL', 'align': 'left'},
                    {'name': 'BOOK_ID', 'label': Translator['BOOK_ID'], 'field': 'BOOK_ID', 'align': 'left'},
                    {'name': 'END_DATE', 'label': Translator['END_DATE'], 'field': 'END_DATE', 'align': 'left'},
                    {'name': 'STATUS', 'label': Translator['STATUS'], 'field': 'STATUS', 'align': 'left'},
                ],
                rows=late_lends,
                row_key='title',
            ).classes('w-full shadow-md rounded-xl')