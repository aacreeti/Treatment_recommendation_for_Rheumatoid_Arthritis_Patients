import json
from pathlib import Path

BASE_URL = "http://hapi.fhir.org/baseR4"
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

rules_file = data_dir / "treatment_recommendations.txt"

def load_recommendations():
    rules = []
    with open(rules_file, "r", encoding="utf-8") as f:
        for line in f:
            if "|" in line:
                diagnosis_code, severity, recommendation = line.strip().split("|", 2)
                rules.append({
                    "diagnosis_code": diagnosis_code,
                    "severity": severity.lower(),
                    "recommendation": recommendation
                })
    return rules

def find_recommendation(diagnosis_code, severity, rules):
    for rule in rules:
        if rule["diagnosis_code"] == diagnosis_code and rule["severity"] == severity.lower():
            return rule["recommendation"]
    return None

def extract_codes_and_severity():
    file_path = data_dir / "conditions.json"
    output_file = data_dir / "recommendations_output.txt"

    # start fresh each run
    output_file.write_text("", encoding="utf-8")

    # load recommendations from text file
    rules = load_recommendations()

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for entry in data.get("entry", []):
        resource = entry["resource"]

        # Diagnosis
        diagnosis_code = resource["code"]["coding"][0]["code"]
        diagnosis_display = resource["code"]["coding"][0]["display"]

        # Severity
        severity_code = resource["severity"]["coding"][0]["code"]
        severity_display = resource["severity"]["coding"][0]["display"].lower()

        print(f"Diagnosis Code: {diagnosis_code} ({diagnosis_display}) | "
              f"Severity: {severity_code} ({severity_display})")

        recommendation = find_recommendation(diagnosis_code, severity_display, rules)

        if recommendation:
            rec_text = (
                f"Recommendation: {recommendation}\n"
                f"Reason:\nDiagnosis Code: {diagnosis_code} ({diagnosis_display}) | "
                f"Severity: {severity_code} ({severity_display})\n"
                + "-" * 60 + "\n"
            )
            print(rec_text, end="")
            with open(output_file, "a", encoding="utf-8") as rf:
                rf.write(rec_text)

if __name__ == "__main__":
    extract_codes_and_severity()