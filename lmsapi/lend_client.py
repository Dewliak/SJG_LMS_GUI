from .worksheet_client import WorksheetClient
from .context_api import Context
from .lend_model import LendModel
from .sheet_names import SheetName

import pandas as pd

class LendClient(WorksheetClient):
    def __init__(self, context = Context()):
        super().__init__(context)

    def lend_book(self, lend_model: LendModel):
        self.sync_sheet(SheetName.LEND)
        book_df = self.get_sheet(SheetName.BOOK)
        lend_df = self.get_sheet(SheetName.LEND)

        book_df.loc[book_df["ID"] == lend_model.book_id, "USED"] += 1 # = self.sheets[SheetName.BOOK.value].loc[filter, "USED"] +
        serialized_book = lend_model.serialize()

        if lend_df.empty:
            self.sheets[SheetName.LEND.value] = serialized_book
        else:
            self.sheets[SheetName.LEND.value] = pd.concat([self.sheets[SheetName.LEND.value],serialized_book],ignore_index=True)

        self.update_sheet(SheetName.LEND)

