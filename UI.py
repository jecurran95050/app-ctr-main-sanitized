from creds.creds import *
from flask import Flask, request, render_template, redirect, url_for, session, flash, send_from_directory
from datetime import datetime, timedelta
from waitress import serve

__author__ = 'jacurran'


app = Flask(__nXXe__)
app.secret_key = b'XXXXX'
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.static_folder = 'static'

####################################################################

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    session.modified = True

####################################################################

@app.route('/')
def login():
    session['encrypted_usernXXe'] = None
    session['encrypted_password'] = None

    session["pg_creds_valid"] = None
    session["XXX_creds_valid"] = None
    session["sys_creds_valid"] = None
    session["XX_creds_valid"] = None

    return render_template('login.html')


@app.route('/', methods=['POST'])
def login_post():
    usernXXe = request.form["usernXXe"]
    password = request.form['password']
    login_result = check_XXXXXX(usernXXe,password)
    if login_result != "Login Successful":
        flash(login_result)
        return redirect(url_for('login'))
    else:
        session['encrypted_usernXXe'] = encrypt_usernXXe(usernXXe)
        session['encrypted_password'] = encrypt_password(password)
        return redirect("/r")

####################################################################

@app.route('/r')
def route():
    if session.get("encrypted_usernXXe") == None and session.get("encrypted_password") == None:
        return redirect("/")

    if session.get("pg_creds_valid") == None:
        if not web_valid_pg_creds() or web_first_pg_creds():
            session.pop('_flashes', None)
            flash("New DB Password")
            return redirect("/service/pg/r")

    if session.get("XXX_creds_valid") == None:
        if not web_valid_snow_creds():
            session.pop('_flashes', None)
            flash("New XXX Password?")
            return redirect("/service/XXX/r")

    if session.get("sys_creds_valid") == None:
        if not web_valid_sys_acct():
            session.pop('_flashes', None)
            flash("New Sys Acct Password?")
            return redirect("/service/sys/r")

    if session.get("XX_creds_valid") == None:
        if not web_valid_XX_acct():
            session.pop('_flashes', None)
            flash("New XX Password?")
            return redirect("/service/XX/r")

    session["pg_creds_valid"] = "ok"
    session["XXX_creds_valid"] = "ok"
    session["sys_creds_valid"] = "ok"
    session["XX_creds_valid"] = "ok"

    return redirect("/0")

####################################################################

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')

####################################################################

@app.route('/service/pg/<app>')
def pg(app):
    if session.get("encrypted_usernXXe") == None and session.get("encrypted_password") == None:
        return redirect("/")
    elif session.get("XXX_creds_valid") != None \
            and session.get("pg_creds_valid") != None \
            and session.get("XX_creds_valid") != None \
            and session.get("sys_creds_valid") != None:
        return redirect("/{}".format(app))
    else:
        return render_template('pg_creds.html')


@app.route('/service/pg/<app>', methods=['POST'])
def pg_post(app):
    new_pg_pw = request.form['pg_login']
    if new_pg_pw != "password":
        old_pw = get_pg_pw()
        update_pg_pw(old_pw, new_pg_pw)
        write_pg_pw(new_pg_pw)
        if web_valid_pg_creds():
            session["pg_creds_valid"] = "ok"
            return redirect("/{}".format(app))

    flash("Invalid Password!")
    return redirect("/service/pg/{}".format(app))


@app.route('/api/pgh')
def pg_pw():
    pg_hash = read_pg_hash()
    return pg_hash

####################################################################

@app.route('/service/XXX/<app>')
def XXX(app):
    if session.get("encrypted_usernXXe") == None and session.get("encrypted_password") == None:
        return redirect("/")
    elif session.get("XXX_creds_valid") != None \
            and session.get("pg_creds_valid") != None \
            and session.get("XX_creds_valid") != None \
            and session.get("sys_creds_valid") != None:
        return redirect("/{}".format(app))
    else:
        return render_template('XXX_creds.html', XXX_user=settings["XXX"]["usernXXe"])


@app.route('/service/XXX/<app>', methods=['POST'])
def XXX_post(app):
    XXX_pw = request.form['XXX_login']
    if check_snow_pw(XXX_pw) == False:
        flash("Invalid Password!")
        return redirect("/service/XXX/{}".format(app))
    else:
        write_XXX_auth(XXX_pw)
        session["XXX_creds_valid"] = "ok"
        return redirect("/{}".format(app))

####################################################################

@app.route('/service/sys/<app>')
def sys(app):
    if session.get("encrypted_usernXXe") == None and session.get("encrypted_password") == None:
        return redirect("/")
    elif session.get("XXX_creds_valid") != None \
            and session.get("pg_creds_valid") != None \
            and session.get("XX_creds_valid") != None \
            and session.get("sys_creds_valid") != None:
        return redirect("/{}".format(app))
    else:
        return render_template('sys_acct.html', sys_acct=settings["sys_acct"])


@app.route('/service/sys/<app>', methods=['POST'])
def sys_post(app):
    sys_acct = settings["sys_acct"]
    sys_pw = request.form["sys_acct"]
    if check_creds(sys_acct, sys_pw) == False:
        flash("Invalid Password!")
        return redirect("/service/sys/{}".format(app))
    else:
        wr_acct_pw(sys_acct, sys_pw)
        session["sys_creds_valid"] = "ok"
        return redirect("/{}".format(app))

####################################################################

@app.route('/service/XX/<app>')
def XX(app):
    if session.get("encrypted_usernXXe") == None and session.get("encrypted_password") == None:
        return redirect("/")
    elif session.get("XXX_creds_valid") != None \
            and session.get("pg_creds_valid") != None \
            and session.get("XX_creds_valid") != None \
            and session.get("sys_creds_valid") != None:
        return redirect("/{}".format(app))
    else:
        return render_template('XX_creds.html', XX_user=settings["XX_acct"])


@app.route('/service/XX/<app>', methods=['POST'])
def XX_post(app):
    XX_acct = settings["XX_acct"]
    XX_pw = request.form["_login"]
    if check_creds(XX_acct, XX_pw) == False:
        flash("Invalid Password!")
        return redirect("/service/XX/{}".format(app))
    else:
        wr_acct_pw(XX_acct, XX_pw)
        session["XX_creds_valid"] = "ok"
        return redirect("/{}".format(app))

####################################################################

@app.route('/0')
def homepage():
    if session.get("encrypted_usernXXe") == None and session.get("encrypted_password") == None:
        return redirect("/")
    else:
        encrypted_usernXXe = session.get("encrypted_usernXXe")
        usernXXe = decrypt_usernXXe(encrypted_usernXXe)

        return render_template('home.html', user=usernXXe)


@app.route('/0', methods=['POST'])
def homepage_post():
    app = request.form["app"]
    if app == "VLXXX Ports":
        return redirect("/1")
    if app == "VLXXX Subnets":
        return redirect("/2")
    else:
        return redirect(url_for('homepage'))

####################################################################

if __nXXe__ == '__main__':
    db = DB(db_nXXe="XXXXX")
    SQL = """
        CREATE TABLE IF NOT EXISTS auth (
            id SERIAL PRIMARY KEY,
            usernXXe VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(200) NOT NULL,
            last_updated TIMESTXXP WITH TIME ZONE DEFAULT CURRENT_TIMESTXXP 
        );
    """
    db.wr_query(query=SQL)
    db.close()

    serve(app, host='0.0.0.0', port=XXXX)
