import random
import requests
import json
from pathlib import Path
import datetime


BASE_URL = "http://hapi.fhir.org/baseR4"
# Directory to store files
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Extract patients records with Rheumatoid Arthritis
def fetch_patient():
    url = f"{BASE_URL}/Patient"
    f"?_has:Condition:subject:code=http://snomed.info/sct|69896004"
    f"&_sort=-_lastUpdated&_count=5"
    response = requests.get(url)
    data = response.json()
    file_path = data_dir / "patients.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data.get('entry', []))} patient records to {file_path}")

# Extract condition records of patients with Rheumatoid arthritis
def get_condition_with_details():
    url = f"{BASE_URL}/Condition?code=http://snomed.info/sct|69896004&_sort=-_lastUpdated&_count=10"
    response = requests.get(url)
    data = response.json()
    file_path = data_dir / "conditions.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(data.get('entry', []))} patient records to {file_path}")


if __name__ == "__main__":
    fetch_patient()
    # get_condition_with_details()