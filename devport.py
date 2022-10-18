from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import difflib


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'the random string'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return 'Users %r' % self.id


with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        flash('Такой логин занят', 'info')
        return render_template('registration.html')
    if request.method == 'POST':
        login = request.form['login']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha1')
        if request.form['password'] == request.form['repeate_password']:
            user = Users(login=login, password=password)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('signup.html')
            except:

                return 'Такой логин уже занят'
        else:
            return 'Пароли не совпадают'


@app.route('/signup.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        input_login = request.form['login']
        password = request.form['password']
        if Users.query.filter_by(login=input_login).first():
            user = Users.query.filter_by(login=input_login).first()
            print('Логин верный')
            if check_password_hash(user.password, password):
                print('Пароль верный')
                return redirect('match.html')
            else:
                return redirect('resignup.html')
        else:
            return redirect('resignup.html')
    if request.method == 'GET':
        return render_template('signup.html')


@app.route('/resignup.html', methods=['GET', 'POST'])
def resignup():
    if request.method == 'GET':
        return render_template('resignup.html')
    if request.method == 'POST':
        input_login = request.form['login']
        password = request.form['password']
        if Users.query.filter_by(login=input_login).first():
            user = Users.query.filter_by(login=input_login).first()
            print('Логин верный')
            if check_password_hash(user.password, password):
                print('Пароль верный')
                return redirect('match.html')
            else:
                return redirect('resignup.html')
        else:
            return redirect('resignup.html')


@app.route('/match.html', methods=['GET', 'POST'])
def match():
    if request.method == 'GET':
        return render_template('match.html')
    if request.method == 'POST':
        team_1 = request.form['team_1']
        team_2 = request.form['team_2']
        temp = difflib.SequenceMatcher(None, team_1, team_2)
        ratio = temp.ratio()
        return render_template('match.html', ratio=ratio, team_1=team_1, team_2=team_2)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
