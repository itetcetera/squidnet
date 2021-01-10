from flask import Flask, render_template, request, redirect, Response
from flask_socketio import SocketIO, send, join_room
import cv2
import base64
import threading
import video_record_file

app = Flask(__name__, static_folder='./client/build', static_url_path='/')
app.config['SECRET_KEY'] = 'poggers'

socketio = SocketIO(app)
socketio.init_app(app, cors_allowed_origins="*", always_connect=True, ping_timeout=5)

app.debug = True

@app.route('/')
def index():

    # socketio.emit('receive_image', 'Pog')

    return render_template('index.html')

@app.route('/websocket')
def websocket():
    print('chat')
    cap = cv2.VideoCapture(0)
    cap.release()

    t = threading.Thread(target=infinite_loop, args=(socketio,))
    t.daemon = True
    t.start()

    return app.send_static_file('index.html')



@app.route('/chat')
def chat():
    username = request.args.get('username')
    room = request.args.get('room')

    # print('chat')
    # cap = cv2.VideoCapture(0)
    # cap.release()

    # t = threading.Thread(target=infinite_loop, args=(socketio,))
    # t.daemon = True
    # t.start()

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

@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    app.logger.info("POOG")

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

    # Process the image frame
    frame = imutils.resize(frame, width=700)
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    emit('response_back', stringData)

@socketio.on('join_room')
def handle_join_room_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data)

@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has sent a message: {}".format(data['username'], data['message']))
    socketio.emit('receive_message', data)

@socketio.on('pong')
def pong(data):
    print(data)

