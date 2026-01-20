from fastapi import FastAPI , Path ,HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json') as f:
        data=json.load(f)
    return data    

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}

@app.get("/about")
def about():
   return {"Message": "This API is designed to manage patient records efficiently."} 

@app.get ("/view")
def view():
    data=load_data()
    return data

@app.get("/patients/{patient_id}")
def view_patient(patient_id: str = Path(..., description="The ID of the patient in Database ", example="P001")):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


