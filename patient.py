from fastapi import APIRouter, HTTPException
from test_db import Itmed_db

patient_router = APIRouter(prefix="/patient", tags=["Patients"])

db = Itmed_db()

@patient_router.on_event("startup")
async def startup_event():
    db.connect()
    db.create_table_patient()

@patient_router.get("/")
async def get_patient():
    data = []
    for item in db.select_item_patient():
        patient = {
            "id": item[0],
            "first_name": item[1].capitalize(),
            "last_name": item[2].capitalize(),
            "age": item[3],
            "organization_id": item[4],
            "organization_name": item[5].capitalize(),
            "doctor_id": item[6]
        }
        data.append(patient)
    return {"Patients": data}

@patient_router.get("/{patient_id}")
async def get_patient_id(patient_id: int):
    data = {}
    wow = False
    for item in db.select_item_patient():
        if item[0] == patient_id:
            patient = {
                "id": item[0],
                "first_name": item[1].capitalize(),
                "last_name": item[2].capitalize(),
                "age": item[3],
                "organization_id": item[4],
                "organization_name": item[5].capitalize(),
                "doctor_id": item[6]
            }
            wow = True
            data = patient
    if wow:
        return {"Patient": data}
    else:
        raise HTTPException(status_code=404 or 422, detail="Patient not found")

@patient_router.post("/")
async def add_patient(
        first_name: str, last_name: str,
        age: int, org_id: int,
        org_name: str, doctor_id: int):
    data_org = db.select_item_org()
    data_doc = db.select_item_doc()
    wow = False
    for i in data_org:
        for j in data_doc:
            if org_id == i[0] and org_name.capitalize() == i[1].capitalize() and doctor_id == j[0]:
                wow = True
    if wow:
        db.add_item_patient(
            first_name.capitalize(), last_name.capitalize(),
            age, org_id, org_name.capitalize(), doctor_id
        )
        return {"Patient added": {"Patient firstname": first_name.capitalize()}}
    else:
        return {"error": "Organization or Doctor not found"}


@patient_router.put("/")
async def update_patient(
        patient_id: int, first_name: str,
        last_name: str, age: int,
        org_id: int, org_name: str, doctor_id: int
):
    data_org = db.select_item_org()
    data_doc = db.select_item_doc()
    org_found = False
    for i in data_org:
        for j in data_doc:
            if patient_id and i[0] == org_id and i[1] == org_name.capitalize() and doctor_id == j[0]:
                db.update_item_patient(
                    patient_id, first_name.capitalize(),
                    last_name.capitalize(), age,
                    org_id, org_name.capitalize(), doctor_id)
                org_found = True
    if org_found:
        return {"Patient updated": {"Patient id": patient_id}}
    else:
        return {
            "Organization or Patient or Doctor not found": {
                "Organization": org_name,
                "Patient firstname": first_name
            }
        }


@patient_router.delete("/")
async def delete_patient(patient_id: int):
    data = db.select_item_patient()
    wow = False
    for i in data:
        if patient_id == i[0]:
            wow = True
    if wow:
        db.delete_item_patient(patient_id)
        return {"Patient deleted": {"Patient id": patient_id}}
    else:
        raise HTTPException(status_code=404 or 422, detail="Patient not found")


@patient_router.on_event("shutdown")
async def shutdown_event():
    db.disconnect()

