import os

print("GOOGLE_CREDS exists:", "GOOGLE_CREDS" in os.environ)

from pipeline import run_pipeline
from export import export_cleaned, export_validation, export_automation_log
from config import spreadsheet_cleaned, gc, load_sheets
from automation import build_automation_log

def main():

    all_sheets = load_sheets(gc)

    cleaned_data, validation_queue, cross_log = run_pipeline(all_sheets)

    export_cleaned(cleaned_data, spreadsheet_cleaned)
    export_validation(validation_queue, spreadsheet_cleaned)

    automation_log = build_automation_log(cleaned_data, validation_queue, cross_log)

    export_automation_log(automation_log, spreadsheet_cleaned)

if __name__ == "__main__":
    main()
