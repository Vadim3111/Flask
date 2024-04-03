from flask import Flask, render_template, request, flash, redirect, url_for
import os
from markupsafe import escape
from config import Config
from models import User, db
from flask_wtf.csrf import CSRFProtect
from forms import RegistrationForm, LoginForm

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
csrf = CSRFProtect(app)


@app.route('/')
@app.route('/index/')
def index():
    context = {
        'title': 'Home page'
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    context = {
        'title': 'Authorization'
    }
    form = LoginForm()
    if request.method == 'POST':  # если нажали на кнопку
        username = request.form.get('username')
        password = request.form.get('password')
        if (username, password) in db():
            return "Вы вошли "
        return f'неправильный {escape(username)} логин или пароль'
    return render_template('login.html', form=form, **context)


@app.route('/form/', methods=['GET', 'POST'])
@csrf.exempt
def my_form():
    return 'No CSRF protection!'


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # Обработка данных из формы
        username = form.username.data.lower()
        surname = form.surname.data.lower()
        email = form.email.data
        user = User(username=username, surname=surname, email=email)
        if User.query.filter(User.username == username).first() or User.query.filter(User.email == email).first():
            flash(f'Пользователь с username {username} или e-mail {email} уже существует')
            return redirect(url_for('registration'))
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Вы успешно зарегистрировались!')
        return redirect(url_for('registration'))
    return render_template('registration.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)