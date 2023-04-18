# Aatom - UPT Projekt
#### Sait suhtlemiseks


### Mida on vaja teha et käivitada programmi:

1. Tehke uus projekt PyCharmis, kasutades Python 3.9 Intepreter
2. Pange kõik failid sinna
3. Avage Terminal aken ja käivitage "pip install -r requirements.txt"
4. Kui koodiredaktor palub installida veel midage lisaks, tehke seda
5. Käivitage app.py fail (Kui väljastab vea, siis vaadake punkt *8)
6. Avage brauser ja minge aadressile http://localhost:5000/
7. Eelistage registreerimiseks kooli email ja seejärel logige sellega sisse (@opilased.nrg.edu.ee või @nrg.edu.ee) *Tegelikult võib kasutada ükskõik milline email

*8. https://www.jetbrains.com/help/pycharm/package-installation-issues.html#terminal 
    https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html#python_create_virtual_env
    Kui se ei tööta siis saab manuaalselt alla laadida kõik vajalikud moodulid: ctrl + alt + S -> Python Interpreter: Python 3.9 -> "+" Pluss nupp (alt+insert) -> kirjutage mooduli nimi (nt. flask-sqlalchemy) ja vajutage "Install Package".


### Kasutatud moodulid (neid võib leida ka failist "requirements.txt"):

Grupp 1: Flask-iga seotud laiendused ja moodulid

    Flask==2.2.3;
    Flask-SocketIO==5.3.2;
    Flask-SQLAlchemy==3.0.3;
    Werkzeug==2.2.3;
    itsdangerous==2.1.2;
    Jinja2==3.1.2;
    MarkupSafe==2.1.2

Grupp 2: Võrgustiku ja HTTP-ga seotud moodulid

    requests==2.28.2
    urllib3==1.26.15
    idna==3.4
    certifi==2022.12.7
    charset-normalizer==3.1.0

Grupp 3: Andmebaasiga seotud moodulid

    SQLAlchemy==2.0.6
    Flask-SQLAlchemy==3.0.3

Grupp 4: Asünkroonne programmeerimine ja samaaegsusega seotud moodulid

    gevent==22.10.2
    greenlet==2.0.2
    eventlet==0.33.3

Grupp 5: Socket suhtlus ja WebSocket-iga seotud moodulid

    python-engineio==4.3.4
    python-socketio==5.7.2


Grupp 6: Kasulikkus ja muud mitmesugused moodulid

    click==8.1.3
    six==1.16.0
    typing_extensions==4.5.0
    sentry-sdk==1.17.0
    colorama==0.4.6
    filelock==3.10.0
    zipp==3.15.0
    zope.event==4.6
    zope.interface==5.5.2
    importlib-metadata==6.0.0
    distlib==0.3.6
    docopt==0.6.2
    pipreqs==0.4.11
    yarg==0.1.9
    cffi==1.15.1
    pycparser==2.21
    dnspython==2.3.0

Grupp 7: Virtual environment-iga seotud moodulid

    virtualenv==20.21.0
    virtualenv-clone==0.5.7
    pipenv==2023.3.18