def liveCamEdgeDetection_canny(image_color):
    threshold_1 = 30
    threshold_2 = 80
    image_gray = cv2.cvtColor(image_color, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(image_gray, threshold_1, threshold_2)
    return canny

def flip(image):
    image_flip = cv2.flip(image, 1)
    return image_flip

def infinite_loop(socket):
    import time
    print('STARTING BOIS')
    num = 0
    cap = cv2.VideoCapture(0)
    
    while True:
        if not cap.isOpened():
            break
        ret, frame = cap.read()
        if not ret:
            print('Unpog')
            break

        resized = cv2.resize(frame, (256, 144))

        # cv2.imshow('live edge detection', liveCamEdgeDetection_canny(frame))
        # cv2.imshow('webcam', frame)

        #store pixel data
        # pixels = [liveCamEdgeDetection_canny(frame)]
        # image_todraw = np.array(pixels)
        # image_todraw = np.reshape(image_todraw, (480, 640))

        im_save = liveCamEdgeDetection_canny(resized)
        img_not = cv2.bitwise_not(im_save)
        #im_save = flip(im_temp)
        # cv2.imwrite('test1.png', img_not, [cv2.IMWRITE_PNG_COMPRESSION, 9])

        ret, buffer = cv2.imencode('.png', img_not)
        im_base64 = base64.b64encode(buffer)
        im_trim = str(im_base64)[2: -1]
        
        socket.emit('receive_image', str(im_trim))
        num += 1
        print(num)
        # print(im_trizm)



        if cv2.waitKey(1) == ord('q'):
            break

        

        time.sleep(0.2)



    cap.release()
    cv2.destroyAllWindows()

# def infinite_loop(socket):
#     import time
#     num = 0
#     print('STARTING')

#     while num < 10000:
#         num += 1
#         print(num)
#         print(socket)
#         socket.emit('receive_image', num)
#         socket.emit('receive_image', 'iVBORw0KGgoAAAANSUhEUgAAAaoAAADwCAAAAAB0hn8PAAAc0UlEQVR42u1diXLjuA5kp/T/v9y7Y4kkQAI8dFlOnHpbL5M4PggCaDQuMHy/7C/w3/+279yHzD/p3kf9fEUycnQnin/311dUA190ZIVb38VXVHtk9e9fAMKt3mP5ymFIVsimC9t/xL1+/iuqYVllFdu8DqfV6pBwv6IatoH6sP/BQ95qA7++6oCiBf4vsAlscQyGfLVq/JxZGDOuyjasWQdV8KtVcyaQqLTknx3E9ZL6atVJWB6hJ4jDbu0rqlOoB0YAbzooniGpr6jmwQQbBnKVi3oIt0DsMFT8iuoKU4jALC+EvnX8iuoi/Wk94PXDNejSEdlXVM/wVY2g+RsCP4W+uCq6/gitwn1HcoldvOpreZ6MaP2UrjAZTnLbDxKa+cTLg6REHwMTrqIlfIxrVfFt2vQkUTlKgc1ks332NBISVzDe75bUA0SFRozP+L16kIpaohz5ZP/2G0QFkQgCS6MmDz4qyj8N0sLAA0VzUAVNY7u8VUxBsmisgn71wak9VnJO5M3583c5reVtUmqrAtXdBLM+JZy4qtlL23hD9dCUhK4Q5/IWQXHyA/MVFSLJ5+W+NjwR87DV4ZwMLcA3K93yUEEhHRCywUswD68Koq38Vame8FyyyugLK04D5pY4sSlMsoWMdnCTWVExFKF9QupE+IrqWkGJUCrngMJadCLDrM0gInkugufRF6VKThm2K/R5eZ6cjBA3Gbp/OkNZkbdauTJfvqoWNkGec2x/JwTe4+SRLGFQHgil2SvwogSIPB9jtPXrMpEuD5ZUsnOQbonO8YA5AssdNxlq3BUpn4EA8T5R7TqmhA5sSYsfQUorHxgoVGyqYu/dX+/LV00dUS41FmDbyoGweHqoC13UEK0q9tHwfXmapHp3K2zRcMVIgSHULK7+ljhkBlNE/haJ/zxXUsFli/5JhyWWrqxsUfO6Rl3car0+MOT6eZqkQFMtBiHIKhAA2KBELZNX3TLD58lqeZxOFampRm7YtI0QjooKekBayg90W8vTJMXij7H7zyMI3Cxf1ljk2PkrqoMEhYZx3CXk1aVFEhGCNNxQ+4isHiXMn4tV6siHxd5Q6J9guFEca7cadbKSCYiMP+OvFtUpEecukoMyIFuVi6IdFNF1Yee7eAtn//NkSZ10l/lCfUmN8rePxYG3T4M5rFM8IdbcRhesOrX5Lm4w47GyMrX2MlGdpBE47b4kYcWKDHwOJ3ipqPYhCtTw4ESBbwniVbHQx5bibmP88n+YqIBdNUSo0IGwUAeO5Z9gXh7qlcWK00LYO+2C/H03dr9GVOQujB3o8g/AQVuYkMWmWERkoXwwUpLCtynRzbBiEhEAsK84V2zN0ZkDjWA8KVZs+uyG6Gh6zXv5jutgxbxvM/Hey2KtJbTcH1Bzq8/Yvv33UpwxaDeHwPciwKlsItJoFeNwUP1oh3oxV8FvNTLoXSicGng8GQHOYBBWjgBiVhjSOAEgPn7Lc0ybwC2uwmyxxe8llsbnDm0KpaHx64epgoXcYiBmIKbR4bCSMylWCn+HEPetSuVcwquYdY7f9MrO5YKI7SRFpxv2hzXYAGVMV63/jc+yuhP+Pa1tWwiqLFjRigCGuqoB4x9c/CmIlK6aKee8nYKqIdZy0+u4NrIoP8raw1J7wPLPJ7ODa4kuYwE8hijGQtS3XGDbYCzvVqhSSyiDIGkLyhiY02GNblGN9m90UMhtnXbei72pFU6MjsquXoA/prFSWVpMlNWERYJjzRBldY1d+8RWOOMtQxxYMBp7czmt4UxEmp2TqiTbjbnKatIHlQLgiWsN3i4qNE+PFQwssIXocsM+2CdRCir+9aOKzJarROSY3LXMweqlp4XglQ5wj21plRW+TOAlGvBBBpBOVSTKwS2ig0D2hxbhDmGAxbEzbj7ooyrMLguBYR4SZe1kkOZNg4tcXJ5hRDSXubZvRE7sXqknCuvOGUu+w627OhiKsRUCs4PFjNEtmuLohemrf3sLwXPUbrntUliBr2r2NVWQKlkbceHE+XWz8q+W1QNrpT7eALYi30o0bLlnFOh9DgRySPU+ohf/KgRogIoE89iyiAaUWiuNZG/AyGtz7u3+XVgRjBGM3HPvWbQMjNB20+zqiKR2D0M46x7cOLv24DvGIOpbU1mBp+xV2fueVQUNniyqBp20W9BMO76G5Dp1l536m2cZyWcPQ6hCtdGUJacs1mfEwddVLPFkSc1YozxXZDAb/wkQ8K4ymHPu7Vyx7eEil2cJ8L21FTuMYBzbwwG1Nph7P7Li0+3iJVoVmy1S7Q3OvAIcrFaK4TK5W612wZGP81VBLY088X5i8Bn1GkR0bcDjvdUlooo2al+XwdiTY+CuvKrcN4jfC7OeDwJvCYFPNPoxAzKWuuBa7kmGjskcsGQ7jR0+S1RnI5bJGugxHNITxXd7wbT5m+50Uq1vreftv/Jbrcotk8tKKv1mx7Bh9u6BXaE3OG8K4XLZ3XffejE4ZPKAuBcbsgcCL0HePK83/GYDCD2IhQIu7hdYsdTQPRv/0MALfdFn7losAy2R1xgobkExRSmVXci041Yu4Vzw5hO/aXzwm0Xl9IpWBX71bzFUsQpRQ11NTXWXX3uy4DZwf1YY90rvMq2CNxfYSaZTN0C5Sinkk3L3tJ5swkeAfRv5/q8L6wCtn211XOaJZPvl3/60ZqwLI+cyixQjEv6aqNpwSGTTqQcO+Kn2XMbOsNtXw57SzqHSwjd7q8tEVWmG3kFgwbI8hNtB4rBqoFFDBk4zEhxBgYayTzXTPV+r0Nx7Q8Ndedgx206mcfct8Q4DC1w5mecTwTqnHyLAPSpxou716d8aW1Z7XNTt5vA6UVWHwsYHdrRJLIuoeKI9t5VtJzgfJN4przevxZRbZX14Tb3elPvNivMSGNMdlkPgsefKfpqoDLDtd8yr3hvst0F+4xv7hk7fl+gzbzSVP5erjfkbXfEAiNmKlheJOwnUfAuAQy/WfxB2HPh0pduTtcr31ZDjXoLoDqkVC4LezZ4r9XNnppYDddJ0hgrmdwpeYMg+1wBCLgBTQJ3GNAqxbzZ7KZTxWdTSDolhZTowOHf/T2aBqeWVGoJNXCHCprg7US4IVk/JgX1ipnL85f6q3v2E7KsXm39FJ70CA2kvZmZsWfK+G43LueHEkBqDr6hKpKeGkSLbION2l8v5kqSMHSDJpWGit5ddKG+r4+37xm6vWEJa+pBsG7MLqsZ3v0oJ81QY5OSH3k0VnwS9hsXiNugQeya1eLvv+rnD3JUh0ms0Y1wlADnEgl5vVknPolSqhOTnCs+oE9H4GkBtqtRwiuhbfMpUR54ivQi9EDNNSZi/8JcWV3yoqCqGKI2kNYgaVMfOiEmY+A1EdVRzIMd9DmItTq+8EL9YVLXjVWcPtak+9GovxI+oRadxAWYzwCpemOekfqdWrRAdYolUaAlKYHX/ClCBA84T7uMViQx/R1RbGXOSkBzG6Exk6oPiOItYVBheULHM93uyK0VlhDBEPU0JaJSgWjGxkVUUYIJ5gf1u/XJwx3v16tKtcNZx0FrU6/fU2GMKzEdTS/8sCuwxBvD+rXCuoZt66iZrd9rgOBny4d2jmB7fX7UDKFxy/avI63a5PV5UuFkczZf4rVp1yrV76xDMkwo6/opWfb9ugRX4Ncf0BH5w+Xu3041mm4UV4e0k4PKWQ5kCFWff6F3P94u3wu2FTEW2iQzfr1tEtau4+Fql2r+vBcDvFRVOEC7OOunj4P9PMet7MGQZlr4LjP2B2opjKsiHUQZfBBiXvpW5dCORfCwjxa+ojsLiMVIWW9PuExfk4Oqb8HOtVo1ismr5jmPuEEtm7reC5YfR/17L5fixWjVqkwxB2UMTcgMwzk/JHtPU69X8GQhQVldsLgveuoh1yMQTqytxrcTeLaq8oFQMtcrzDcz2+aeObOEna1UxqMq8iNXKPgiBWBUyUaF2GaxJMbf6FAy78Ku1ivXQaOZNLfbgw9TJeAvv6l03AzPxg7Vq52eg7CVsZiaut4Tt+4DajX6oqLbhbTvOhGAAjSYeec93SerMkIxV1MHr2JR7fNXQQ1FuCBblDOXi4N2O4dD+y7qhUv32YlT6GLr2RUSkbaW6D0EM+NO7Fy++Pn1pyvlc+GgEOO6zV3zBElAJyL51Cou5PfhbecenaJU1da4cg0DoKJknqcZJVoEfLqqx5eWOpCA1LhwahDVENRwwnLw+RXyxqIj+oOV6AoXomK8nD18lqemB+TRj4Ou+Lk8t9hbcWMHRC0HEaRUF0jvP0OCa8BUfqlUjW+TrT8rTMFtLPXj66YLhwkLV62HF1ObjQItH4pmwQIETq3zjqV+XG8CZ9aA1M4tqEsXxOHOdTpJzgeS8fXhHjfezKpYEAqe3/Y84mhjiVdCEn61VMytfbfhgtaQe0S0paDT9IK/6pA8V1egBZjO3jtNcC/qxTTSDoRnHXm728hQX6TCceiKsGNkLkAITJiZiRex5UipTDHa8LY355fY9TffvLjCGy/WSGul3TzEUVIYxTyBY5zEhDi075KrAsIOYJ/i7p8FgaN0aFWqOmrTmReSutzwTcJu4yQNvCx9G916uVRzQOj1pqVho3hi2vXs+RRqTO+FRfvvsWvQs+6YbkjLfHEj3HBF2j6ia3lDxF7RqxEvFLAfid3FwXG+MCML+KiH0NjNOI4nPZivQg67IJHpemTlOIKyr1/fi4i2jjGHZ4vdqFcaVKgRdWTGRkpjyWKLccHOE/BR4sVyqUn1JaRtWTNrU/6Qrqz0WmULlP0NWyz2C8g09Q7FGh4UsKPiFXCS983whX43gJ8lquUxSM0ap9Go0F/Hk/wNlMdphmMOxDbe/UlTjsGzjAAoafVtkgLhbVJ9c3EcEzNbCaE5PMCOurGod/F0IEDaEgxcAo+RsuLEJcoBqrbB7IBl2ozswvBcD/lwjqdFzMgW1ITNSM02vR0L2wE1HwNwynfWahDEpvFWxljsk1XDfrBsWGRsTxXJ7tRN4yMk0j5q1QXs+tjhdqwCjzgrxF33idp1ku6bSAUsT1SqQGZP0UkpLPzJh/2ClusAA0tlBNbzKgSmRyFSo7iotxxnXosam8k9PB+xniwpBc0kopTUmbKybFFftaldszi09ZEouh7okFo8G6z9nS8rr7YNOP7Vl7Q4WwJEUVdIl5g07+By1Olur2LilQyYwmT8Yz4RweJoV1Eaf3iqQ/m9/AbHkxpPdjs3Yroi8NW42sG6Bv61IQ2lXM8pN+PW3Ty6joBS2qTudrW1bJqrYmnneUAhB01rFvOfAvwv6lJf7NCoTOt32FxKSbgIPyqmYwg1qeN4aWrtTnS5QwatSi0irEKOMMlBoYYs1qopZRmaOguHQ3EbZ6S25P6lrCH9zgV/ZGCXVpM8MyF51hrKf+wAsLWdQiO/6qRX+NmLJxk6My2QZmtOsUgBWoL2DFZrJ+FpvkYOXCL9xewGqpb15dRVyDUsnDj4v2svrzEi9sp6BRYnhUzH7RaKiurPRe7++AsPYSL9/u01P6bCtC88p/VP5YDzUYZ0sKnszWIxeybQQe+hMeNKcda+Vbi0WACA5ppY6/+b9VRpipYJZDJq4a6YzljtUWbjOfIko9A78XZt2HMcLFEnCbUF6B++fY4rys1Tcb8R0xc8ZhfWoFNa5ooL9I8YbSrFitl/px4OxlL4lyTUJUAFFN9mghr9SVIae6NkgYUvCS5fWXvt2nJ8RqgSxlVZTilZ6Gg8Dgcup2kQvbOTW32HsjTV3ycaTAY/JC6lbIQZNxGBpBuuFxe+1h8uMNNxNApzyX+rAaq69qHPBAZoAuorCHaqARwZSO0UV6yOLuRzsgwrKSbO0TU2eHCefNG86T40AOxqptZgTsaSX+HSrAD9IVBooeYScIyvhnV6HVDbzEprkK7P8iebYlVpQjlGqs6RtGXZZjEeJSg7ZXR1OI8M3Mlhgm9CoRpvGZ0bdBqLo1J3nxto76iKYenomt/+Qhfbk1KKYy5wzhHvuNXq86+bCmV9SyPOoSy+VirCHguv3C2upwluH/CzuB2NQfX0MzUQEmha/e96UVWRIiY/8TxwQFA3nqN4tWNk8e8B7GKga2Kz7+Tq4lFsDWEI+6C7qlpHp9lNkp2605iCCc0a3RPHGTshVqTcLU1LidtbANTAMF8hdMbcieYvyONJk39aUB3Akpif8eEs/Wa4n6hjNQTuMYpaguCKlHYAOuxsD74sBG3ehxiVpNdyqWEdOdcDDfutLzAb3As/Q7KoeFlTDXgtzFh0lRdgc2Ho+1lf7Hl/Vqvnq4b35gfeQyT3qQgduvFw6tAOCajxO9/0QakLW2ttv7dNiYUaw79V3G8DgTvIY2XOmbVtDrXxTpoUoc+a2Qh9WKemT8kgTCEtf2E3vmThyG85jWGnKpCelDJBQGPxup2acH0JpfZwrXB8GBqNgU8bbNJNSENX7r3+E4JGRTovSVeOwqA5oAG+JDTilt+rG0orzMU2vnpIPGT8Mjhpr6EFl3CjmplWhI/RwJ+NZeZvTWspO9t4LI3/iKYwqTeCrCmZ1TXC7bqIhFIzGaDUsWqwXzIZwmJvNsjL5nREMNw3WWgpv0RaU5Om4y9ZWPK2/TIMFCcfRhlK/wZXuLynix1JS6WY2BjrcoFkLWKt7l0xDn8Nps6aphY2NeYGcIhnHPoRXUWAbOQ6Z9pCb9i4VlcyRjr6Y967QdnVqAlWc1PhvGsKZBgShyRv6bxzQjbHwROlRm1ebwQX2ZWwXBAv3XrMKdKYeJO6JibDe2PXzRjQ3PoU7tE4tg0Gwclgm8nN4zEu1yngzaAlNZ3GtC1fj1aJMi3Ly1cscnnElG82nfjMJJH0J08aja4uxudKUW7mErrVsX2P6Mcr3TtFTqMGbhOesK/sV1jt+JVFtkOt3uQl8XmCOnqRKhMJCsS5I9i+ht3eXdZuo42OJLWiNBSfbBEZTzwo7z2O2HpoYMhO4dqZX5uNQCNufR6wkhSCGGVrp0bPYitK8h7KAgia/UehdEkVaZxmVCEXApplbhFw2gVMyHflSwGHVTSLCvbJwaEg4YYtFTZ3y9VNRoqq3XVeNIxW8sgJIW+tbXRwU+7CpitQjsuD2CpuwdtgNwJmqjdCWFFqSQpr/5IYtHt15VZRV5fg01QN6CoXSactdU0UOVXnaeOHL2Bd7cojwlioVz14H2saS7yKrCvZITRwjlPfCiqFQb4XccfS1urIZYm1lJlDpDVa1/bT4gimPBSdKhkWYwvzTWlIQTKh76NEiOBTGNfOalmh5aYKlwpO5brYibXWzZrUZgpbrSGBkByMrUwGGxjKYbDqMtcNUTVhsMhsezX+JrJa2kqtsrMZV3mqTVPVHNAuOWBulVVYDilVdlwrm0LLd1oeqXKs29rbhY8/SXSGrH0lHGsaEJZ9pDWmhzutCspgtepDlL2MevAkv1i1h+iesrJ17k5DbPJgGxBiR41DoyyYpeIWvcmP8+udOpVgZMulFvhX5XKkTpaNpVC4YPzeemJ4eqFioRg7INs3f5oMh/u18TnBpvpGyNanmGJzEUOLNlb+yEh6gZTqcEi60a5d64z31lHCTP28KqUm9V+/pbE5wKS427CpkyWcKDch+q5zZm/Z6wCt2inQZih4AwsmOO4rGPOSCpq1Fs0CucfUHLBjcMh1sGxnOC7EW3XJktaMX2tXfsaXHVcCa75H3im1J+9p0aAvi9K1tNGlA865bKcWtKjMzh1xLRvuQoXd3JPGya1OWq1UYmP1GqUq2vaGby+00MlFA6c1CxhJ2MUrdKDdUo7L8ckQwsEFzphfYymM6SxFQSaMlqVDfuQOiIiwoJj4yvMi44RnkpdKykpS3nGCOPE0xC6llQXIsWPAidcCla5SU5MU/ODKvMLOyZgaLhqR2Qvf6BX5UK7MuSnlN5UW0MAn/IRQXsn4R6hoAFD4q6OWkMdmz/RkSkfbqwncIPkbKXqymwDb0G3oRoCQy8zrg6fEGUMpIW5u0Cw9W2DL4xdoArqcPMx+9taGpq22N/VJXmbUqeGxS5gNZd1K1umoq3gBecN7wLs3tiRg6P6hKOOoUpswon2ADlyIwR2kL/YQbKRqsiZIHpc8gCUsZO+6J1FzFMjyrT7BCiGgUe/hAgSXemJtkKxmmBF7Kxs6dNhA2rIBz6Sp6TAdHZdKg/CshD9DlppOVgqVydOo5qxtRo5kqoAgDnQrNWic0uAJCzROtD2JWVjTAerDb3dP5srYp0W3Be2YUHS6lPGEMuGTfvaJIdDiDSjLLD90y5eQxxml8OBcfiXUTidS4yXgkZTESsS1qHjqKKuSWvLPN6sUbRBAN8pTFwxQdd8HMLLPkGIpIiC01YGNSCSi3ZdWHb31sVp68JkHKpB44EG0HxyrUbEVCEDlugKL7rBok9fLlr8oaOc3WbBOfVW4oNkmLZjWwZNOgGMaAoto+vxPk2YO2ysKq0mpQVAQdbwInY6WP8LhaLS8cVO7xoIITaLRSmZe2edfzBWWitWXRUA62E8WU7LxDXwjuY6vXZYw8msaBLtE/sMq9uqNFym4rb9y5vM7yVYLBK98hg8GwlpO/ti5eHeai+RGhYSzLbF1BpQkrmP5fuaByHT1jgNGG+2i1RqENQeD2hiiGtMjJDYvNPMFli3qxc5cnY/9aX6myEUQzaQFJNlHvgKsIDDGMWHs6NgPcNU1N20/Zob1OiFcaCNp/IE5m4nzhMeuRpDCDGChzDXs2GaqWpeocoD5D7oUzsCNULSyFZgUWgS6C4d2LVi6ndh0uOgY7jeIwIis4ToK7vBVNDtDrcKp3yLNlNPQnYZWVpKg9g807I6cvqfAB5Ajvgsapoj8KDtjHFK0gikYJDdXnoys9z4xOpkNg+iovQzjTJ8mK7GmRFCzjI7t7E4WZE3VSZfGEUaGZC0mNUJZmfbdz6jU4sMau0U9HtJGZ56xY+6rhfMrAHPvoVcDA7h9CLrpBxe+vYFxE4pCQE9422orZqV1I3aiKQOeQ1XR+RUBaazIt0CXe3KgFdBHgnHdz7SlGFklIJkRnIuo8WE5MoySz2blRm/kz0TqtLnV2PqW0ePR8WlV6w7LxYnQxnokABfvhzjMN7k12/affD+csZ4Znb3IEjGCwjjUDS+VfhqbseMmn9u2EHr1Wzz9LZzvNsDsIkKjV0zwHhmaDZsdUoriGbisUy6yhbApGbVscxaL7yCL5Uba4tlB+vtWpUMD+3IjRHyqSbSev9DKAlHORIb32eJzFHtQsQ5GBpzYrcEcIhbLtrsMpMYTOcFSJHRh6AyxTmGO23+0utViCZ43syZO7aBL2zE3nz6b7txmaHWk05h00ayqIwUBLIROzPcEe6TLErBeYqRGBN9qWh1TETy65f7J3uHBzolqVleszdYUgq3H59awziGn7ITScM0e95zYNBrkrTYQL4KhS7Uqa9Srw9pc8cujXGHw46tifWlrVFUTo32K20JHJVmQvRt27Q3YuGA4Ywd7RoAwwJ5Wq8bqwnGf/nYv+irrarWhIQrD3zrEtMQ77qhfDpDrnW6OtJr0jwVGKJaWXsas8VVbztfoDnDIF2NEi654s+DwVayEUzRmsoU3PiCy+7+yOl5u98rkkA529ASriBMbtLGTeAWb1YtVo0F6CVPWdISZGg2x/dgMXAdM0gq2AfG+izOLft15xFwetfZlA5qix5KwjzMXN9vtX/C6DBRBaDICig404De4brgGGHGAqaZ7GEuLFokLYnEDGwDB5iDMO7tjsZ6ghVu3QzuwAYjssRVJXhmC1nM29/1WTJFUId5LmYn9czwfuKzyEyW5xIlIfZzgJ3VbSwKy7qr2Y4rbMagzE/82nJQrhmc/zH7zMDeg3fodkAAAAAElFTkSuQmCC')
#         time.sleep(0.5)


        


if __name__ == '__main__':
    socketio.run(app)
    