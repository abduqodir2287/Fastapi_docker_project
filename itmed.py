from fastapi import FastAPI, HTTPException
from itmed_db import Itmed_db
from patient import patient_router

app = FastAPI()

db = Itmed_db()

@app.on_event("startup")
async def startup_event():
    db.connect()
    db.create_table_org("organization")
    db.create_table_doc("doctors")

app.router(patient_router)

@app.get("/")
async def hi():
    return {"Text": "Hello World"}

@app.get("/organization")
async def get_organization():
    data_org = db.select_item_org("organization")
    organizations = []
    for org_id, org_name, doctors, patient in data_org:
        org_data = {"id": org_id, "org_name": org_name.capitalize(), "doctors": [], "patient": []}
        for item in db.select_item_doc("doctors"):
            if item[4] == org_id and item[5].capitalize() == org_name:
                doctor = {
                    "id": item[0],
                    "first_name": item[1].capitalize(),
                    "last_name": item[2].capitalize(),
                    "age": item[3],
                    "organization_id": item[4],
                    "organization_name": item[5].capitalize()
                }
                org_data["doctors"].append(doctor)
        for item in db.select_item_patient():
            if item[4] == org_id and item[5].capitalize() == org_name:
                patient = {
                    "id": item[0],
                    "first_name": item[1].capitalize(),
                    "last_name": item[2].capitalize(),
                    "age": item[3],
                    "organization_id": item[4],
                    "organization_name": item[5].capitalize(),
                    "doctor_id": item[6]
                }
                org_data["patient"].append(patient)
        organizations.append(org_data)
    return {"organizations": organizations}

@app.get("/organization/get/{org_id}")
async def get_organization_id(org_id: int):
    data_org = db.select_item_org("organization")
    organizations = []
    wow = False
    for i in data_org:
        if i[0] == org_id:
            org_data = {"id": i[0], "org_name": i[1], "doctors": []}
            for item in db.select_item_doc("doctors"):
                if item[4] == org_id and item[5].capitalize() == i[1].capitalize():
                    doctor = {
                        "id": item[0],
                        "first_name": item[1].capitalize(),
                        "last_name": item[2].capitalize(),
                        "age": item[3],
                        "organization_id": item[4],
                        "organization_name": item[5].capitalize()
                    }
                    org_data["doctors"].append(doctor)
            organizations.append(org_data)
            wow = True
    if wow:
        return {"organizations": organizations}
    else:
        raise HTTPException(status_code=404 and 422, detail="Organization not found")


@app.put("/organization")
async def update_organization(org_id: int, org_name: str):
    data = db.select_item_doc()
    wow = False
    for i in data:
        if i[0] == org_id:
            db.update_item_org(org_id, org_name.capitalize())
            db.update_item_org_doc(org_id, org_name.capitalize(), org_id)
            wow = True
    if wow:
        return {"Organization updated": {"Org id": org_id}}
    else:
        raise HTTPException(status_code=404 and 422, detail="Organization not found")

@app.delete("/organization")
async def delete_organization(org_id: int):
    data = db.select_item_org()
    wow = False
    for i in data:
        if i[0] == org_id:
            db.delete_item_org_doc(org_id)
            db.delete_item_org(org_id)
            wow = True
    if wow:
        return {"Organization deleted": {"Org id": org_id}}
    else:
        raise HTTPException(status_code=404 and 422, detail="Organization not found")

@app.post("/organization")
async def add_organization(org_name: str):
    db.add_item_org(org_name.capitalize(), "organization")
    return {"Organization added": {"Org name": org_name.capitalize()}}

@app.get("/organization/doctors")
async def get_doctors():
    doc = []
    for item in db.select_item_doc("doctors"):
        doctor = {
            "id": item[0],
            "first_name": item[1].capitalize(),
            "last_name": item[2].capitalize(),
            "age": item[3],
            "organization_id": item[4],
            "organization_name": item[5].capitalize()
        }
        doc.append(doctor)
    return {"Doctors": doc}

@app.get("/organization/doctors/{doctor_id}")
async def get_doctors_id(doctor_id: int):
    doc = {}
    wow = False
    for item in db.select_item_doc("doctors"):
        if item[0] == doctor_id:
            doctor = {
                "id": item[0],
                "first_name": item[1].capitalize(),
                "last_name": item[2].capitalize(),
                "age": item[3],
                "organization_id": item[4],
                "organization_name": item[5].capitalize()
            }
            wow = True
            doc = doctor
    if wow:
        return {"Doctor": doc}
    else:
        raise HTTPException(status_code=404 or 422, detail="Doctor not found")


@app.post("/organization/doctors")
async def add_doctors(first_name: str, last_name: str, age: int, org_id: int, org_name: str):
    data = db.select_item_org()
    wow = False
    for i in data:
        if org_id == i[0] and org_name.capitalize() == i[1].capitalize():
            wow = True
    if wow:
        db.add_item_doc(
            first_name.capitalize(), last_name.capitalize(),
            age, org_id, org_name.capitalize(), "doctors"
        )
        return {"Doctor added": {"Doctor firstname": first_name.capitalize()}}
    else:
        return {"error": "Organization not found"}


@app.delete("/organization/doctors")
async def delete_doctors(user_id: int):
    data = db.select_item_doc()
    wow = False
    for i in data:
        if user_id == i[0]:
            wow = True
    if wow:
        db.delete_item_doc(user_id)
        return {"Doctor deleted": {"Doctor id": user_id}}
    else:
        raise HTTPException(status_code=404 or 422, detail="Doctor not found")

@app.put("/organization/doctors")
async def update_doctors(
        user_id: int, first_name: str,
        last_name: str, age: int,
        org_id: int, org_name: str
):
    data_org = db.select_item_org("organization")
    org_found = False
    for i in data_org:
        if user_id and i[0] == org_id and i[1] == org_name.capitalize():
            db.update_item_doc(
                user_id, first_name.capitalize(),
                last_name.capitalize(), age,
                org_id, org_name.capitalize(), "doctors")
            org_found = True
    if org_found:
        return {"Doctor updated": {"Doctor id": user_id}}
    else:
        return {
            "Organization or Doctor not found": {
                "Organization": org_name,
                "Doctor firstname": first_name
            }
        }

@app.on_event("shutdown")
async def shutdown_event():
    db.disconnect()
