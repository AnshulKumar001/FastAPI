from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated, Optional, Literal
from pydantic import BaseModel, Field, computed_field
import json

app = FastAPI()

DATA_FILE = "patients.json"

# ------------------ Utils ------------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# ------------------ Models ------------------
class Patient(BaseModel):
    id: str
    name: str
    city: str
    age: int
    gender: Literal["male", "female", "other"]
    height: float
    weight: float

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[Literal["male", "female", "other"]] = None
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)

# ------------------ PUT API ------------------
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    existing_patient = data[patient_id]

    updates = patient_update.model_dump(exclude_unset=True)
    existing_patient.update(updates)

    # Recalculate BMI + verdict
    existing_patient["id"] = patient_id
    patient_obj = Patient(**existing_patient)

    data[patient_id] = patient_obj.model_dump(exclude={"id"})
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient updated successfully",
            "bmi": patient_obj.bmi,
            "verdict": patient_obj.verdict
        }
    )


