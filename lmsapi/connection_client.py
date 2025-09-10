import gspread
from google.oauth2.service_account import Credentials

import json
from base_logger import logger

from .context_api import Context


class ConnectionClient:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def __init__(self, context: Context) -> None:
        # Login with Oauth to the Google api

        creds = Credentials.from_service_account_file(
            context.creds, scopes=ConnectionClient.SCOPES
        )
        self._client = gspread.authorize(creds)
        logger.info(f" [{__name__} - init] Connected to the Google API")

        # Load neccesary env data
        with open(context.secrets) as f:
            try:
                self._secrets = json.load(f)
                logger.info(f"[{__name__} - init] Secrets file loaded")
            except:
                logger.error(f"[{__name__} - init] Error loading secrets file")
