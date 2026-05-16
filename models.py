from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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

    p_id = db.Column(db.Integer, db.ForeignKey("patient.p_id"))

"""class Anamnese(db.Model):
    a_id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    name = db.Column(db.String(100))
    date = db.Column(db.Date)
    phone = db.Column(db.String(100))
    adress = db.Column(db.String(200))
    hausarzt = db.Column(db.String(100))
    other_doctors = db.Column(db.String(200))
    first_period = db.Column(db.Integer)
    first_period = db.Column(db.Integer)
    period = db.Column(db.String(300))
    
"""