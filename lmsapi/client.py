from lmsapi.connection_client import ConnectionClient
from base_logger import logger
import pandas as pd

import gspread

class Client(ConnectionClient):
    BOOK_DATA_SHEET = "BOOK_DATA" # constants for the sheet name
    LEND_DATA_SHEET = "LEND_DATA"

    def __init__(self,credentials_file: str = "credentials.json", secrets_file: str = "secrets.json"  ):
        super().__init__(credentials_file,secrets_file)

        # Store the spreadsheets' id for future use
        self.spreadsheet_id = self._secrets["sheet-id"]

        self.book_sheet = self.get_sheet(Client.BOOK_DATA_SHEET)
        self.book_sheet = self.get_sheet(Client.LEND_DATA_SHEET)

    def get_sheet(self, sheet_name) -> pd.DataFrame:
        workbook = self._client.open_by_key(self._secrets["sheet-id"])
        try:
            sheet = workbook.worksheet(sheet_name)
            logger.info(f"[Client - init]Worksheet {sheet_name} found")
            return pd.DataFrame(sheet.get_all_records())
        except gspread.exceptions.WorksheetNotFound:
            logger.error(f"[Client - init]Worksheet {sheet_name} not found")
            return None
