import pandas as pd
from utils import log_anomaly
from datetime import datetime, timezone


def validate_future_dates(df, sheet_name, logs):

    df = df.copy()
    df.columns = df.columns.str.lower().str.strip()

    map_col = {
        "biochar_production": ["timestamp"],
        "biochar_application": ["timestamp", "application_date"],
        "bag_application": ["timestamp"],
        "bag_production": ["timestamp"]
    }

    cols = map_col.get(sheet_name, [])

    for col in cols:
        if col not in df.columns:
            continue

        dt = pd.to_datetime(df[col], errors="coerce")

        for idx in df[dt > pd.Timestamp.today()].index:
            log_anomaly(
                logs,
                sheet_name,
                idx,
                col,
                "Type 5",
                df.loc[idx, col]
            )


def cross_sheet_validation(df_prod, df_bag, df_app, df_bag_app):

    logs = []

    now_utc = datetime.now(timezone.utc)
    now_wib = datetime.now(timezone.utc).astimezone()

    def log(sheet, idx, col, typ, desc, val):
        logs.append({
            "sheet_name": sheet,
            "row_index": idx,
            "column_name": col,
            "anomaly_type": typ,
            "description": desc,
            "value": val,
            "detected_at_utc": now_utc,
            "detected_at_wib": now_wib,
            "status": "OPEN"
        })

    valid = set(df_prod["activity_id"].dropna())

    for idx, row in df_app.iterrows():
        if row.get("activity_id") not in valid:
            log(
                "biochar_application",
                idx,
                "activity_id",
                "Type 7",
                "orphan",
                row.get("activity_id")
            )

    merged = df_app.merge(
        df_prod[["activity_id", "biochar_amount_kg"]],
        on="activity_id",
        how="left"
    )

    merged["idx"] = df_app.index

    for _, r in merged.iterrows():
        if pd.notna(r["total_weight"]) and pd.notna(r["biochar_amount_kg"]):
            diff = abs(r["total_weight"] - r["biochar_amount_kg"]) / r["biochar_amount_kg"]
            if diff > 0.05:
                log(
                    "biochar_application",
                    r["idx"],
                    "total_weight",
                    "Type 8",
                    "mismatch",
                    r["total_weight"]
                )

    dup = df_app[df_app["activity_id"].duplicated(keep=False)]

    for idx, row in dup.iterrows():
        log(
            "biochar_application",
            idx,
            "activity_id",
            "Type 10",
            "duplicate usage",
            row["activity_id"]
        )

    return pd.DataFrame(logs)