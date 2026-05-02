import pandas as pd
from config import CLEANED_MAP

def clean_for_gsheets(df):
    df = df.copy()

    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].astype(str)

    df = df.map(lambda x: str(x) if isinstance(x, pd.Timestamp) else x)
    df = df.fillna("")

    return df


def write_to_sheet(spreadsheet, sheet_name, df):

    df = clean_for_gsheets(df)

    try:
        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.clear()
    except:
        worksheet = spreadsheet.add_worksheet(
            title=sheet_name,
            rows=str(len(df) + 10),
            cols=str(len(df.columns) + 10)
        )

    data = [df.columns.tolist()] + df.values.tolist()
    worksheet.update(data)


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