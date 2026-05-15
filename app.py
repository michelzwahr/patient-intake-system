from flask import Flask, render_template, request, jsonify
import json
from data_handler import format_string


def create_app(pdf):

    app = Flask("Patient-Intake-System")

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/test_formular")
    def test_form():
        return render_template("test_formular.html")

    @app.route("/submit", methods=["POST"])
    def submit():

        data = request.json

        #pdf.test_pdf(data)

        """
        print("Empfangen:")
        print(data)
        """

        with open("patient_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

        print(format_string(data))

        with open("patient_data.txt", "w", encoding="utf-8") as txt_file:
            txt_file.write(format_string(data))

        return jsonify({
            "status": "ok",
            "received": data
        })

    @app.route("/success")
    def success():
        return render_template("success.html")

    @app.route("/anamnese")
    def anamnese():
        return render_template("Fragebogen_allgemein.html")

    return app