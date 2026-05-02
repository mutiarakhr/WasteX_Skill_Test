import pandas as pd
from datetime import datetime, timezone
import pytz


def build_automation_log(cleaned_data: dict, validation_queue: pd.DataFrame, cross_log=None):
    wib = pytz.timezone("Asia/Jakarta")
    run_time_wib = datetime.now(wib)

    logs = []

    for sheet_name, df in cleaned_data.items():

        # filter log per sheet
        if isinstance(validation_queue, pd.DataFrame) and not validation_queue.empty:
            log_df = validation_queue[
                validation_queue["sheet_name"] == sheet_name
            ]
        else:
            log_df = pd.DataFrame()

        records_in = len(df)
        records_flagged = len(log_df)

        if not log_df.empty:
            records_clean = records_in - len(
                log_df[log_df.get("status", "OPEN") == "OPEN"]
            )
        else:
            records_clean = records_in

        def count_error(type_name):
            if log_df.empty:
                return 0
            return len(log_df[log_df["anomaly_type"] == type_name])

        logs.append({
            "Run_Timestamp": run_time_wib,
            "Sheet_Processed": sheet_name,
            "Records_In": records_in,
            "Records_Clean": records_clean,
            "Records_Flagged": records_flagged,

            "Errors_Comma_Decimal": count_error("Type 1"),
            "Errors_Negative": count_error("Type 2"),
            "Errors_Missing_Critical": count_error("Type 3"),
            "Errors_Duplicate_Bag": count_error("Type 4"),
            "Errors_Future_Date": count_error("Type 5"),
            "Errors_Invalid_Category": count_error("Type 6"),
            "Errors_Orphan_Bag": count_error("Type 7"),
            "Errors_Weight_Discrepancy": count_error("Type 8"),

            "Action_Taken": "AUTO_PIPELINE_RUN",
            "Notes": ""
        })

    return pd.DataFrame(logs)
