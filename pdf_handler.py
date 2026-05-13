from weasyprint import HTML
from datetime import datetime
from flask import render_template

class PDFHandler:
    def __init__(self):
        pass

    def test_pdf(data):
        fname = data.get("fname")
        name = data.get("name")

        match data.get("allergies"):
            case "ja":
                allergies = data.get("allergy_details")
            case "nein":
                allergies = "Nein"
            case _:
                raise Exception("Invalid Data")
        

        html = render_template(
            "pdf_template.html",
            fname=fname,
            name=name,
            allergies=allergies
        )

        # PDF speichern
        pdf_path = "storage/pdfs/"
        pdf_name = f"{fname}_{name}_{datetime.today().strftime('%Y-%m-%d')}.pdf"

        HTML(string=html).write_pdf(pdf_path+pdf_name)

    