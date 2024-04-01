import sqlite3
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from datetime import datetime, date
#import harperdb

from load_save_data import load_sheets



#from st_pages import show_pages_from_config, add_page_title

#dd_page_title("")
#show_pages_from_config(".streamlit/pages.toml")




#book_service = BookService()
#lend_service = LendService()


if 'book_sheet' not in st.session_state or 'lend_sheet' not in st.session_state:
    book_sheet, workbook, lend_sheet, lend_workbook = load_sheets()
    st.session_state["book_sheet"] = book_sheet
    st.session_state["lend_sheet"] = lend_sheet
    st.session_state["workbook"] = workbook
    st.session_state['lend_workbook'] = lend_workbook




if not st.session_state['book_sheet'].empty:
    #print(book_sheet.columns)
    gb = GridOptionsBuilder.from_dataframe(st.session_state['book_sheet'][["ID", "AUTHOR", "TITLE", "QUANTITY", "USED","ISBN"]])
    # configure selection
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gb.configure_side_bar()
    gridOptions = gb.build()

    data = AgGrid(st.session_state['book_sheet'],
                  gridOptions=gridOptions,
                  enable_enterprise_modules=True,
                  allow_unsafe_jscode=True,
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                  columns_auto_size_mode=1,
                  height=600,
                  theme="alpine")  # ColumnsAutoSizeMode.FIT_CONTENTS #alpine, balham, streamlit, material

else:
    st.info("Nincsen könyv az adatbázisban")

