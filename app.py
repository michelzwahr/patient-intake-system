from flask import Flask, render_template, request, jsonify, redirect, session, abort, send_file
import data_handler as dh

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

        filepath = dh.save_files(data)
        dh.save_data(data, filepath)

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
#            if username in users and check_password_hash(users[username], password):
#                session["user"] = username
#                return redirect("/dashboard")
            if dh.check_user(username, password):
                session["user"] = username
                print(session)
                return redirect("/dashboard")

        return render_template("login.html")
    
    @app.route("/dashboard")
    def dashboard():

        if "user" not in session:
            return redirect("/login")
        else:
            username = session["user"]

        return render_template("Dashboard.html")
    
    @app.route("/logout")
    def logout():
        session.pop("user", None)

        return redirect("/login")

    @app.route("/patient/<int:patient_id>")
    def get_patient(patient_id):
        if "user" in session:
            return dh.patient_info(patient_id)
    
    @app.route("/search/<string:patient_name>")
    def search(patient_name):
        if "user" in session:
            return dh.search_user_by_name(patient_name)

    @app.route("/download/<path:path>")
    def download(path):
        if "user" not in session:
            return redirect("/login")
        else:
            download = dh.provide_download(path)
            if download[0] == "error":
                abort(download[1])
            elif download[0] == "filepath":
                return send_file(
                    download[1],
                    as_attachment=True
                )

    return app