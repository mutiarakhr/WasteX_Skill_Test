from pipeline import run_pipeline
from export import export_cleaned, export_validation, export_automation_log
from config import spreadsheet_cleaned, gc, load_sheets

def main():

    all_sheets = load_sheets(gc)

    cleaned_data, validation_queue, cross_log = run_pipeline(all_sheets)

    export_cleaned(cleaned_data, spreadsheet_cleaned)
    export_validation(validation_queue, spreadsheet_cleaned)
    export_automation_log(cleaned_data, validation_queue, cross_log, spreadsheet_cleaned)

if __name__ == "__main__":
    main()