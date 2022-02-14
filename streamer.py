from flask import Flask, Response, make_response
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)


def generate_frames():
    while True:
        ## read the camera frame
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    camera.release()


@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



app.run(host="0.0.0.0", port=8080)
