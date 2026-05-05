import pandas as pd
from utils import log_anomaly

def process_bag_production(df):
    logs = []
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    # TYPE 1 FIX
    for idx, row in df.iterrows():
        val = row.get("weight")

        if isinstance(val, str) and "," in val:
            df.at[idx, "weight"] = val.replace(",", ".")
            log_anomaly(logs, "bag_production", idx, "weight", "Type 1", val, True)

    df["weight"] = pd.to_numeric(df["weight"], errors="coerce")

    for idx, row in df.iterrows():
        val = row.get("weight")

        if pd.notna(val) and val < 0:
            log_anomaly(logs, "bag_production", idx, "weight", "Type 2", val)

        if pd.isna(val):
            log_anomaly(logs, "bag_production", idx, "weight", "Type 3", val)

        if "bag_id" in df.columns and df["bag_id"].duplicated().iloc[idx]:
            log_anomaly(logs, "bag_production", idx, "bag_id", "Type 4", row.get("bag_id"))

    return df, pd.DataFrame(logs)


def process_biochar_application(df):
    logs = []
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    valid = ["Application-Pure Biochar", "Application-Charged Biochar", "Sale-Pure Biochar", "Sale-Charged Biochar"]

    df["application_date"] = pd.to_datetime(df["application_date"], errors="coerce")

    for idx, row in df.iterrows():

        val = row.get("application_type")

        if pd.isna(val) or str(val).lower() not in valid:
            log_anomaly(logs, "biochar_application", idx, "application_type", "Type 6", val)

    return df, pd.DataFrame(logs)


def process_biochar_production(df):
    logs = []
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()

    critical = ["timestamp", "biochar_amount_kg", "carbon_content_%"]

    for idx, row in df.iterrows():
        for col in critical:
            if col in df.columns and pd.isna(row.get(col)):
                log_anomaly(logs, "biochar_production", idx, col, "Type 3", row.get(col))

    return df, pd.DataFrame(logs)