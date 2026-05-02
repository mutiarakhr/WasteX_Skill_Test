import pandas as pd
from config import CLEANED_MAP

def export_cleaned(cleaned_data, spreadsheet):

    for key, sheet_name in CLEANED_MAP.items():
        write_to_sheet(spreadsheet, sheet_name, cleaned_data[key])


def export_validation(validation_queue, spreadsheet):

    dfs = []

    for df in validation_queue.values():
        if isinstance(df, pd.DataFrame) and not df.empty:
            dfs.append(df)

    if not dfs:
        return

    final_df = pd.concat(dfs, ignore_index=True)

    write_to_sheet(spreadsheet, "VALIDATION_QUEUE", final_df)


def export_automation_log(df, spreadsheet):

    if df is None or df.empty:
        return

    df = df.copy()
    df["Run_Timestamp"] = df["Run_Timestamp"].astype(str)
    df = df.fillna("")

    write_to_sheet(spreadsheet, "AUTOMATION_LOG", df)