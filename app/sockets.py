from app import socketio

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
    socketio.emit("confirmation",str(json["data"]))
