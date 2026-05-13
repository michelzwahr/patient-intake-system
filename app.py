from flask import Flask, render_template, request, jsonify


def create_app():

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

        fname = data.get("fname")
        name = data.get("name")

        print("Empfangen:")
        print(data)

        return jsonify({
            "status": "ok",
            "received": data
        })

    @app.route("/success")
    def success():
        return render_template("success.html")

    return app