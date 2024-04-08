
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, ColumnsAutoSizeMode
from modal import Modal
from datetime import datetime, date
#import harperdb
st.set_page_config(layout="wide")

from load_save_data import add_book, update_sheet, load_sheets


def check_if_book_at_disposal(book_df, lend_df, lend_sheet):
    for id, record in lend_df.iterrows():
        if len(book_df.loc[book_df["ID"] == record["BOOK_ID"]]) == 0 and record["STATUS"] != "Book not at disposal":
            lend_df.loc[lend_df["ID"] == record["ID"], 'STATUS'] = 'Book not at disposal'

    update_sheet(lend_sheet, lend_df)

    return lend_df

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

    st.session_state['data'] = AgGrid(st.session_state["book_sheet"],
                  gridOptions=gridOptions,
                  enable_enterprise_modules=True,
                  allow_unsafe_jscode=True,
                  update_mode=GridUpdateMode.SELECTION_CHANGED,
                  columns_auto_size_mode=1,
                  height=600,
                  theme="alpine")  # ColumnsAutoSizeMode.FIT_CONTENTS #alpine, balham, streamlit, material
    print("SELECTED_ROW",st.session_state['data']["selected_rows"])
    st.session_state["selected_rows"] = st.session_state['data']["selected_rows"]


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

                st.session_state["lend_sheet"] = check_if_book_at_disposal(st.session_state["book_sheet"],st.session_state["lend_sheet"],st.session_state["lend_workbook"])

                modal.close()

            if st.button("NEM"):
                modal.close(())
print(st.session_state["selected_rows"])
if len(st.session_state["selected_rows"]) > 0:
    print(st.session_state["selected_rows"])
    with st.form("my_form", clear_on_submit=True):
        selected_rows = st.session_state["selected_rows"].to_dict()

        print("SELECTE_ROW", selected_rows)


        TITLE = tuple(selected_rows["TITLE"].values())[0]
        AUTHOR = tuple(selected_rows["AUTHOR"].values())[0]
        ISBN = tuple(selected_rows["ISBN"].values())[0]
        QUANTITY = tuple(selected_rows["QUANTITY"].values())[0]
        USED = tuple(selected_rows["USED"].values())[0]

        with st.sidebar:

            if len(selected_rows) != 0:
                print("DEBUG:", selected_rows)
                name = st.text_input("Meno:",value=TITLE)
                author = st.text_input("Author:",value=AUTHOR)
                isbn = st.text_input("ISBN:", value=ISBN)
                quantity = st.number_input(label="Quantity:",value = QUANTITY,min_value = min(QUANTITY,USED))

            submitted = st.form_submit_button("Submit")




            if submitted:
                print("DEBUG:", selected_rows)
                if len(selected_rows) != 0:
                    BOOK_ID = tuple(selected_rows["ID"].values())[0]

                    try:
                        print("DEBUG:", st.session_state['data'])
                        #firma_id = firma.split("-")[0].strip()
                        #update person data
                        used = st.session_state["book_sheet"].loc[st.session_state["book_sheet"]["ID"] == BOOK_ID,  "USED"]
                        st.session_state["book_sheet"].loc[st.session_state["book_sheet"]["ID"] == BOOK_ID] = pd.DataFrame({"ID":BOOK_ID,"AUTHOR":author, "TITLE":name, "ISBN":isbn,"QUANTITY": quantity,"USED":used})
                        update_sheet(st.session_state["workbook"],st.session_state["book_sheet"])
                        #book_service.update(BOOK_ID,{"Name":name,"Author":author,"ISBN":isbn,"quantity":quantity })
                        st.success(f"The book's data was successfully update")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(e)
                        print(e)
                else:
                    st.error("Nothing was selected")

