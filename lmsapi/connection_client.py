import pandas as pd

import gspread
from google.oauth2.service_account import Credentials

import hashlib

import pandas as pd
from datetime import datetime

import json
from base_logger import logger


class ConnectionClient:

    def __init__(self,credentials_file: str = "credentials.json", secrets_file: str = "secrets.json" ) -> None:

        #Login with Oauth to the Google api
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file(credentials_file, scopes=scopes)
        self._client = gspread.authorize(creds)
        logger.info(f" [Client - init] Connected to the Google API")

        # Load neccesary env data
        with open(secrets_file) as f:
            try:
                self._secrets = json.load(f)
                logger.info(f"[Client - init] Secrets file loaded")
            except:
                logger.error(f"[Client - init] Error loading secrets file")








