from flask import Flask, render_template, redirect, request, abort
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from backend.data import db_session
from backend.data.users import User
from backend.data.jobs_type import JobsType
from backend.data.jobs import Jobs
from backend.data.departaments import Departament
from backend.login_form import LoginForm
from backend.add_jobs import JobsForm
from backend.departament_form import DepartamentsForm
from backend.data.db_session import global_init

app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route("/")
def index():
    session = db_session.create_session()
    jobs = session.query(Jobs).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names, title="Список работ")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html",
            message="Неправильный логин или пароль",
            form=form,
            title="Авториязация",
        )
    return render_template("login.html", title="Авторизация", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template(
            "register.html", title="Регистрация", password_error=False
        )
    elif request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        retry_password = request.form["retry_password"]
        surname = request.form["surname"]
        name = request.form["name"]
        age = request.form["age"]
        position = request.form["position"]
        speciality = request.form["speciality"]
        address = request.form["address"]
        if password == retry_password:
            session = db_session.create_session()
            user = User()
            user.email = email
            user.set_password(password)
            user.surname = surname
            user.name = name
            user.age = int(age)
            user.position = position
            user.speciality = speciality
            user.address = address
            session.add(user)
            session.commit()
            return redirect("/")
        return render_template(
            "register.html", title="Регистрация", password_error=True
        )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/jobs", methods=["GET", "POST"])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.title.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.colloborators.data
        jobs.is_finished = form.finished.data
        jobs.team_leader = form.team_leader.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("/")
    return render_template("jobs.html", title="Добавление работы", form=form)


@app.route("/jobs/<int:id>", methods=["GET", "POST"])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = (
            db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        )
        if jobs:
            form.title.data = jobs.job
            form.work_size.data = jobs.work_size
            form.colloborators.data = jobs.collaborators
            form.finished.data = jobs.is_finished
            form.team_leader.data = jobs.team_leader
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = (
            db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
        )
        if jobs:
            jobs.job = form.title.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.colloborators.data
            jobs.is_finished = form.finished.data
            jobs.team_leader = form.team_leader.data
            db_sess.commit()
            return redirect("/")
        else:
            abort(404)
    return render_template("jobs.html", title="Редактирование работы", form=form)


@app.route("/jobs_delete/<int:id>", methods=["GET", "POST"])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id, Jobs.user == current_user).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/")


@app.route("/departaments")
def show_departaments():
    session = db_session.create_session()
    departaments = session.query(Departament).all()
    users = session.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template(
        "departaments.html",
        departaments=departaments,
        names=names,
        title="Список департаментов",
    )


@app.route("/add_departament", methods=["GET", "POST"])
@login_required
def add_departament():
    form = DepartamentsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departaments = Departament()
        departaments.title = form.title.data
        departaments.chief = form.chief.data
        departaments.members = form.members.data
        departaments.email = form.email.data
        current_user.departaments.append(departaments)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect("/departaments")
    return render_template(
        "departaments_form.html", title="Добавление департамента", form=form
    )


@app.route("/departaments/<int:id>", methods=["GET", "POST"])
@login_required
def edit_departaments(id):
    form = DepartamentsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        departaments = (
            db_sess.query(Departament)
            .filter(Departament.id == id, Departament.user == current_user)
            .first()
        )
        if departaments:
            form.title.data = departaments.title
            form.chief.data = departaments.chief
            form.members.data = departaments.members
            form.email.data = departaments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departaments = (
            db_sess.query(Departament)
            .filter(Departament.id == id, Departament.user == current_user)
            .first()
        )
        if departaments:
            departaments.title = form.title.data
            departaments.chief = form.chief.data
            departaments.members = form.members.data
            departaments.email = form.email.data
            db_sess.commit()
            return redirect("/departaments")
        else:
            abort(404)
    return render_template(
        "departaments_form.html", title="Редактирование департамента", form=form
    )


@app.route("/departaments_delete/<int:id>", methods=["GET", "POST"])
@login_required
def departaments_delete(id):
    db_sess = db_session.create_session()
    departaments = (
        db_sess.query(Departament)
        .filter(Departament.id == id, Departament.user == current_user)
        .first()
    )
    if departaments:
        db_sess.delete(departaments)
        db_sess.commit()
    else:
        abort(404)
    return redirect("/departaments")


if __name__ == "__main__":
    global_init("backend/db/mars_explorer.db")
    app.run(port=8080, host="127.0.0.1")