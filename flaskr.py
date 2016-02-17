#all import
from flask import Flask, request, session, g,redirect, url_for,\
    abort, render_template, flash
from db import *

#configuration
DEBUG = True
SECRET_KEY = 'development key'

#create app

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def home_page():
    return render_template('show_entries.html')

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    return redirect(url_for('home_page'))
def add_user(username, password):
    user = usertable(
        name = username,
        passwd = password
    )
    qsession = get_session()
    qsession.add(user)
    qsession.commit()

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        add_user(username, password)
        flash('you were register')
        return redirect(url_for('home_page'))
    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        qsession = get_session()
        username = request.form['username']
        query = qsession.query(usertable).filter_by(name=username).first()
        if(query != None):
            if query.passwd != request.form['password']:
                flash('error password, please retry')
                return redirect(url_for('login'))
            else:
                session['logged_in'] = True
                session['cur_username'] = username
                session['cur_user_id'] = query.userid
                flash('you were logged in')
                return redirect(url_for('home_page'))
        else:
            error = 'no some user'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    return redirect(url_for('home_page'))

if __name__=='__main__':
    app.run()