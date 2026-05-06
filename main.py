from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001", "P002"])]
    name: Annotated[str, Field(..., description="Name of the patient", examples=["P001", "P002"])]
    city: Annotated[str, Field(..., description="City of the patient", examples=["San Francisco"])]
    age: Annotated[int, Field(..., description="Age of the patient", gt=0, lt=120)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., description="Height of the patient in meters", gt=0)]
    weight: Annotated[float, Field(..., description="Weight of the patient in kgs", gt=0)]

    @computed_field()
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height ** 2), 2)
        return bmi

    @computed_field()
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal"
        elif self.bmi < 30:
            return "Normal"
        else:
            return "Overweight"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]

def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {"message":"patient management system"}

@app.get("/about")
def about():
    return {"message":"A fully functional API to manage your patient record"}

@app.get("/view")
def view():
    data = load_data()

    return data

#path parameter used here = Path()
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="This is the patient ID", example="P001")):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    return HTTPException(status_code=404, detail="Patient details not found")

#this works like a query parameter
@app.get("/patient_test")
def patient_test(patient_id: str):
    load = load_data()

    if patient_id in load:
        return load[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")


#query parameter uses Query() just like a path parameter uses Path()

'''
query parameter - 
default
title
description
example/examples
min_length
max_length
ge, gt, le, lt
regex
'''


@app.get("/sort")
def sort_patients(sort_by:str = Query(..., description = "Sort on the basis of height, weight and BMI"),
                  order:str = Query("asc", description = "Sort in ascending or descending order")):
    valid_field = ["height", "weight", "BMI"]

    if sort_by not in valid_field:
        raise HTTPException(status_code=404, detail=f"not a valid field select from {valid_field}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=404, detail=f"not a valid order select from {order}")

    data = load_data()

    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse = sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: Patient):
    #load the data
    data = load_data()
    #check if patient aldready exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="patient already exists")
    #new patient add to the database
    #key = value
    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "patient created successfully"})


@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        return HTTPException(status_code=404, detail="patient doesnt exist")

    exisiting_patient_info = data[patient_id]
    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, values in updated_patient_info.items():
        exisiting_patient_info[key] = values

    #exisiting_patient_info -> pydantic object -> compute bmi and verdict automatically -> convert it back to json
    exisiting_patient_info["id"] = patient_id
    patient_pydantic_object = Patient(**exisiting_patient_info)

    exisiting_patient_info = patient_pydantic_object.model_dump(exclude='id')

    #add this dict to data
    data[patient_id] = exisiting_patient_info

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "patient updated successfully"})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient doesnt exist")

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={"message": "patient deleted successfully"})