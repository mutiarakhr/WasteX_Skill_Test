import os
import json
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_client():
    creds_json = json.loads(os.environ["GOOGLE_CREDS"])

    creds = Credentials.from_service_account_info(
        creds_json,
        scopes=SCOPES
    )

    return gspread.authorize(creds)

gc = get_client()

def load_sheets(gc):
    sheet_id_source = "1ekb_YgpSlzHUwkGrnOVXf8XjnPxadRTyIlabhCzPRrM"

    spreadsheet = gc.open_by_key(sheet_id_source)

    sheets = {}

    for ws in spreadsheet.worksheets():
        data = ws.get_all_values()

        if not data:
            continue

        header = data[0]
        rows = data[1:]

        df = pd.DataFrame(rows, columns=header)
        sheets[ws.title] = df

    return sheets

sheet_id_source = "1ekb_YgpSlzHUwkGrnOVXf8XjnPxadRTyIlabhCzPRrM"
sheet_id_cleaned = "1TjH5yD8CI4m6t0Vb5nSiHXEUz0k69i07tNFpomC1ktI"

spreadsheet_source = gc.open_by_key(sheet_id_source)
spreadsheet_cleaned = gc.open_by_key(sheet_id_cleaned)

CLEANED_MAP = {
    "biochar_production": "CLEANED_prod_batch",
    "bag_production": "CLEANED_bag_prod",
    "biochar_application": "CLEANED_app_batch",
    "bag_application": "CLEANED_bag_app"
}

VALID_TYPES = ["soil", "compost", "water", "other"]