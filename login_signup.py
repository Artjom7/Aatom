from __main__ import app
from flask import request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from andmebaas import Kasutaja, db

# Andmebaas
def lae_ab(email):
    with app.app_context():
        return Kasutaja.query.filter_by(email=email).first()

# Registreerimine
@app.route('/registreeri', methods=['GET', 'POST'])
def registreeri():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Vormi andmete saamine
        email = request.form['email']
        parool = request.form['parool']
        parool_confirm = request.form['parool_confirm']
        # Vormi andmete kinnitamine
        # E-posti kontroll
        if lae_ab(email):
            return render_template('registreeri.html', error='E-posti aadress on juba registreeritud')
        # Väljade kontroll
        if not email or not parool or not parool_confirm:
            return render_template('registreeri.html', error='Kõik väljad on kohustuslikud')
        # Paroolide kontroll
        if parool != parool_confirm:
            return render_template('registreeri.html', error='Paroolid ei kattu')
            # Siia saab lisada emaili kinnitamise läbi posti
        # Kontroll lõppeb siin
        # Räsi parool
        rasi_parool = generate_password_hash(parool)
        # Salvesta konto andmebaasi
        nimi = email[:email.find('@')]
        for i in ['_', "."]:
            nimi = nimi.replace(i, ' ').title()
        if email[email.find('@'):] == '@opilased.nrg.edu.ee':
            info = 'Nõo Reaalgümnaasiumi õpilane'
            on_opetaja = False
        elif email[email.find('@'):] == '@nrg.edu.ee':
            info = 'Nõo Reaalgümnaasiumi õpetaja'
            on_opetaja = True
        else:
            info, on_opetaja = '', None
        db.session.add(Kasutaja(email=email, parool=rasi_parool, nimi=nimi, info=info, on_opetaja=on_opetaja))
        db.session.commit()
        # Ümbersuunamine
        return redirect(url_for('logisisse'))
    return render_template('registreeri.html')


# Sisselogimine
@app.route('/logisisse', methods=['GET', 'POST'])
def logisisse():
    if 'logged_in' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Vormi andmete saamine
        session.permanent = True
        email = request.form['email']
        parool = request.form['parool']
        # Vormi andmete kinnitamine
        # E-posti kontroll
        if not lae_ab(email):
            return render_template('logisisse.html', error='E-posti aadress ei ole registreeritud')
        # Väljade kontroll
        if not email or not parool:
            return render_template('logisisse.html', error='Kõik väljad on kohustuslikud')
        # Parooli kontroll
        if not check_password_hash(lae_ab(email).parool, parool):
            return render_template('logisisse.html', error='Vale parool')
        # Salajase võtme muutmine
        app.permanent_session_lifetime = timedelta(hours=12)
        if request.form.get('checkbox'):
            app.permanent_session_lifetime = timedelta(days=30)
        # Sisse logimine
        session['logged_in'] = True
        session['email'] = email
        # Ümbersuunamine
        return redirect(url_for('index'))
    return render_template('logisisse.html')


# Kasutatakse et välja logida kasutajat
@app.route('/valja')
def valja():
    # Väljalogimine
    session.pop('logged_in', None)
    session.pop('email', None)
    # Ümbersuunamine
    return redirect(url_for('logisisse'))
