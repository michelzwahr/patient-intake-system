import json
from datetime import datetime
import os
from pathlib import Path

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

def save_data(data):
    BASE_DIR = Path(__file__).resolve().parent
    filename = f"{data['fname']}_{data['name']}_{datetime.today().timestamp()}"
    folder = BASE_DIR / "storage" / data["type"]
    folder.mkdir(parents=True, exist_ok=True)
    filepath = folder / filename

    print(BASE_DIR)
    print(filepath.resolve())

    with open(f"{filepath}.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    with open(f"{filepath}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(format_string(data))