
from flask_mysqldb import MySQL
from utils import *
from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import MySQLdb.cursors
import MySQLdb.cursors, re, hashlib
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'wake'
app.config['MYSQL_PASSWORD'] = 'DynXet05'
app.config['MYSQL_DB'] = 'Serv_Ktin'

app.secret_key = 'e4f8ac1b7c89f3a73e89458a'
mysql = MySQL(app)

bcrypt = Bcrypt(app)

@app.route("/")
def home():
    if 'loggedin' in session:
        return render_template('index.html')
    return redirect(url_for('login'))
 
@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ''
    #check si mdp et user ok
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #hash du mdp

        #check le compte
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE User_name = %s ', (username,))
        account = cursor.fetchone()

        if account and bcrypt.check_password_hash(account['Password'], password):
            
            session['loggedin'] = True
            #session['id'] = account['id']
            session['username'] = account['User_name']

            return redirect('/')
        else:
            msg = "Username/password invalid !!"

    return render_template('login.html', msg=msg)  

@app.route("/admin")
def admin():
    if 'loggedin' in session and session['username'] == 'ktin':
        return render_template("admin.html")
    elif 'loggedin' in session :
        return render_template("index.html")
    return redirect(url_for('login'))



@app.route("/status")
def status():
    return jsonify({"status": ping_pc()})

@app.route("/vpn")
def vpn():
    return jsonify({"status": ping_vpn()})

@app.route("/cpu")
def cpu():
    return jsonify({"status": check_cpu()})

@app.route("/ram")
def ram():
    return jsonify({"status": check_ram()})

@app.route("/wol", methods=["POST"])
def wol():
    wake_on_lan("107C615D34E7")
    return "Packet envoyé"

@app.route('/add', methods=['GET','POST'])
def add_db():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE user_name = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password:
            msg = 'Please fill out the form!'
        else : 
            #hash du mdp
            password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute('INSERT INTO user VALUES (%s, %s)', (username, password))
            mysql.connection.commit()
            cursor.close()
            msg = 'Utilisateur ajouter !'

    elif request.method == 'POST':
        msg = 'complete le form'
    return render_template('admin.html', msg=msg)

@app.route('/del', methods=['POST'])
def del_db():
    msg = ''
    username = request.form['username']
    password = request.form['password']
    #hash du mdp

    #check le compte
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE User_name = %s ', (username,))
    account = cursor.fetchone()

    if account and bcrypt.check_password_hash(account['Password'], password):

        cursor.execute("DELETE FROM user WHERE user_name = %s",(username,))
        mysql.connection.commit()
        cursor.close()
        msg = 'user supprimer'
        return render_template('admin.html', msg=msg)
    else:
        msg = 'Infos incorrectes'
        return render_template('admin.html', msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.50', port=5000)