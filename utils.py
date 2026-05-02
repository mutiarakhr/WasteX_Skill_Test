from datetime import datetime
from zoneinfo import ZoneInfo

def get_now():
    return {
        "wib": datetime.now(ZoneInfo("Asia/Jakarta"))
    }


ANOMALY_TYPE_DESC = {
    "Type 1": {"name": "Comma decimal separator", "desc": '"18,45" → 18.45'},
    "Type 2": {"name": "Negative values", "desc": "No negative values allowed"},
    "Type 3": {"name": "Missing critical fields", "desc": "Required fields missing"},
    "Type 4": {"name": "Duplicate bag_id (same batch)", "desc": "Duplicate bag_id"},
    "Type 5": {"name": "Future timestamps/dates", "desc": "Date > today"},
    "Type 6": {"name": "Invalid application_type", "desc": "Invalid category"},
    "Type 7": {"name": "Orphan bag", "desc": "Bag not found in production"},
    "Type 8": {"name": "Weight discrepancy", "desc": ">5% mismatch"},
    "Type 9": {"name": "Batch sum mismatch", "desc": "Batch mismatch"},
    "Type 10": {"name": "Bag used in multiple applications", "desc": "Duplicate usage"}
}

def log_anomaly(logs, sheet, row_idx, col, anomaly_type, value, auto_fixed=False):

    info = ANOMALY_TYPE_DESC.get(anomaly_type, {})

    now = get_now()

    logs.append({
        "sheet_name": sheet,
        "row_index": row_idx,
        "column_name": col,
        "anomaly_type": anomaly_type,
        "anomaly_name": info.get("name"),
        "description": info.get("desc"),
        "value": value,
        "detected_at": now["wib"],
        "resolved_at": now["wib"] if auto_fixed else None,
        "status": "AUTO_FIXED" if auto_fixed else "OPEN"
    })