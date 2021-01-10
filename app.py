from flask import Flask, render_template, request, redirect, Response
from flask_socketio import SocketIO, send, join_room
import video_record_file

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
        return render_template('chat.html', username=username, room=room)
    else:
        return redirect('/')

@app.route('/video_feed', methods=['GET', 'POST'])
def video_record():
    if(request.method == 'POST'):
        camera = video_record_file.start_camera()
        return Response(video_record_file.gen_frames(camera), mimetype='multipart/x-mixed-replace; boundary=frame')
        #return redirect('chat.html', video=video_record_file.gen_frames(camera))

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent a message: {}".format(data['username'], data['message']))
    socketio.emit('receive_message', data, room=data['room'])

if __name__ == '__main__':
    socketio.run(app)
    