from .connection_client import ConnectionClient
from .context_api import Context
from .sheet_names import SheetName

from base_logger import logger

import pandas as pd
import gspread


class WorksheetClient(ConnectionClient):


    def __init__(self,context:Context  ):
        super().__init__(context)

        # Store the spreadsheets' id for future use
        self.spreadsheet_id = self._secrets["sheet-id"]

        self.sheets = {SheetName.BOOK: self.get_sheet(sheet_name=SheetName.BOOK),
                       SheetName.LEND: self.get_sheet(sheet_name=SheetName.LEND)}

    def get_sheet(self, sheet_name: SheetName) -> pd.DataFrame | None:
        workbook = self._client.open_by_key(self._secrets["sheet-id"])
        try:
            sheet = workbook.worksheet(sheet_name.value)
            logger.info(f"[{__name__} - init] Worksheet {sheet_name.value} found")
            # TODO: put column datatypes
            return pd.DataFrame(sheet.get_all_records())
        except gspread.exceptions.WorksheetNotFound:
            logger.error(f"[{__name__} - init] Worksheet {sheet_name.value} not found")
            return None

    def update_sheet(self, sheet_name:SheetName) -> None:
        data_sheet = self.sheets[sheet_name]

        workbook = self._client.open_by_key(self._secrets["sheet-id"])
        try:
            sheet = workbook.worksheet(sheet_name.value)
            sheet.clear()
            sheet.update([data_sheet.columns.values.tolist()] + data_sheet.values.tolist())
            logger.info(f"[{__name__} - update]Worksheet {sheet_name.value} updated")

        except gspread.exceptions.WorksheetNotFound:
            logger.error(f"[{__name__} - update]Worksheet {sheet_name.value} not found")
            raise gspread.exceptions.WorksheetNotFound

    def update_all_sheets(self) -> None:

        for sheet_name in SheetName.list():
            self.update_sheet(sheet_name=sheet_name)
