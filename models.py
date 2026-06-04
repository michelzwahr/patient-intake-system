from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
-----Database-tables-----
>> using ORM (Object-Relational Mapping) to represent database with python objects
>> https://www.sqlalchemy.org/
"""

class Patient(db.Model):
    p_id = db.Column(db.Integer, primary_key=True)

    fname = db.Column(db.String(100), nullable=False)

    name = db.Column(db.String(100), nullable=False)

    birth_date = db.Column(db.Date)

class ContactData(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)

    adress = db.Column(db.String(100))

    telephone = db.Column(db.String(100))

    p_id = db.Column(db.Integer, db.ForeignKey("patient.p_id"))

class Document(db.Model):
    d_id = db.Column(db.Integer, primary_key=True)

    document_type = db.Column(db.String(100))

    path = db.Column(db.String(100))

    created_at = db.Column(db.Date)

    filetype = db.Column(db.String(10))

    p_id = db.Column(db.Integer, db.ForeignKey("patient.p_id"))

class User(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100))

    password_hash = db.Column(db.String(255))

