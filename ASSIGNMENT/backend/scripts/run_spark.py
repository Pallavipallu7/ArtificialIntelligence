import json
from backend.analytics.spark_jobs import run_pyspark_analytics

if __name__ == "__main__":
    print("--- Running PySpark Analytics Job ---")
    results = run_pyspark_analytics()
    print(json.dumps(results, indent=2))
    print("PySpark Analytics job completed successfully.")
