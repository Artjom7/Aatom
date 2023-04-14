from flask import Flask
import os
import socket

# Uus app
app = Flask(__name__)
# Andmebaas
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# Salajase võtme seadistamine
app.secret_key = os.environ.get('SECRET_KEY') or "P|[Oc~Vmj/(1U]eAIPC*kzqOo:aq}o"

import index
import login_signup
import andmebaas
import kusitlus
import vestlus
import markmeid
from andmebaas import *
from vestlus import socketio

# On vaja et märkmete filtreerimine töötaks.
aine_tuubid = [
    'Matemaatika',
    'Eesti keel',
    'Kirjandus',
    'Inglise keel',
    'Saksa keel',
    'Vene keel',
    'Geograafia',
    'Bioloogia',
    'Keemia',
    'Füüsika',
    'Ajalugu',
    'Kehaline kasvatus',
    'Arvutiõpetus',
    'Ühiskonnaõpetus',
    'Inimeseõpetus',
    'Muusikaõpetus',
    'Kunstiõpetus',
    'UPT',
    'Valikkursus'
]

# Saadab vajaliku informatsiooni leheküljest
host = socket.gethostbyname(socket.gethostname())
port = "5000"
@app.context_processor
def inject():
    if 'logged_in' not in session:
        return {'host': host+':'+port}
    kasutaja = Kasutaja.query.filter_by(email=session['email']).first()
    return {'host': host+':'+port, 'andmed': kasutaja, 'aine_tuubid': aine_tuubid}

# Saidi kodulehe url: http://localhost:5000/
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=port)
