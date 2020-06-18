from app import app
from app import db
from flask import render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import SignUpForm, LoginForm, NewRoomForm
from app.models import User, Room

@app.route("/")
@app.route("/index")
@login_required
def index():
    #Consulta de rooms
    rooms_admin = Room.query.filter_by(administrator=current_user.id).all()
    return render_template("index.html", rooms = current_user.rooms, rooms_admin=rooms_admin)
    

@app.route("/group_admin/<room_id>/")
@login_required
def group_admin(room_id):
    #Consulta de rooms
    # Query si realmente es administrador del grupo
    room = Room.query.filter_by(id = room_id).first()
    # users = db.session.select(users_rooms).where(room.id = room_id)

    # users = User.query.filter_by(rooms=room_id).all()
    return render_template("group_admin.html", users = room.users, room=room)


@app.route("/group_admin/<room_id>/user/<int:user_id>/add/")
@login_required
def group_add_user(room_id, user_id):
    #Consulta de rooms
    # Query si realmente es administrador del grupo
    room = Room.query.filter_by(id = room_id).first()
    user = User.query.filter_by(id = user_id).first()
    if user:
        room.users.append(user)
        db.session.commit()
    else:
        flash("El usuario no existe!")
    return redirect("/group_admin/{}/".format(room_id))

@app.route("/group_admin/<room_id>/user/<username>/add/")
@login_required
def group_add_user_by_username(room_id, username):
    #Consulta de rooms
    # Query si realmente es administrador del grupo
    room = Room.query.filter_by(id = room_id).first()
    user = User.query.filter_by(username = username).first()
    if user:
        room.users.append(user)
        db.session.commit()
    else:
        flash("El usuario no existe!")
    return redirect("/group_admin/{}/".format(room_id))


@app.route("/group_admin/<room_id>/user/<int:user_id>/delete/")
@login_required
def group_delete_user(room_id, user_id):
    #Consulta de rooms
    # Query si realmente es administrador del grupo
    room = Room.query.filter_by(id = room_id).first()
    user = User.query.filter_by(id = user_id).first()
    room.users.remove(user)
    db.session.commit()
    # users = db.session.select(users_rooms).where(room.id = room_id)

    # users = User.query.filter_by(rooms=room_id).all()
    return redirect("/group_admin/{}/".format(room_id))


@app.route("/group_admin/<room_id>/user/<username>/delete/")
@login_required
def group_delete_user_by_username(room_id, username):
    #Consulta de rooms
    # Query si realmente es administrador del grupo
    room = Room.query.filter_by(id = room_id).first()
    user = User.query.filter_by(username = username).first()
    room.users.remove(user)
    db.session.commit()
    # users = db.session.select(users_rooms).where(room.id = room_id)

    # users = User.query.filter_by(rooms=room_id).all()
    return redirect("/group_admin/{}/".format(room_id))

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

@app.route("/group", methods=["GET", "POST"])
@login_required
def new_group():
    form = NewRoomForm()
    if form.validate_on_submit():
        #Post
        roomname = form.roomname.data
        room = Room()
        room.roomname = roomname
        room.administrator = current_user.id
        room.users.append(current_user)
        db.session.add(room)
        db.session.commit()
        flash("Grupo {} creado".format(roomname))
        return redirect("/index")
    else:
        return render_template("new_room.html", title="Nuevo Grupo",form=form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))