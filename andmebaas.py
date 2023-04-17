from __main__ import app
from datetime import datetime
from flask import session

import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

# Loon uue andmebaasi 'db'
db = SQLAlchemy()
db.init_app(app)

# Kasutajad tabel
class Kasutaja(db.Model):
    __tablename__ = 'kasutaja'
    id = db.Column(db.Integer, primary_key=True)
    nimi = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    parool = db.Column(db.String(100), nullable=False)
    info = db.Column(db.String(500), default='')
    lend = db.Column(db.String(4), default='-')
    tunniplaan = db.Column(db.String(50), default='')
    on_opetaja = db.Column(db.Boolean, default=None)
    vana_logo = db.Column(db.Boolean, default=False)
    kuupaev = db.Column(db.DateTime, default=datetime.utcnow)
    varv = db.Column(db.Float, default=0)

# Küsitlus tabel
class Kusimustik(db.Model):
    __tablename__ = 'kusimustik'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('kasutaja.id'))
    pealkiri = db.Column(db.String, default='Küsimustik')
    info = db.Column(db.String, default='')
    valikud = db.Column(db.String)
    haalejad_id = db.Column(db.String, default='{}')
    anonuumne = db.Column(db.Boolean, default=False)
    kuupaev = db.Column(db.String, default='00-00-0000 00:00')
    umberhaalimine = db.Column(db.Boolean, default=False)
    mitmivalik = db.Column(db.Boolean, default=False)

# Märkmeid tabel
class Markmeid(db.Model):
    __tablename__ = 'markmeid'
    id = db.Column(db.Integer, primary_key=True)
    autor_id = db.Column(db.Integer, db.ForeignKey('kasutaja.id'))
    pealkiri = db.Column(db.String, default='Küsimustik')
    sisu = db.Column(db.String, default='')
    aine = db.Column(db.String, default='Muu')
    failid_id = db.Column(db.String)
    privaatne = db.Column(db.Boolean, default=True)
    kuupaev = db.Column(db.String, default='?')

class Failid(db.Model):
    __tablename__ = 'failid'
    id = db.Column(db.Integer, primary_key=True)
    postituse_id = db.Column(db.Integer, default=-1)
    faili_nimi = db.Column(db.String)
    andmed = db.Column(db.LargeBinary)

# Luua kõik tabelid
with app.app_context():
    db.create_all()
