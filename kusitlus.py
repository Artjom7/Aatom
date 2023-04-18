from __main__ import app
from flask import render_template, session, redirect, url_for, request, jsonify
from flask_socketio import SocketIO
from andmebaas import *
import datetime
import json


# URL mille läbi kasutaja saab informatsiooni andmebaasist
@app.route('/api/kysimustik')
def kysimustik():
    # Kasutaja id
    kasutaja_id = Kasutaja.query.filter_by(email=session['email']).first().id
    # Sorteeritud andmebaas
    ab_kusimustik = db.session.query(Kusimustik, Kasutaja).join(Kasutaja).order_by(Kusimustik.id)
    # Filtreerimine: kõik küsimustikud / kasutaja küsimustikud
    if request.values['sakk'] == '0':
        ab_kusimustik = ab_kusimustik.all()
    else:
        ab_kusimustik = ab_kusimustik.filter(Kusimustik.autor_id == kasutaja_id).all()
    # Lopp tulemus mida saadakse kasutajale
    tulemused = []
    for tulemus in ab_kusimustik:
        haaled_id = json.loads(tulemus[0].haalejad_id)
        valikud = json.loads(tulemus[0].valikud)
        haaled = [0]*len(valikud)
        haaled_arv = 0
        # Loendab haali
        if tulemus[0].mitmivalik:
            for i in haaled_id.values():
                if i != -1:
                    haaled_arv += 1
                    for j in range(len(i)):
                        haaled[int(j)] += i[j]
        else:
            for i in haaled_id.values():
                if i != -1:
                    haaled_arv += 1
                    haaled[int(i)] += 1
        kasutaja_nimi = ('Anonüümne' if tulemus[0].anonuumne and tulemus[1].id != kasutaja_id else \
            (tulemus[1].nimi + ' ' + tulemus[1].lend))
        haal = haaled_id[str(kasutaja_id)] if str(kasutaja_id) in haaled_id.keys() else -1
        tulemused.append({
            "kasutaja": kasutaja_nimi,
            "pealkiri": tulemus[0].pealkiri,
            "info": tulemus[0].info,
            "valikud": valikud,
            "haal": haal,
            "haaled": haaled,
            "haaled_arv": haaled_arv,
            "kuupaev": tulemus[0].kuupaev,
            "umberhaalimine": tulemus[0].umberhaalimine,
            "mitmivalik": tulemus[0].mitmivalik,
            "id": tulemus[0].id
        })
    # Saadab andmed JSON formaadis
    return jsonify(tulemused)


# Kuvab küsitluse lehekülg
def renderi_kusitlus(sakk='0'):
    return render_template('kusitlus.html', sakk=sakk)

# Küsitlus
@app.route('/kusitlus', methods=['GET', 'POST'])
def kusitlus():
    # Ümbersuunamine
    if 'logged_in' not in session:
        return redirect(url_for('logisisse'))
    if request.method == 'POST':
        filter_form = request.form["filter"]
        return renderi_kusitlus(sakk=filter_form)
    return renderi_kusitlus()


# Ootab kasutaja küsimustiku andmed ja salvestab neid
@app.route('/salvesta_info_kusitlus', methods=['GET', 'POST'])
def salvesta_info_kusitlus():
    andmed = json.loads(request.form['info_kusitlus'])
    autor_id = Kasutaja.query.filter_by(email=session['email']).first().id
    # Kuupäev
    def kokkusobiv(a):
        return a.replace('<', '&lt;').replace('>', '&gt;')

    kuupaev = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
    valikud = json.dumps(andmed['valikud'])
    db.session.add(Kusimustik(autor_id=autor_id, pealkiri=kokkusobiv(andmed['pealkiri']), info=kokkusobiv(andmed['info']),
                              valikud=kokkusobiv(valikud), anonuumne=andmed['anonuumsus'], kuupaev=kuupaev,
                              umberhaalimine=andmed['umberhaalimine'], mitmivalik=andmed['haale_tuup']))
    db.session.commit()
    return ''


# Ootab kasutaja hääli, kontrollib andmed ja salvestab need
@app.route('/salvesta_info_haal', methods=['POST'])
def salvesta_info_haal():
    andmed = json.loads(request.form['info_haal'])
    haaled_sql = Kusimustik.query.filter_by(id=str(andmed['id'])).first()
    haalejad_id = json.loads(haaled_sql.haalejad_id)
    kasutaja_id = str(Kasutaja.query.filter_by(email=session['email']).first().id)
    on_haalenud = kasutaja_id in haalejad_id
    # Kontrollib kas kasutaja oli juba hääletanud
    if not haaled_sql.umberhaalimine and on_haalenud:
        return ''
    haalejad_id[kasutaja_id] = andmed['haal']
    haaled_sql.haalejad_id = json.dumps(haalejad_id)
    db.session.commit()
    return ''
