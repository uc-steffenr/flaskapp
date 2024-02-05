from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from collections import Counter

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Used for flashing messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    # info to be displayed
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('info', username=username))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
        else:
            new_user = User(username=username, password=password,
                            first_name=first_name, last_name=last_name, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Account created for {username}! You can now log in.')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/info/<username>')
def info(username):
    user = User.query.filter_by(username=username).first()
    
    count_str = """<html lang="en">\n\t<body>"""
    word_counter = Counter(open('Limerick.txt', 'r').read().lower().replace('\n', ' ').replace(':', '').replace('?', '').split(" "))
    
    for word, count in word_counter.most_common():
        count_str += fr'<br> "{word}": {count}'
    
    tot_html = render_template('info.html', user=user) + count_str
          
    return tot_html

@app.route('/download')
def download_file():
    flash('Downloading Limerick file!')
    return send_file(os.path.join(os.getcwd(), 'Limerick.txt'), as_attachment=True, download_name='Limerick.txt')


if __name__ == '__main__':
  app.run()