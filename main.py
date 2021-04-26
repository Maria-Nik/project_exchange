from flask import Flask, render_template
from sqlalchemy.sql.functions import current_user
from werkzeug.utils import redirect

from adjob import AddForm
from data import db_session
from data.users import User
from data.jobs import Jobs
import datetime
from flask_login import LoginManager, login_user, login_required, logout_user

from loginin import LoginForm
from user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/customers.db")

    # app.run()


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.is_private == True)
    return render_template("index.html", news=news)


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
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
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
            age=form.age.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)
@app.route('/add_job', methods=['GET', 'POST'])
def addingjob():
    form = AddForm()
    if form.validate_on_submit():

        db_sess = db_session.create_session()
        if db_sess.query(Jobs).filter(Jobs.job == form.job.data).first():
            return render_template('register.html', title='Регистрация работы',
                                   form=form,
                                   message="Такая работа уже есть")
        user = Jobs(
            job=form.job.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data
        )

        db_sess.add(user)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")

if __name__ == '__main__':
    main()
    app.run(port=8080, host='127.0.0.1')
