from __main__ import app
from flask import render_template, session, redirect, url_for
from flask_socketio import SocketIO
from andmebaas import Kasutaja, db

socketio = SocketIO(app)

# Vestlus
@app.route('/vestlus', methods=['GET', 'POST'])
def vestlus():
    # Ümbersuunamine
    if 'logged_in' not in session:
        return redirect(url_for('logisisse'))
    return render_template('vestlus.html')

# Sessioon
@app.route('/sessions')
def sessions():
    return render_template('vestlus.html')

# Salvestab vestluse ajalugu loendis
ajalugu = []
@socketio.on('event')
def uus_sonum_sundmus(json):
    json['message'] = json['message'].replace('<', '&lt;').replace('>', '&gt;')
    ajalugu.append(json)
    socketio.emit('vastus', json)

# Annab vestluse ajalugu uue kasutajale
@socketio.on('uus_kasutaja')
def uus_kasutaja_sundmus():
    socketio.emit('vestluse_lugu', ajalugu)
