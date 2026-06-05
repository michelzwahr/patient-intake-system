import json
from datetime import datetime
from models import db, Patient, ContactData, Document, User
from sqlalchemy import select, or_
import os


# Saving data in the database
# only used for "Fragebogen_allgemein" -> first form every patient needs to fill out
def save_data(data, filepath):
    # Checking for valid birth date
    try:
        birth_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except ValueError:
        # checking database for birth date if it is not given...
        patient = Patient.query.filter_by(
            fname=data["fname"],
            name=data["name"]
        ).one_or_none()

        if patient is not None:
            birth_date = patient.birth_date

        # ...otherwise raise error
        else:
            raise Exception("No birth date specified")
    created_at = datetime.now().date()
    base_path = filepath
    document_type = data["type"]

    # select patient by forename, name and birth date
    patient = Patient.query.filter_by(
        fname=data["fname"],
        name=data["name"],
        birth_date=birth_date
    ).one_or_none()

    # If patient doesn't exist, create the patient
    if patient is None:
        patient = Patient(
            fname=data["fname"],
            name=data["name"],
            birth_date=birth_date
        )
        db.session.add(patient)
        db.session.flush()

    # Select Contact data by patient id
    contact = ContactData.query.filter_by(p_id=patient.p_id).one_or_none()

    # If data doesn't exist, create data...
    if contact is None:
        contact = ContactData(
            adress=data["adress"],
            telephone=data["phone"],
            p_id=patient.p_id
        )
        db.session.add(contact)
    # ...otherwise update the existing data to the new values
    else:
        if data["adress"] != "":
            contact.adress = data["adress"]
        if data["phone"] != "":
            contact.telephone = data["phone"]

    # saving documents by the path to the database
    json_document = Document(
        document_type=document_type,
        path=str(base_path.with_suffix(".json")),
        created_at=created_at,
        filetype="json",
        p_id=patient.p_id
    )

    txt_document = Document(
        document_type=document_type,
        path=str(base_path.with_suffix(".txt")),
        created_at=created_at,
        filetype="txt",
        p_id=patient.p_id
    )

    db.session.add(json_document)
    db.session.add(txt_document)
    # commiting all changes
    db.session.commit()

# sql-request for selecting patients
def select_patients():
    patients = db.session.execute(
        select(
            Patient.p_id,
            Patient.fname,
            Patient.name
        )
    ).all()
    return patients

# provide patient info for the dashboard
def patient_info(patient_id: int) -> list:
    paths = db.session.execute(
        select(Document.path).where(
            Document.p_id == patient_id,
            Document.filetype == "json"
        ) # find all json documents

    ).scalars().all()

    data_list = []

    # cycle through all paths which where found
    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # add parameter filename and filepath,
            # so the entries at the dasboard can be specified
            data["filename"] = os.path.splitext(os.path.basename(path))[0]
            data["filepath"] = os.path.relpath(path, "storage")

            data_list.append(data)
    
    return data_list



# sql query to search user by name
def search_patient_by_name(name: str) -> json:
    search_result = db.session.execute(
        # select forename, name and the id
        select(Patient.fname, Patient.name, Patient.p_id).where(
            or_(
                Patient.name.ilike(f"%{name}%"), # cf. sql"WHERE <attribute> LIKE <'%value%'>"
                Patient.fname.ilike(f"%{name}%") # searching name and forename
            )
        )
    ).all() # returns list with all search results

    result = []
    for element in search_result:
        result.append(
            {
                "fname": element[0], # index 0: forename
                "name": element[1],  # index 1: name
                "id": element[2]     # index 2: p_id
            }
        )
    return json.dumps(result) # return json file
