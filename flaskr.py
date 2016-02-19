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
    qsession = get_session()
    entries = qsession.query(blogtable).filter_by(userid=session['cur_user_id']).all()
    return render_template('show_entries.html', entries=entries)

@app.route('/del_blog/<int:blogid>')
def del_blog(blogid):
    qsession = get_session()
    blog = qsession.query(blogtable).filter_by(blogid=blogid).first()
    qsession.delete(blog)
    qsession.commit()
    return redirect(url_for('home_page'))


@app.route('/edit_blog/<int:blogid>', methods=['GET', 'POST'])
def edit_blog(blogid):
    qsession = get_session()
    blog = qsession.query(blogtable).filter_by(blogid=blogid).first()
    if request.method == 'POST':
        blog.title = request.form['title']
        blog.text = request.form['text']
        qsession.commit()
        return redirect(url_for('home_page'))
    return render_template('edit_blog.html', blog=blog)

@app.route('/<int:blogid>', methods=['GET'])
def show_blog(blogid):
    qsession = get_session()
    blog = qsession.query(blogtable).filter_by(blogid=blogid).first()
    return render_template('show_blog.html', blog=blog)


def add_blog(userid, title, text):
    blog = blogtable(
        userid = userid,
        title = title,
        text = text
    )
    qsession = get_session()
    qsession.add(blog)
    qsession.commit()

@app.route('/publish', methods=['GET', 'POST'])
def publish():
    if request.method == 'POST':
        userid = session['cur_user_id']
        title = request.form['title']
        text = request.form['text']

        add_blog(userid, title, text)


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

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('logged_in', None)
    session['cur_user_id'] = None
    flash('you were logged out')
    return redirect(url_for('home_page'))

if __name__=='__main__':
    app.run()