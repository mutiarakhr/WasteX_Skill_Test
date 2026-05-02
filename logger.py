import logging
from google.cloud import logging as cloud_logging
from google.cloud import bigquery
from datetime import datetime

# =========================
# CLOUD LOGGING
# =========================
def init_cloud_logging():
    client = cloud_logging.Client()
    client.setup_logging()
    return logging.getLogger("wastex-etl")


# =========================
# BIGQUERY LOGGER
# =========================
class BigQueryLogger:

    def __init__(self, project_id, dataset, table):
        self.client = bigquery.Client()
        self.table = f"{project_id}.{dataset}.{table}"

    def write_log(self, row: dict):

        row["timestamp"] = datetime.utcnow()

        errors = self.client.insert_rows_json(
            self.table,
            [row]
        )

        if errors:
            print("BigQuery log error:", errors)