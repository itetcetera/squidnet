from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'poggers'

socketio = SocketIO(app)

app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    if username and room:
        return render_template('chat.html')
    else:
        return redirect('/')

@socketio.on('join_room')
def handle_join_room_event(data):
    for d in data:
        print(d)
    app.logger.info("{} has joined the room {}".format(data.get('username'), data['room']))

if __name__ == '__main__':
    socketio.run(app)
    