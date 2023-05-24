import requests
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="Nick",
                        password="",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST','GET'])
def login():
    custom_text = ''
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == '' or password == '':
                custom_text = 'Empty login or password'
            else:
                try:
                    cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                                   (str(username), str(password)))
                    records = list(cursor.fetchall())

                    return render_template('account.html', full_name=records[0][1], login=records[0][2],
                                           password=records[0][3])
                except IndexError:
                    custom_text = 'Incorrect login or password'
        elif request.form.get("registration"):
            return redirect("/registration/")
    return render_template('login.html', text_custom=custom_text)

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    custom_text = ''
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if login == '' or name == '' or password == '':
            custom_text = 'Empty name, login or password'
        else:
            try:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(login), str(password)))
                conn.commit()

                return redirect('/login/')
            except:
                custom_text = 'Login already taken'

    return render_template('registration.html', text_custom=custom_text)
