# import base64
# import io
# import os
# from flask import Flask, jsonify, render_template, request, url_for
# from flask import send_from_directory
# from PIL import Image
# import numpy as np
# import cv2

# app = Flask(__name__)


# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.route('/play_video/<path:video>')
# def play_video(video):
#     return send_from_directory('videos', video)


# @app.route('/process_frame', methods=['POST'])
# def process_frame():
#     image_data = request.json.get('image_data')

#     image_bytes = io.BytesIO(base64.b64decode(image_data.split(',')[1]))
#     image = Image.open(image_bytes).convert('L')  # Convert to grayscale

#     matrix = np.array(image)
#     cv2.imshow(matrix)

#     grayscale_image_path = os.path.join('static', 'grayscale_image.jpg')
#     grayscale_image = Image.fromarray(matrix).convert('L')
#     grayscale_image.save(grayscale_image_path)

#     grayscale_image_url = f"/{grayscale_image_path}"
#     return jsonify({'grayscale_image': grayscale_image_url})


# if __name__ == '__main__':
#     app.run(debug=True, ssl_context='adhoc')


import cv2
from ultralytics import YOLO
from flask import Flask, render_template, Response
from curls import perform_curl
app = Flask(__name__)

# Counter variable to track frames
frame_counter = 0
# Capture video from the webcam
video_capture = cv2.VideoCapture(0)


def generate_frames_curls():

    global frame_counter
    model = YOLO('./models/yolov8s-pose.pt')
    while True:
        # Capture frame-by-frame
        success, frame = video_capture.read()

        if not success:
            break

        if frame_counter % 3 == 0:
            # Pass the frame to the process_frame function
            processed, shoulder_msg, elbow_msg = perform_curl(
                'L', frame, model)

            print(shoulder_msg)
            print(elbow_msg)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', processed)
            frame = buffer.tobytes()

            # Yield the frame as an HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:

            # Yield the frame as an HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames_curls(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
