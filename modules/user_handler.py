from werkzeug.security import check_password_hash, generate_password_hash
from typing import TypedDict
from models import db, Patient, ContactData, Document, User
from sqlalchemy import select

# TypedDict for user data to prevent incorrect formatting
class UserData(TypedDict):
    username: str
    password: str
    role: str

# create users from list with username and pwd
def create_users(users: list[UserData]) -> None: # TypedDict (cf. line 6)
    for user in users:
        # checking if user is already in database...
        existing_user = User.query.filter_by(username=user["username"]).first()
        # ...otherwise add user
        if existing_user is None:
            new_user = User(
                username=user["username"],
                password_hash=generate_password_hash(user["password"]),
                role = user["role"]
            )
            db.session.add(new_user)
    db.session.commit()

# validating user data
def check_user(username: str, password: str) -> bool:
    # selecting hashed passwords from database
    hashed_password = db.session.execute(
        select(User.password_hash).where(
            User.username == username
        )
    ).scalar_one_or_none()

    if hashed_password is None:
        return False
    return check_password_hash(hashed_password, password)

def get_role(username: str) -> str:
    role = db.session.execute(
        select(User.role).where(
            User.username == username
        )
    ).one_or_none()

    if role is None:
        return ""
    return role

def get_user(username: str) -> dict:
    user = db.session.execute(
        select(User.username, User.role).where(
            User.username == username
        )
    ).one_or_none()

    if user is None:
        return {}
    return {
        "username": user.username,
        "role": user.role
    }
