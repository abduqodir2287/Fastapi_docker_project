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

app.include_router(patient_router)

@app.get("/")
async def hi():
    return {"Text": "Hello World"}


@app.get("/organization")
async def get_organization():
    data_org = db.select_item_org("organization")
    organizations = []
    for org_id, org_name, doctors in data_org:
        org_data = {"id": org_id, "org_name": org_name.capitalize(), "doctors": []}
        for item in db.select_item_doc("doctors"):
            if item[4] == org_id and item[5].capitalize() == org_name:
                doctor = {
                    "id": item[0],
                    "first_name": item[1].capitalize(),
                    "last_name": item[2].capitalize(),
                    "age": item[3],
                    "organization_id": item[4],
                    "organization_name": item[5].capitalize(),
                    "patients": []
                }
                for i in db.select_item_patient():
                    if i[6] == doctor["id"]:
                        patient = {
                            "id": i[0],
                            "first_name": i[1].capitalize(),
                            "last_name": i[2].capitalize(),
                            "age": i[3],
                            "organization_id": i[4],
                            "organization_name": i[5].capitalize(),
                            "doctor_id": i[6]
                        }
                        doctor["patients"].append(patient)
                org_data["doctors"].append(doctor)
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
                        "organization_name": item[5].capitalize(),
                        "patients": []
                    }
                    for j in db.select_item_patient():
                        if j[6] == doctor["id"]:
                            patient = {
                                "id": i[0],
                                "first_name": j[1].capitalize(),
                                "last_name": j[2].capitalize(),
                                "age": j[3],
                                "organization_id": j[4],
                                "organization_name": j[5].capitalize(),
                                "doctor_id": j[6]
                            }
                            doctor["patients"].append(patient)
                    org_data["doctors"].append(doctor)
            organizations.append(org_data)
            wow = True
    if wow:
        return {"organizations": organizations}
    else:
        raise HTTPException(status_code=404 and 422, detail="Organization not found")

@app.get("/organization/patients/{org_id}")
async def get_organization_id(org_id: int):
    data_org = db.select_item_org()
    organizations = []
    wow = False
    for i in data_org:
        if i[0] == org_id:
            org_data = {"id": i[0], "org_name": i[1], "patients": []}
            for item in db.select_item_patient():
                if item[4] == org_id and item[5].capitalize() == i[1].capitalize():
                    patient = {
                        "id": item[0],
                        "first_name": item[1].capitalize(),
                        "last_name": item[2].capitalize(),
                        "age": item[3],
                        "organization_id": item[4],
                        "organization_name": item[5].capitalize(),
                        "doctor_id": item[6]
                    }
                    org_data["patients"].append(patient)
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
        for j in db.select_item_patient():
            db.update_item_org(org_id, org_name.capitalize())
            wow = True
            if i[4] == org_id:
                db.update_item_org_doc(org_id, org_name.capitalize(), org_id)
            if j[4] == org_id:
                db.update_item_org_patient(org_id, org_name.capitalize(), org_id)
    if wow:
        return {"Organization updated": {"Org id": org_id}}
    else:
        raise HTTPException(status_code=404 and 422, detail="Organization not found")

@app.delete("/organization")
async def delete_organization(org_id: int):
    data = db.select_item_org()
    wow = False
    for i in data:
        for q in db.select_item_doc():
            for j in db.select_item_patient():
                if i[0] == org_id:
                    db.delete_item_org_doc(org_id)
                    wow = True
                    if q[4] == org_id:
                        db.delete_item_org_doc(org_id)
                    if j[4] == org_id:
                        db.delete_item_org_patient(org_id)
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
    data = db.select_item_patient()
    for item in db.select_item_doc("doctors"):
        doctor = {
            "id": item[0],
            "first_name": item[1].capitalize(),
            "last_name": item[2].capitalize(),
            "age": item[3],
            "organization_id": item[4],
            "organization_name": item[5].capitalize(),
            "patients": []
        }
        for i in data:
            if i[6] == doctor["id"]:
                patient = {
                    "id": i[0],
                    "first_name": i[1].capitalize(),
                    "last_name": i[2].capitalize(),
                    "age": i[3],
                    "organization_id": i[4],
                    "organization_name": i[5].capitalize(),
                    "doctor_id": i[6]
                }
                doctor["patients"].append(patient)
        doc.append(doctor)
    return {"Doctors": doc}

@app.get("/organization/doctors/{doctor_id}")
async def get_doctors_id(doctor_id: int):
    doc = {}
    data = db.select_item_patient()
    wow = False
    for item in db.select_item_doc():
        if item[0] == doctor_id:
            doctor = {
                "id": item[0],
                "first_name": item[1].capitalize(),
                "last_name": item[2].capitalize(),
                "age": item[3],
                "organization_id": item[4],
                "organization_name": item[5].capitalize(),
                "patients": []
            }
            for i in data:
                if i[6] == doctor["id"]:
                    patient = {
                        "id": i[0],
                        "first_name": i[1].capitalize(),
                        "last_name": i[2].capitalize(),
                        "age": i[3],
                        "organization_id": i[4],
                        "organization_name": i[5].capitalize(),
                        "doctor_id": i[6]
                    }
                    doctor["patients"].append(patient)
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


# @app.delete("/organization/doctors")
# async def delete_doctors(doctor_id: int):
#     data = db.select_item_doc()
#     wow = False
#     for i in data:
#         for j in db.select_item_patient():
#             if doctor_id == j[6]:
#                 db.delete_item_doc_patient(doctor_id)
#             if doctor_id == i[0]:
#                 db.delete_item_doc(doctor_id)
#                 wow = True
#     if wow:
#         return {"Doctor deleted": {"Doctor id": doctor_id}}
#     else:
#         raise HTTPException(status_code=404 or 422, detail="Doctor not found")


@app.delete("/organization/doctors")
async def delete_doctors(doctor_id: int):
    patients = []
    wow = False

    for i in db.select_item_patient():
        if i[6] == doctor_id:
            patients.append(i)
    if patients:
        for i in patients:
            db.delete_item_patient(i[0])
    for i in db.select_item_doc():
        if i[0] == doctor_id:
            db.delete_item_doc(doctor_id)
            wow = True
    if wow:
        return {"Doctor deleted": {"Doctor id": doctor_id}}
    else:
        raise HTTPException(status_code=404, detail="Doctor not found")



@app.put("/organization/doctors")
async def update_doctors(
        doctor_id: int, first_name: str,
        last_name: str, age: int,
        org_id: int, org_name: str
):
    data_org = db.select_item_org()
    org_found = False
    for i in data_org:
        for j in db.select_item_doc():
            if doctor_id == j[0] and i[0] == org_id and i[1] == org_name.capitalize():
                db.update_item_doc(
                    doctor_id, first_name.capitalize(),
                    last_name.capitalize(), age,
                    org_id, org_name.capitalize())
                org_found = True
    if org_found:
        return {"Doctor updated": {"Doctor id": doctor_id}}
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
