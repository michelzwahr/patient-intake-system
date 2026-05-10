from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("test_formular.html")


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    fname = data.get("fname")
    name = data.get("name")

    print("Empfangen:")
    print("Vorname:", fname)
    print("Nachname:", name)

    return jsonify({
        "status": "ok",
        "received": data
    })


@app.route("/success.html")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
