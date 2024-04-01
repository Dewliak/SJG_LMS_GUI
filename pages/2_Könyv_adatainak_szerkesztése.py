
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from modal import Modal
from datetime import datetime, date
#import harperdb
st.set_page_config(layout="wide")

from load_save_data import add_book, update_sheet, load_sheets

if "selected_rows" not in st.session_state:
    st.session_state["selected_rows"] = []

if "book_sheet" not in st.session_state:
    book_sheet, workbook, lend_sheet, lend_workbook = load_sheets()
    st.session_state["book_sheet"] = book_sheet
    st.session_state["lend_sheet"] = lend_sheet
    st.session_state["workbook"] = workbook
    st.session_state['lend_workbook'] = lend_workbook

#df, sheet, lend_dataframe, lend_sheet = load_sheets()

modal = Modal("Biztos?",
    key="demo-modal",

    # Optional
    padding=20,  # default value
    max_width=304  # default value
)

col1, col2, col3 = st.columns([1,1,5])

with col1:

    if st.button("Újratöltés"):
        book_sheet, workbook, lend_sheet, lend_workbook = load_sheets()
        st.session_state["book_sheet"] = book_sheet
        st.session_state["lend_sheet"] = lend_sheet
        st.session_state["workbook"] = workbook
        st.session_state['lend_workbook'] = lend_workbook

with col2:
    open_modal = st.button("Törlés")

if len(st.session_state["book_sheet"]):
    gb = GridOptionsBuilder.from_dataframe(st.session_state["book_sheet"][["ID","AUTHOR","TITLE","ISBN","QUANTITY","USED"]])
    # configure selection
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gb.configure_side_bar()
    gridOptions = gb.build()

    data = AgGrid(st.session_state["book_sheet"],
                  gridOptions=gridOptions,
                  enable_enterprise_modules=True,
                  allow_unsafe_jscode=True,
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                  columns_auto_size_mode=1,
                  height=600,
                  theme="alpine")  # ColumnsAutoSizeMode.FIT_CONTENTS #alpine, balham, streamlit, material
    st.session_state["selected_rows"] = data["selected_rows"]


    if open_modal and len(st.session_state["selected_rows"]) != 0:
        modal.open()
        print("S",st.session_state["selected_rows"])


    if modal.is_open():
        with modal.container():
            if st.button("Igen"):
                print("______________________-")
                print("SS",st.session_state["selected_rows"])

                id = st.session_state["selected_rows"][0]["ID"]

                index = st.session_state['book_sheet'][st.session_state['book_sheet']['ID'] == id].index

                st.session_state['book_sheet'] = st.session_state['book_sheet'].drop(index)
                update_sheet(st.session_state["workbook"], st.session_state["book_sheet"])
                modal.close()

            if st.button("NEM"):
                modal.close(())

if len(st.session_state["selected_rows"]) > 0:
    with st.form("my_form", clear_on_submit=True):
        selected_rows = st.session_state["selected_rows"]
        print("SELECTE_ROW", selected_rows)
        with st.sidebar:

            if len(selected_rows) != 0:
                print("DEBUG:", selected_rows)
                name = st.text_input("Meno:",value=selected_rows[0]["TITLE"])
                author = st.text_input("Author:",value=selected_rows[0]["AUTHOR"])
                isbn = st.text_input("ISBN:", value=selected_rows[0]["ISBN"])
                quantity = st.number_input(label="Quantity:",value = selected_rows[0]["QUANTITY"],min_value = min(selected_rows[0]["USED"],selected_rows[0]["QUANTITY"]))

            submitted = st.form_submit_button("Submit")




            if submitted:
                print("DEBUG:", selected_rows)
                if len(selected_rows) != 0:
                    BOOK_ID = selected_rows[0]["ID"]
                    try:
                        print("DEBUG:", data)
                        #firma_id = firma.split("-")[0].strip()
                        #update person data
                        used = st.session_state["book_sheet"].loc[st.session_state["book_sheet"]["ID"] == BOOK_ID,  "USED"]
                        st.session_state["book_sheet"].loc[st.session_state["book_sheet"]["ID"] == BOOK_ID] = pd.DataFrame({"ID":BOOK_ID,"AUTHOR":author, "TITLE":name, "ISBN":isbn,"QUANTITY": quantity,"USED":used})
                        update_sheet(st.session_state["sheet"],st.session_state["book_sheet"])
                        #book_service.update(BOOK_ID,{"Name":name,"Author":author,"ISBN":isbn,"quantity":quantity })
                        st.success(f"The book's data was successfully update")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(e)
                        print(e)
                else:
                    st.error("Nothing was selected")

