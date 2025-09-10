import streamlit as st
import time
from legacy.load_save_data import add_book, load_sheets

if "book_sheet" not in st.session_state:
    book_sheet, workbook, lend_sheet, lend_workbook = load_sheets()
    st.session_state["book_sheet"] = book_sheet
    st.session_state["lend_sheet"] = lend_sheet
    st.session_state["workbook"] = workbook
    st.session_state["lend_workbook"] = lend_workbook


with st.form("my_form", clear_on_submit=True):
    name = st.text_input("*Cim:")
    author = st.text_input("*Author:")
    isbn = st.text_input("ISBN:")
    quantity = st.number_input(label="Quantity:", value=1)
    submitted = st.form_submit_button("Submit")

    if submitted:
        if name != "" and author != "":
            st.session_state["book_sheet"] = add_book(
                st.session_state["workbook"],
                st.session_state["book_sheet"],
                author,
                name,
                isbn,
                quantity,
            )
            st.success(f"A könyv sikeresen hozzá lett adva")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Minden *-al jelölt mezőt ki kell tölteni")
