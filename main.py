from app import create_app
from models import db
import data_handler as dh

app = create_app()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "timeout": 30
    }
}

# Datenbank mit Flask verbinden
db.init_app(app)

# Tabellen erzeugen
with app.app_context():
    db.create_all()
    
    # Standard-User im sicheren Kontext anlegen
    default_users = [
        {"username": "hzwahr", "password": "1234"},
        {"username": "bschulz", "password": "1234"}
    ]
    dh.create_users(default_users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
