import json
from datetime import datetime
from pathlib import Path
from models import db, Patient, ContactData, Document
from sqlalchemy import select
import os

def format_string(data: dict):
    methods = data["contraception"]

    if methods:
        text_contraception = "\n".join(
            f'{entry["method"]} ({entry["from"]} - {entry["to"]})'
            for entry in methods
        )
    else:
        text_contraception = "Keine Verhütungsmethoden"

    medications = data["medications"]

    if medications:
        text_medications = "\n".join(
            f'{entry["name"]} (Dosis: {entry["dose"]} Seit: {entry["since"]})'
            for entry in medications
        )
    else:
        text_medications = "Keine regelmäßige Einnahme von Medikamenten"

    if data["births"] == "ja":
        births_text = f"""{data["births_nb"]}
    Wann: {data["births_time"]}
    Komplikationen: {
        data["births_complications"]
        if data["births_complications"]
        else "Nein"
    }"""
    else:
        births_text = "Nein"

    if data["pregnancy"] == "ja":
        pregnancy_text = f"""
    Ja: {data["pregnancy_details"]}
    Letzte Regel: {data["last_period_pregnancy"]}"""
    else:
        pregnancy_text = "Nein"

    return f"""Patient {data["fname"]} {data["name"]}
Geburtsdatum: {data["date"]}
Telefon: {data["phone"]}
Adresse: {data["adress"]}
Hausarzt: {data["hausarzt"]}
Mitbehandelnde Fachärzte: {data["other_doctors"]}
Erste Regel: {data["first_period"]}
Letzte Regel: {data["last_period"]}
Regel: {"Regelmäßig" if data["period_regulary"] == "ja"
        else data["period_regulary_details"]}
Verhütung: {text_contraception}
Akute Symptome: {"Nein" if data["acute_symptoms"] == "nein"
                 else data['acute_symptoms_details']}
Vorerkrankungen: {"Nein" if data["disease"] == "nein"
                 else data['disease_details']}
Allgemeine Operationen: {"Nein" if data["gen_op"] == "nein"
                         else data["gen_op_details"]}
Gynäkologische Operationen: {"Nein" if data["gyn_op"] == "nein"
                         else data["gyn_op_details"]}
Geburten: {births_text}
Fehlgeburten: {"Nein" if data["miscarriage"] == "nein"
                         else data["miscarriage_details"]}
Kinderwunsch: {"Nein" if data["child_desire"] == "nein"
                         else "seit "+data["child_desire_details"]}
Schwangerschaft: {pregnancy_text}
Medikamente: {text_medications}
Allergien: {"Nein" if data["allergy"] == "nein"
                         else data["allergy_details"]}
Einnahme von:
    Nikotin: {data["nic"]}
    Alkohol: {data["alc"]}
    Cannabis: {data["cannabis"]}
    Andere Drogen: {data["other_drugs"]}
Persönliches Anliegen: {"Nein" if data["personal_matter"] == "nein"
                         else data["personal_matter_details"]}
"""

def save_files(data):
    BASE_DIR = Path(__file__).resolve().parent
    filename = f"{data['fname']}_{data['name']}_{datetime.now().strftime('%d-%m-%Y-%H-%M-%S')}"
    folder = BASE_DIR / "storage" / data["type"]
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / filename

    with open(f"{filepath}.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    with open(f"{filepath}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(format_string(data))

    return filepath

def save_data(data, filepath):
    try:
        birth_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
    except ValueError:
        patient = Patient.query.filter_by(
            fname=data["fname"],
            name=data["name"]
        ).one_or_none()
        if patient is not None:
            birth_date = patient.birth_date
        else:
            raise Exception("No birth date specified")
    created_at = datetime.now().date()
    base_path = filepath
    document_type = data["type"]

    patient = Patient.query.filter_by(
        fname=data["fname"],
        name=data["name"],
        birth_date=birth_date
    ).one_or_none()

    if patient is None:
        patient = Patient(
            fname=data["fname"],
            name=data["name"],
            birth_date=birth_date
        )
        db.session.add(patient)
        db.session.flush()

    contact = ContactData.query.filter_by(p_id=patient.p_id).one_or_none()

    if contact is None:
        contact = ContactData(
            adress=data["adress"],
            telephone=data["phone"],
            p_id=patient.p_id
        )
        db.session.add(contact)
    else:
        contact.adress = data["adress"]
        contact.telephone = data["phone"]

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
    db.session.commit()

def select_patients():
    patients = db.session.execute(
        select(
            Patient.p_id,
            Patient.fname,
            Patient.name
        )
    ).all()
    return patients

def patient_info(patient_id):
    paths = db.session.execute(

        select(Document.path).where(
            Document.p_id == patient_id,
            Document.document_type == "Fragebogen_allgemein",
            Document.filetype == "json"
        )

    ).scalars().all()

    data_list = []

    for path in paths:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            data["filename"] = os.path.splitext(os.path.basename(path))[0]

            data_list.append(data)
    
    return data_list

