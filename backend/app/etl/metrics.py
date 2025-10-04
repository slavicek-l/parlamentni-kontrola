from prometheus_client import Counter, Histogram

etl_lines_ok = Counter("etl_lines_ok", "ETL parsed lines OK", ["file"])
etl_lines_fail = Counter("etl_lines_fail", "ETL parsed lines failed", ["file"])
etl_duration = Histogram("etl_duration_seconds", "ETL step duration", ["step"])
