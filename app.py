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
@app.context_processor
def inject():
    if 'logged_in' in session:
        kasutaja = Kasutaja.query.filter_by(email=session['email']).first()
        return {'andmed': kasutaja, 'aine_tuubid': aine_tuubid}
    return ''

# Saidi kodulehe url antud link konsoolis
if __name__ == '__main__':
    socketio.run(app, debug=True, host=socket.gethostbyname(socket.gethostname()), port='5000')
