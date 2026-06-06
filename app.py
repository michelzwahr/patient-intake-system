from flask import Flask, render_template, request, jsonify, redirect, session, abort, send_file
import modules.data_handler as dh
import modules.user_handler as user_handler
import modules.storage_handler as storage_handler

def create_app():

    app = Flask("Patient-Intake-System")
    app.secret_key = "app-key"

    # Index: Allgemeiner Fragebogen
    @app.route("/")
    def index():
        return redirect("/allgemeiner_Fragebogen")

    # Route for submitting the form
    @app.route("/submit", methods=["POST"])
    def submit():

        data = request.json

        filepath = storage_handler.save_files(data)
        dh.save_data(data, filepath)

        return jsonify({
            "status": "ok",
            "received": data
        })

    @app.route("/success")
    def success():
        return render_template("success.html")

    @app.route("/allgemeiner_Fragebogen")
    def anamnese():
        return render_template("Fragebogen_allgemein.html")
    
    # login route
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            if user_handler.check_user(username, password): # checking if user exists and if the pwd is correct
                session["user"] = user_handler.get_user(username=username)
                # enter dashboard after succesfully loging in
                return redirect("/dashboard")

        return render_template("login.html")
    
    @app.route("/dashboard")
    def dashboard():
        # checking if current user is logged in
        if not session.get("user"):
            return redirect("/login")
        else:
            return render_template("Dashboard.html", user=session["user"])
    
    @app.route("/logout")
    def logout():
        session.clear()

        return redirect("/login")

    # Route for getting patient-data on the dashboard
    @app.route("/patient/<int:patient_id>")
    def get_patient(patient_id):
        if session.get("user"):
            return dh.patient_info(patient_id)
    
    # Route for searching patient by name on the dashboard
    @app.route("/search/<string:patient_name>")
    def search(patient_name):
        if session.get("user"):
            return dh.search_patient_by_name(patient_name)

    # Route for downloading a file
    @app.route("/download/<path:path>")
    def download(path):
        user = session.get("user")
        if user and user.get("role") in ("admin", "doctor"):
            download = storage_handler.provide_download(path)
            if download[0] == "error":
                abort(download[1]) # 403 or 404 (check 'data_handler.provide_download()')
            elif download[0] == "filepath":
                return send_file(
                    download[1],
                    as_attachment=True
                ) # With permission: provide file
        else:
            return abort(403)

    # Error-Handling
    @app.errorhandler(Exception)
    def handle_exception(e):
        # logging error in backend
        app.logger.error(e)
        return render_template("error.html")

    return app