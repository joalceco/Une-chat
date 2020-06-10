from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import SignUpForm, LoginForm
from app.models import User

@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash("El usario ya existe")
            return redirect(url_for("signup"))
        user = User()
        user.username = form.username.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Usuario creado exitosamente")
        return redirect("/login")
    return render_template("signup.html", title="Login",form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        #POST
        #Iniciar sesión con base de datos
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No se encontro el usuario o la contraseña esta incorrecta")
            return redirect(url_for("login"))
        login_user(user, remember=True)
        flash("Iniciaste Sesión correctamente, Hola {}".format(form.username.data))
        return redirect("/index")
    return render_template("login.html", title="Login",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))