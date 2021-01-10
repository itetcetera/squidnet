from flask import Flask, render_template, Response
import cv2

#app = Flask(__name__)

#app.debug=True

def start_camera():
    camera = cv2.VideoCapture(0)
    return camera

def gen_frames(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
'''
@app.route('/')
def index():
    return render_template('video_index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(ob), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run()
'''