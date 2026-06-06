from app import create_app
from models import db
import modules.user_handler as user

app = create_app()

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "timeout": 30
    }
}

# Connect Database to Flask
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()
    
    # Default Users
    default_users = [
        {"username": "doctor", "password": "doctor", "role": "doctor"},
        {"username": "reception", "password": "reception", "role": "reception"},
        {"username": "admin", "password": "admin", "role": "admin"}
    ]
    user.create_users(default_users)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
