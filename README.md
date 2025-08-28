## Introduction

This project is a rule-based Clinical Decision Support System (CDSS) for Rheumatoid Arthritis (RA). It uses Python to fetch patient data from a HAPI FHIR (R4) server, identifies RA using SNOMED CT 69896004, and applies ACR 2021 activity-stratified rules to generate concise, auditable treatment recommendations. Output is printed to the console and saved to 
```src/data/recommendations_output.txt```

### Repository Map 
```
src/
├─ data/
│  ├─ patients.json                  # FHIR Patient storage
│  ├─ conditions.json                # FHIR Condition storage (includes RA + severity)
│  ├─ treatment_recommendations.txt  # Rule from ACR RA guideline for each severity
│  └─ recommendations_output.txt     # Generated recommendations
├─ __init__.py                       
├─ fhir_patient_data_retrieval.py    # Call HAPI FHIR (fetch Patient/Condition) and store as JSON file
└─ main.py                           # Carryout the pipeline process (fetch → match rules → output)
```

## Step-by-Step: How to Run

### Prerequisites
- Python >= 3.9
- Install dependency

```commandline
pip install requests
```
- This code targets the public HAPI FHIR R4 endpoint (eg:```http://hapi.fhir.org/baseR4```)

### Step 1: Run the data fetcher python code

```
python src/fhir_patient_data_retrieval.py
```
- This file call the HAPI FHIR server to retrieve **Patient** and **Condition** resources.
- It stores the data into json file as ```patients.json``` and ```conditions.json``` in data folder
- Expected outputs:
```src/data/patients.json```updated/created
```src/data/conditions.json```updated/created

### Step 2: Run the full pipeline

```
python src/main.py
```
- This fetch the data from HAPI FHIR or reuse the stored patient.json and condition.json 
- It extractS SNOMED code for RA and severity level.
- Then it loads rules from ```src/data/treatment_recommendations.txt```
- After the rules are loaded, it matches the patient's diagnosis code and severity to the rule and gives output as recommendation in the console and stores the recommendation in ```src/data/recommendations_output.txt```

### Expected Output example:

```commandline
Recommendation: Start methotrexate monotherapy; titrate to ≥15 mg/week within 4–6 weeks if tolerated (optimize route/split dosing and folate). Avoid chronic glucocorticoids. If not at target on maximized methotrexate, add a bDMARD or tsDMARD rather than triple therapy (shared decision-making).
Reason:
Diagnosis Code: 69896004 (rheumatoid arthritis) | Severity: 6736007 (moderate)
```
- This is stored in the recommendation_output.txt file in data folder.
 