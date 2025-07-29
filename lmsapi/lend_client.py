from lmsapi import WorksheetClient
from context_api import Context
from lend_model import LendModel
from sheet_names import SheetName

class LendClient(WorksheetClient):
    def __init__(self, context = Context()):
        super().__init__(context)

    def lend_book(self, lend_model: LendModel):
        self.sync_sheet(SheetName.LEND)
        book_df = self.get_sheet(SheetName.BOOK)
        lend_df = self.get_sheet(SheetName.LEND)
        print(book_df)

        book_df.loc[book_df["ID"] == lend_model.book_id, "USED"] += 1 # = self.sheets[SheetName.BOOK.value].loc[filter, "USED"] +
        serialized_book = lend_model.serialize()

        print(book_df)
        print(lend_df)

        if lend_df.empty:
            self.sheets[SheetName.LEND.value] = serialized_book
        else:
            self.sheets[SheetName.LEND.value].loc[len(self.sheets[SheetName.LEND.value])] = serialized_book

        self.update_sheet(SheetName.LEND)


if __name__ == "__main__":
    from datetime import datetime
    client = LendClient()

    lend_model = LendModel("Peter Parker","II.A","bob.ross@gmail.com","c1283b768e",datetime.now(), datetime.now())
    client.lend_book(lend_model)