from cleaning import (
    process_bag_production,
    process_biochar_application,
    process_biochar_production
)

from validation import (
    validate_future_dates,
    cross_sheet_validation
)

import pandas as pd


def run_pipeline(all_sheets):

    df_prod, log1 = process_biochar_production(all_sheets["biochar_production"])
    validate_future_dates(df_prod, "biochar_production", log1)

    df_bag, log2 = process_bag_production(all_sheets["bag_production"])
    validate_future_dates(df_bag, "bag_production", log2)

    df_app, log3 = process_biochar_application(all_sheets["biochar_application"])
    validate_future_dates(df_app, "biochar_application", log3)

    df_bag_app = all_sheets["bag_application"].copy()
    log4 = []
    validate_future_dates(df_bag_app, "bag_application", log4)

    # ✅ fix type
    log4 = pd.DataFrame(log4)

    cross_log = cross_sheet_validation(
        df_prod,
        df_bag,
        df_app,
        df_bag_app
    )

    cleaned_data = {
        "biochar_production": df_prod,
        "bag_production": df_bag,
        "biochar_application": df_app,
        "bag_application": df_bag_app
    }

    # ✅ unified log structure
    validation_queue = {
        "biochar_production": log1,
        "bag_production": log2,
        "biochar_application": log3,
        "bag_application": log4,
        "cross_validation": cross_log
    }

    return cleaned_data, validation_queue, cross_log