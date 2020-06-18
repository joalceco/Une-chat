from app import app,socketio
from app.models import User, Room

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Room': Room}


if __name__ == "__main__":
    socketio.run(app)