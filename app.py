from flask import Flask, render_template, request, jsonify, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import data_handler as dh


def create_app():

    app = Flask("Patient-Intake-System")
    app.secret_key = "DEIN_SECRET_KEY"

    users = {
    "hzwahr": generate_password_hash('1234'),
    "bschulz": generate_password_hash('1234')
    }

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/test_formular")
    def test_form():
        return render_template("test_formular.html")

    @app.route("/submit", methods=["POST"])
    def submit():

        data = request.json

        dh.save_data(data)

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
    
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if username in users and check_password_hash(users[username], password):
                session["user"] = username
                return redirect("/dashboard")

        return render_template("login.html")
    
    @app.route("/dashboard")
    def dashboard():

        if "user" not in session:
            return redirect("/login")
        else:
            username = session["user"]

        return render_template("dashboard.html", username=username)
    
    @app.route("/logout", methods=["POST"])
    def logout():

        session.pop("user", None)

        return redirect("/login")

    return app