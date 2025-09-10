import unittest
import json
from unittest.mock import patch, MagicMock, mock_open
import pandas as pd
import logging 

from lmsapi import DataClient, WorksheetClient, ConnectionClient, LendClient, Book, LendModel, SheetName

class FakeContext:
    creds = 'tests/fake_data/fake_creds.json'
    secrets = 'tests/fake_data/fake_secrets.json'

class BaseClientTest(unittest.TestCase):

    def setUp(self):
        logging.disable(logging.CRITICAL)  # disable all logging
        self.mock_client = MagicMock()
        self.mock_workbook = MagicMock()
        self.mock_worksheet = MagicMock()

        self.mock_client.open_by_key.return_value = self.mock_workbook
        self.mock_workbook.worksheet.return_value = self.mock_worksheet
        self.mock_worksheet.get_all_records.return_value = []

        self._mock_workbook = self.mock_workbook


class TestDataClient(unittest.TestCase):
    @patch("lmsapi.connection_client.gspread.authorize")
    @patch("builtins.open", new_callable=mock_open, read_data=json.dumps({"sheet-id": "fake-sheet"}))
    @patch('lmsapi.connection_client.Credentials.from_service_account_file')
    def setUp(self, mock_creds, mock_open, mock_auth):
        logging.disable(logging.CRITICAL)  # disable all logging
        

        #worksheet
        self.mock_worksheet = MagicMock()
        self.mock_worksheet.get_all_records.return_value = []

        #Workbook
        self.mock_workbook = MagicMock()

        #Client
        self.mock_client = MagicMock()
        self.mock_client.open_by_key.return_value = self.mock_workbook


  
        self.mock_workbook.worksheet.return_value = self.mock_worksheet


        self._mock_workbook = self.mock_workbook
        mock_creds.return_value= MagicMock()
        mock_auth.return_value = self.mock_client()
        
        self.client = DataClient(FakeContext())

         # Preload empty sheets
        self.client.sheets[SheetName.BOOK.value] = pd.DataFrame(
            columns=["ID", "AUTHOR", "TITLE", "ISBN", "QUANTITY", "USED"]
        )
        self.client.sheets[SheetName.LEND.value] = pd.DataFrame(
            columns=["ID", "book_id"]
        )
    
    def test_add_book(self):
        result = self.client.add_book("Orwell", "1984", isbn="1234", quantity=2)
        self.assertTrue(result)
        self.assertIn("Orwell", self.client.sheets[SheetName.BOOK.value]["AUTHOR"].values)

    def test_update_book_success(self):
        # :TODO 
        assert True