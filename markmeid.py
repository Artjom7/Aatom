from __main__ import app
from flask import render_template, session, redirect, url_for, request, jsonify, send_file
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from andmebaas import *
from sqlalchemy import and_, not_, or_
from app import aine_tuubid
from io import BytesIO
import datetime
import json
import os

lubatud_failid = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'docx', 'pptx'}

postitaja, filtreerimine = 0, -1

@app.route('/api/markmeid')
def markmik_ajax():
    if 'logged_in' not in session:
        return redirect(url_for('logisisse'))
    kasutaja_id = Kasutaja.query.filter_by(email=session['email']).first().id
    postitaja, filtreerimine = int(request.args.get('postitaja')), int(request.args.get('filter'))
    markmikud = db.session.query(Markmeid).order_by(Markmeid.id.desc())
    andmed_markmik = []

    if filtreerimine != -1:
        markmikud = markmikud.filter(Markmeid.aine == filtreerimine)

    if postitaja == 1:
        markmikud = markmikud.filter(Markmeid.autor_id == kasutaja_id).all()
    else:
        markmikud = markmikud.filter(or_(Markmeid.privaatne == False, Markmeid.autor_id == kasutaja_id)).all()

    for i in markmikud:
        failid_len = str(len(json.loads(i.failid_id)))
        aine = (aine_tuubid[int(i.aine)] if i.aine != '-2' else 'Muu')
        postituse_autor = Kasutaja.query.filter_by(id=i.autor_id).first()
        andmed_markmik.append({'id': i.id, 'omanik': postituse_autor.id == kasutaja_id, 'autor': postituse_autor.nimi,
                'autor_lend': postituse_autor.lend, 'privaatne': i.privaatne, 'sisu': i.sisu, 'aine': aine,
                'failid_len': failid_len, 'pealkiri': i.pealkiri, 'kuupaev': i.kuupaev})
    return jsonify(andmed_markmik)


# Märkmeid
@app.route('/markmik', methods=['GET', 'POST'])
def markmik():
    if 'logged_in' not in session:
        return redirect(url_for('logisisse'))
    postitaja, filtreerimine = int(request.args.get('postitaja')), int(request.args.get('filter'))
    return render_template('markmeid.html', postitaja=postitaja, filter=filtreerimine)

# Postituse lehekülg
@app.route('/markmik/<int:posti_id>', methods=['GET', 'POST'])
def markmik_postitus(posti_id: int):
    if 'logged_in' not in session:
        return redirect(url_for('logisisse'))
    kasutaja_id = Kasutaja.query.filter_by(email=session['email']).first().id
    postitus = db.session.query(Markmeid).filter_by(id=posti_id).first()
    if not (postitus.autor_id == kasutaja_id or not postitus.privaatne):
        return render_template('postitus.html', lubatud=False)
    pealkiri = postitus.pealkiri.replace('&lt;', '<').replace('&gt;', '>')
    aine = (aine_tuubid[int(postitus.aine)] if postitus.aine != '-2' else 'Muu')
    sisu = postitus.sisu.replace('&lt;', '<').replace('&gt;', '>')
    autor = Kasutaja.query.filter_by(id=postitus.autor_id).first()
    failid = []
    for i in json.loads(postitus.failid_id):
        fail = Failid.query.filter_by(id=i).first()
        failid.append({'id': i, 'nimi': fail.faili_nimi})
    return render_template('postitus.html', lubatud=True, pealkiri=pealkiri, aine=aine, sisu=sisu, autor=autor.nimi +
                           ' ' + autor.lend, kuupaev=postitus.kuupaev, privaatne=postitus.privaatne, failid=failid,
                           omanik=autor.id == kasutaja_id)

# Salvestab uue postituse mida kasutaja tegi
@app.route('/salvesta_postitus', methods=['GET', 'POST'])
def salvesta_postitus():
    if request.method == 'POST':
        andmed = {i: request.form[i] for i in ['pealkiri', 'aine', 'sisu']}
        andmed['pealkiri'] = andmed['pealkiri'].replace('<', '&lt;').replace('>', '&gt;')
        andmed['sisu'] = andmed['sisu'].replace('<', '&lt;').replace('>', '&gt;')
        andmed['privaatne'] = bool(request.form.get('privaatne'))
        andmed['failid_id'] = []
        andmed['kuupaev'] = datetime.datetime.now().strftime('%d-%m-%Y %H:%M')
        kasutaja = Kasutaja.query.filter_by(email=session['email']).first()
        failid = request.files.getlist("file")
        if not (len(failid) == 1 and failid[0].filename == ''):
            for i in failid:
                if failid and ('.' in i.filename and i.filename.rsplit('.', 1)[1].lower() in lubatud_failid):
                    failinimi = secure_filename(i.filename)
                    fail_ab = Failid(faili_nimi=failinimi, andmed=i.read())
                    db.session.add(fail_ab)
                    db.session.commit()
                    andmed['failid_id'].append(fail_ab.id)
        postitus = Markmeid(autor_id=kasutaja.id, pealkiri=andmed['pealkiri'], sisu=andmed['sisu'], kuupaev=andmed['kuupaev'],
            aine=andmed['aine'], failid_id=json.dumps(andmed['failid_id']), privaatne=andmed['privaatne'])
        db.session.add(postitus)
        db.session.commit()
        for i in andmed['failid_id']:
            Failid.query.filter_by(id=i).first().postituse_id = postitus.id
            db.session.commit()
        return redirect(url_for('markmik', postitaja=postitaja, filter=filtreerimine))
    return redirect(url_for('index'))

@app.route('/laealla/<faili_id>')
def lae_alla_fail(faili_id):
    if 'logged_in' not in session:
        return redirect(url_for('logisisse'))
    kasutaja_id = Kasutaja.query.filter_by(email=session['email']).first().id
    fail = Failid.query.filter_by(id=faili_id).first()
    postitus = Markmeid.query.filter_by(id=fail.postituse_id).first()
    if not (postitus.autor_id == kasutaja_id or not postitus.privaatne):
        return render_template('postitus.html', lubatud=False)
    return send_file(BytesIO(fail.andmed), download_name=fail.faili_nimi, as_attachment=True)