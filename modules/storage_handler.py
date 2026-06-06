from datetime import datetime
from pathlib import Path
import json

# Saving data in the folder 'storage'
def save_files(data):
    STORAGE_DIR = Path("storage").resolve()
    # filename-format: <Document_type>_<Sirname>_<date: %d-%m-%Y--%H-%M-%S>
    filename = f"{data['type']}_{data['name']}_{datetime.now().strftime('%d-%m-%Y--%H-%M-%S')}"
    folder = STORAGE_DIR / data["type"]
    folder.mkdir(parents=True, exist_ok=True) # Preventing error if folder is not available
    filepath = folder / filename

    # Saving data as JSON-file
    with open(f"{filepath}.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    # Saving data as TXT-file
    with open(f"{filepath}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(_format_string(data))

    # Returning filepath for saving data correctly in database
    return filepath

# finds file in strorage with given name
def provide_download(filename):
    STORAGE_DIR = Path("storage").resolve()
    file_path = (STORAGE_DIR / filename).resolve().with_suffix(".txt")

    # prevent downloading other files except those in the right directory
    if not str(file_path).startswith(str(STORAGE_DIR)):
        return ["error", 403] # Error 403: forbidden

    # checks if the given path exists
    if not file_path.exists():
        return ["error", 404] # error 404: not found
    
    else:
        return ["filepath", file_path]

"""private function"""
# Format the data from a dictionary to a string (for the .txt-file)
def _format_string(data: dict):
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