from app import socketio
from flask_socketio import join_room, leave_room
from flask import session
from flask_login import current_user


# @socketio.on("initial")
# def handle_my_event(json):
#     print("recibi", str(json["value"]))
#     socketio.emit("respuesta","Ya te vi")

# @socketio.on("carro")
# def handle_my_event(json):
#     print("recibi desde carro", str(json["value"]))
#     socketio.emit("respuesta","Ya te vi")


@socketio.on("message")
def handle_my_event(json):
    print("Recibido:", str(json["data"]))
    if "room" not in session:
        pass
    else:
        json["user_id"] = current_user.id
        json["username"] = current_user.username
        socketio.emit("confirmation",json, room=session['room'])

@socketio.on('join')
def on_join(data):
    username = data['username']
    if "room" in session:
        leave_room(session["room"])        
        socketio.emit("leaved","{} se desconecto del grupo".format(username), room=session["room"])
        
    room = data['room']
    user = data['user_id']
    join_room(room)
    session['room'] = room
    socketio.emit("joined","{} se conecto al grupo {}".format(username,room), room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    socketio.send(username + ' has left the room.', room=room)

