from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__, static_folder='./client/build', static_url_path='/',)
app.config['SECRET_KEY'] = 'poggers'

socketIo = SocketIO(app, cors_allowed_origins="*")

app.debug = True

@app.route('/')
def index():
    return app.send_static_file('index.html')

@socketIo.on("message")
def handleMessage(msg):
    print(msg)
    send(msg, broadcast=True)
    return None

if __name__ == '__main__':
    socketIo.run(app)