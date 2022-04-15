import sqlite3
from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.leaders import Leaders
from data.forms import RegisterForm, LoginForm, WorksForm
from flask_login import LoginManager, login_user, logout_user, login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(id)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Leaders).all()
    return render_template("base.html", jobs=jobs)


@app.route('/cookie')
def cookie():
    return render_template('cookie.html', title='Печенье')


@app.route('/cookie_opened')
def cookie_opened():
    print(User.score)
    con = sqlite3.connect(database='db/predictions_and_players.db')
    cur = con.cursor()
    result = cur.execute(f"""UPDATE users
        SET score = score + 1
        WHERE name = 'yo'""")
    con.commit()
    con.close()
    return render_template('cookie_opened.html', title='Что же тут?')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.confirm.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            score=0
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/add_work', methods=['GET', 'POST'])
def add_work():
    form = WorksForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Leaders(
            team_leader=form.team_leader.data,
            job=form.job.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_work.html', title='Добавление работ', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    name_db = 'predictions_and_players.db'
    db_session.global_init(f"db/{name_db}")
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
