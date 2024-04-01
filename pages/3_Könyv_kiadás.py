import streamlit as st
import pandas as pd
from load_save_data import add_book, update_sheet, load_sheets
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode,JsCode
from datetime import datetime


jscode = JsCode("""
function(params) {
    if (params.data.STATUS === 'Needs to be returned') {
        return {
            'color': 'white',
            'backgroundColor': 'red'
        }
    }
    if (params.data.STATUS === 'Book not at disposal') {
        return {
            'color': 'white',
            'backgroundColor': 'gray'
        }
    }
};
""")

def format_books(book_df, lend_df):

    record_sheet = []
    for id, record in lend_df.iterrows():
        print(id)
        print(record)
        new_record = {"ID":record["ID"],
                      "NAME":record["NAME"],
                      "CLASS":record["CLASS"],
                      "EMAIL":record["EMAIL"],
                      "END_DATE":record["END_DATE"]}

        if(len(book_df) == 0):
            new_record["STATUS"] = "Book not at disposal"
            new_record["AUTHOR"] = ""
            new_record["TITLE"] = ""
            record_sheet.append(new_record)

            continue

        if len(book_df.loc[book_df["ID"] == record["BOOK_ID"]]) > 0:
            author = book_df["AUTHOR"].loc[book_df["ID"] == record["BOOK_ID"]].array[0]
            title = book_df["TITLE"].loc[book_df["ID"] == record["BOOK_ID"]].array[0]
            new_record["AUTHOR"] = author
            new_record["TITLE"] = title

            return_date = datetime.strptime(record["END_DATE"], "%Y-%m-%d")

            if return_date < datetime.now() and record["STATUS"] != "Email Sent":
                new_record["STATUS"] = "Needs to be returned"
            elif record["STATUS"] == "Email sent":
                new_record["STATUS"] = "Email sent"
            else:
                new_record["STATUS"] = "Lent"
        else:
            new_record["AUTHOR"] = ""
            new_record["TITLE"] = ""
            new_record["STATUS"] = "Book not at disposal"

        record_sheet.append(new_record)

    return record_sheet

def load_lent_data():
    book_sheet, workbook, lend_sheet, lend_workbook = load_sheets()
    st.session_state["book_sheet"] = book_sheet
    st.session_state["lend_sheet"] = lend_sheet
    st.session_state["workbook"] = workbook
    st.session_state['lend_workbook'] = lend_workbook


    st.session_state["book_dataframe"] = pd.DataFrame(format_books(book_sheet, lend_sheet))

if "selected_rows" not in st.session_state:
    st.session_state.selected_rows = []

from load_save_data import add_book, update_sheet, load_sheets

if 'book_sheet' not in st.session_state or 'lend_sheet' not in st.session_state or "book_dataframe" not in st.session_state:
    load_lent_data()


button_col1,button_col2,button_col3,button_col4 = st.columns([2,2,4,6])


def give_back_book(lent_id):
    """
        1. Book Sheet Lent - 1
        2. Lend Sheet delete row
        """
    book_df = st.session_state["book_sheet"]
    lent_df = st.session_state["lend_sheet"]
    print("LENT DF", lent_df.loc[lent_df["ID"] == lent_id, "BOOK_ID"].array[0])
    book_id = int(lent_df.loc[lent_df["ID"] == lent_id, "BOOK_ID"].array[0])

    if not book_df.loc[book_df["ID"] == book_id].empty:
        st.session_state["book_sheet"].loc[st.session_state["book_sheet"]["ID"] == book_id, "USED"] -= 1

        index = st.session_state['lend_sheet'][st.session_state['lend_sheet']['ID'] == lent_id].index
        print("DROPPING")
        print(index)
        print(st.session_state['lend_sheet'])
        st.session_state['lend_sheet'] = st.session_state['lend_sheet'].drop(index)
        print(st.session_state['lend_sheet'])
        update_sheet(st.session_state["workbook"],st.session_state["book_sheet"])
        update_sheet(st.session_state["lend_workbook"], st.session_state["lend_sheet"])
        st.success("Sikeres ovlt a visszadas")
    else:
        st.error("No book found")


with st.container():

    with button_col1:
        if st.button("Visszaad"):
            if st.session_state.selected_rows != []:
                lent_id = st.session_state.selected_rows[0]["ID"]


                if give_back_book(lent_id):
                    load_lent_data()

    with button_col2:
        if st.button("Újratölt"):

            load_lent_data()


    with button_col3:

        if st.button("Eltűnt könyvek törlése"):
            # NEEDS TO BE TESTED

            for i in st.session_state["book_dataframe"].loc[st.session_state["book_dataframe"]["STATUS"] == "Book not at disposal", "ID"]:
                index = st.session_state['lend_sheet'][st.session_state['lend_sheet']['ID'] == i].index
                st.session_state['lend_sheet'] = st.session_state['lend_sheet'].drop(index)
                print("DELETING", i)
            update_sheet(st.session_state["lend_workbook"], st.session_state["lend_sheet"])
            load_lent_data()


with st.container():
    if len(st.session_state.lend_sheet) != 0:
        gb = GridOptionsBuilder.from_dataframe(st.session_state['book_dataframe'][["TITLE","AUTHOR","NAME","CLASS","EMAIL","END_DATE","STATUS"]])
        #gb = GridOptionsBuilder.from_dataframe(st.session_state.book_data[["STATUS","END_DATE","NAME","CLA, SS","TITLE","AUTHOR","BOOK_ID", "ID"]])
    # configure selection

        gb.configure_selection(selection_mode="single", use_checkbox=True)
        gb.configure_side_bar()
        gridOptions = gb.build()
        gridOptions["getRowStyle"] = jscode

        data = AgGrid(st.session_state['book_dataframe'],
                          gridOptions=gridOptions,
                          enable_enterprise_modules=True,
                          allow_unsafe_jscode=True,
                          update_mode=GridUpdateMode.SELECTION_CHANGED,
                          columns_auto_size_mode=1,
                          height=600,
                          theme="alpine")  # ColumnsAutoSizeMode.FIT_CONTENTS #alpine, balham, streamlit, material
        st.session_state.selected_rows = data["selected_rows"]

