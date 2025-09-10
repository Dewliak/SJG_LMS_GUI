import pandas as pd
import streamlit as st
from legacy.load_save_data import load_sheets

from legacy.qrtoimg import Book, generate_print_sheet

st.set_page_config(page_title="Könyvek")


def load_data():
    book_sheet, workbook, lend_sheet, lend_workbook = load_sheets()
    st.session_state["book_sheet"] = book_sheet
    st.session_state["lend_sheet"] = lend_sheet
    st.session_state["workbook"] = workbook
    st.session_state["lend_workbook"] = lend_workbook

    counter = 0
    default_print = []

    print_sheet = book_sheet

    for id, record in book_sheet.iterrows():
        print(record)

        default_print.append(int(record["QUANTITY"]))

        counter += 1

    print_sheet = print_sheet.assign(PRINTED=[False for _ in range(counter)])
    print_sheet = print_sheet.assign(PRINT_QUANTITY=default_print)
    print("Printsheet", print_sheet)
    st.session_state["print_sheet"] = print_sheet


def nyomtatas(col):
    for_print = st.session_state["print_edited"].loc[
        st.session_state["print_edited"]["PRINTED"] == True
    ]
    books = []
    link = "https://sulilms.vercel.app/?id={}"  # TODO: CHANGE TO VERCEL

    for id, record in for_print.iterrows():
        print(link.format(record["ID"]))
        for i in range(int(record["PRINT_QUANTITY"])):
            books.append(
                Book(
                    record["ID"],
                    record["TITLE"],
                    record["AUTHOR"],
                    link.format(record["ID"]),
                )
            )
    print(books)
    d, bio = generate_print_sheet(books, bytes=True)

    if d:
        with col:
            st.download_button(
                label="Letöltés",
                data=bio.getvalue(),
                file_name="Nyomtatas.docx",
                mime="docx",
            )


if (
    "book_sheet" not in st.session_state
    or "lend_sheet" not in st.session_state
    or "print_sheet" not in st.session_state
):
    load_data()

if "selected_rows" not in st.session_state:
    st.session_state["selected_rows"] = []

if "row_input" not in st.session_state:
    st.session_state["row_input"] = {}

button_col1, button_col2, button_col3, button_col4 = st.columns([3, 3, 3, 10])

with button_col1:
    if st.button("Újratöltés"):
        load_data()

with button_col2:
    if st.button("Nyomtatás"):
        nyomtatas(button_col3)

st.session_state["print_edited"] = st.data_editor(
    st.session_state["print_sheet"],
    disabled=["ID", "AUTHOR", "TITLE", "ISBN", "QUANTITY", "USED"],
)
