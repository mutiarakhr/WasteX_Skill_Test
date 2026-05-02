from google.auth import default
import gspread

def get_client():
    creds, _ = default()
    return gspread.authorize(creds)

gc = get_client()

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