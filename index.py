from __main__ import app
from flask import render_template, redirect, url_for, session, request
from andmebaas import Kasutaja, db
import json

@app.route("/salvesta_info_navbar", methods=['GET', 'POST'])
def salvesta_info_navbar():
    andmed = json.loads(request.form['navbar_andmed'])
    kasutaja = Kasutaja.query.filter_by(email=session['email']).first()
    kasutaja.info = andmed["info"]
    kasutaja.lend = andmed["lend"]
    kasutaja.tunniplaan = {'12a': 'view.php?class=-16', '12b': 'view.php?class=-17', '12c': 'view.php?class=-18',
                           '11a': 'view.php?class=-19', '11b': 'view.php?class=-20', '11c': 'view.php?class=-21',
                           '10a': 'view.php?class=-22', '10b': 'view.php?class=-23', '10c': 'view.php?class=-24',
                           '-': ''}[andmed['lend']]
    db.session.commit()
    return ''

@app.route("/salvesta_info_seaded", methods=['GET', 'POST'])
def salvesta_info_seaded():
    andmed = json.loads(request.form['seaded_andmed'])
    kasutaja = Kasutaja.query.filter_by(email=session['email']).first()
    kasutaja.vana_logo = andmed["vana_logo"]
    kasutaja.varv = andmed["varv"]
    db.session.commit()
    return ''

@app.route("/varskenda", methods=['GET', 'POST'])
def varskenda():
    return ''

@app.route('/', methods=['GET', 'POST'])
def index():
    # Ümbersuunamine
    if 'logged_in' not in session:
        return redirect(url_for('logisisse'))
    return render_template('index.html')

@app.route('/api/andmed')
def saata_andmeid():
    kasutaja = Kasutaja.query.filter_by(email=session['email']).first()
    return {'varv': kasutaja.varv, 'logo': kasutaja.vana_logo}

@app.errorhandler(404)
def page_not_found(e):
    # Ümbersuunamine kui lehte ei leitud
    return render_template('404.html', error=e), 404
