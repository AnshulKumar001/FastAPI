from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json

app = FastAPI()

DATA_FILE = "patients.json"

# ---------------- Utils ----------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- DELETE API ----------------
@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    deleted_patient = data.pop(patient_id)

    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient deleted successfully",
            "patient_id": patient_id
        }
    )


