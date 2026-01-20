from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import json

from typing import Annotated, Literal
from pydantic import BaseModel, Field, computed_field

app = FastAPI()


# -------------------- MODEL --------------------
class Patient(BaseModel):
    id: Annotated[str,Field(..., description="Unique id of the patient", examples=["P001"])]
    name: Annotated[str,Field(..., min_length=1, max_length=50, description="Full name of the patient")]
    city: Annotated[str,Field(..., description="City of residence")]
    age: Annotated[int,Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal["Male", "Female", "Other"],Field(..., description="Gender of the patient")]
    height: Annotated[float,Field(..., gt=0, description="Height in meters")]
    weight: Annotated[float,Field(..., gt=0, description="Weight in kg")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 24.9:
            return "Normal weight"
        else:
            return "Obese"


# -------------------- FILE HANDLING --------------------
def load_data():
    try:
        with open("patients.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)


# -------------------- API --------------------
@app.post("/add")
def add_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    data[patient.id] = patient.model_dump(exclude={"id"})

    save_data(data)

    return JSONResponse(
        content={
            "message": "Patient added successfully",
            "patient": patient.model_dump()
        },
        status_code=201
    )
