from app import create_app
from models import Patient, Document, ContactData, db

app = create_app()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Datenbank mit Flask verbinden
db.init_app(app)

# Tabellen erzeugen
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)