import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo


def build_automation_log(cleaned_data: dict, validation_queue: pd.DataFrame, cross_log=None):

    run_time_wib = datetime.now(ZoneInfo("Asia/Jakarta"))
    logs = []

    # normalize sheet_name once (VERY IMPORTANT)
    if isinstance(validation_queue, pd.DataFrame) and not validation_queue.empty:
        validation_queue = validation_queue.copy()
        validation_queue["sheet_name"] = (
            validation_queue["sheet_name"]
            .astype(str)
            .str.strip()
        )

    for sheet_name, df in cleaned_data.items():

        sheet_name = str(sheet_name).strip()

        if isinstance(validation_queue, pd.DataFrame) and not validation_queue.empty:
            log_df = validation_queue[
                validation_queue["sheet_name"] == sheet_name
            ].copy()
        else:
            log_df = pd.DataFrame()

        records_in = len(df)
        records_flagged = len(log_df)

        if not log_df.empty and "status" in log_df.columns:
            open_count = (log_df["status"] == "OPEN").sum()
            records_clean = records_in - open_count
        else:
            records_clean = records_in

        if not log_df.empty and "anomaly_type" in log_df.columns:
            error_counts = log_df["anomaly_type"].value_counts()
        else:
            error_counts = pd.Series(dtype=int)

        logs.append({
            "Run_Timestamp": run_time_wib,
            "Sheet_Processed": sheet_name,
            "Records_In": records_in,
            "Records_Clean": records_clean,
            "Records_Flagged": records_flagged,

            "Errors_Comma_Decimal": error_counts.get("Type 1", 0),
            "Errors_Negative": error_counts.get("Type 2", 0),
            "Errors_Missing_Critical": error_counts.get("Type 3", 0),
            "Errors_Duplicate_Bag": error_counts.get("Type 4", 0),
            "Errors_Future_Date": error_counts.get("Type 5", 0),
            "Errors_Invalid_Category": error_counts.get("Type 6", 0),
            "Errors_Orphan_Bag": error_counts.get("Type 7", 0),
            "Errors_Weight_Discrepancy": error_counts.get("Type 8", 0),

            "Action_Taken": "AUTO_PIPELINE_RUN",
            "Notes": ""
        })

    return pd.DataFrame(logs)