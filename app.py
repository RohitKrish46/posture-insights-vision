import base64
import io
import json
import os
import cv2
from flask import Flask, jsonify, render_template, request, url_for, Response, redirect
from flask import send_from_directory
from PIL import Image
# from requests import Response
from ultralytics import YOLO
from curls import perform_curl
from planks import perform_plank
import numpy as np


app = Flask(__name__)
frame_counter = 0
global video_capture
wrist_pos = []
video_capture = None
global exercise
exercise = None
global processed_data
processed_data = None


def generate_frames():
    global exercise
    print(exercise)
    if exercise == 'bicep_curl':
        return generate_frames_curls()
    elif exercise == 'plank':
        return generate_frame_planks()
    elif exercise == 'push_ups':
        return generate_frame_push_ups()
    else:
        return redirect(url_for('index'))


def generate_frames_curls():
    global video_capture
    video_capture = cv2.VideoCapture(0)

    # Capture video from the webcam
    global processed_data
    processed_data = None

    model = YOLO('./models/yolov8s-pose.pt')
    while True:

        # Capture frame-by-frame
        success, frame = video_capture.read()

        if not success:
            break

        if frame_counter % 3 == 0:
            # Pass the frame to the process_frame function
            processed, shoulder_msg, elbow_msg, wrist = perform_curl(
                'R', frame, model)

            wrist_pos.append(wrist)

            if len(wrist_pos) < 2:
                continue
            if abs(wrist_pos[-1] - wrist_pos[-2]) > 18:
                wrist_msg = 'Moving too fast'
            else:
                wrist_msg = 'Good'

            processed_data = {
                "shoulder": shoulder_msg,
                "elbow": elbow_msg,
                'ankle': 'Good',
                'wrist': wrist_msg,
                'hip': 'Good'
            }

            # Convert the process_data dictionary to a JSON string
            # process_data_json = json.dumps(process_data)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', processed)
            frame = buffer.tobytes()

            # Yield the frame as an HTTP response with the encoded process_data
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            # Yield the frame as an HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frame_planks():
    global video_capture
    video_capture = cv2.VideoCapture(0)

    # Capture video from the webcam
    global processed_data
    processed_data = None

    model = YOLO('./models/yolov8s-pose.pt')
    while True:

        # Capture frame-by-frame
        success, frame = video_capture.read()

        if not success:
            break

        if frame_counter % 3 == 0:
            # Pass the frame to the process_frame function
            processed, Hip_msg, elbow_msg, shoulder_msg = perform_plank(
                frame, model)

            processed_data = {
                "shoulder": shoulder_msg,
                "wrist": 'Good',
                'elbow': elbow_msg,
                'ankle': 'Good',
                'hip': Hip_msg
            }

            # Convert the process_data dictionary to a JSON string
            # process_data_json = json.dumps(process_data)

            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', processed)
            frame = buffer.tobytes()

            # Yield the frame as an HTTP response with the encoded process_data
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            # Yield the frame as an HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frame_push_ups():
    global video_capture
    video_capture = cv2.VideoCapture(0)

    # Capture video from the webcam
    global processed_data
    processed_data = None

    model = YOLO('./models/yolov8s-pose.pt')
    while True:

        # Capture frame-by-frame
        success, frame = video_capture.read()

        if not success:
            break

        if frame_counter % 3 == 0:
            # Pass the frame to the process_frame function
            processed, Hip_msg, elbow_msg, shoulder_msg = perform_plank(
                frame, model)
            processed_data = {
                "shoulder": shoulder_msg,
                "wrist": 'Good',
                'elbow': elbow_msg,
                'ankle': 'Good',
                'hip': Hip_msg
            }
            # Encode the frame in JPEG format
            ret, buffer = cv2.imencode('.jpg', processed)
            frame = buffer.tobytes()

            # Yield the frame as an HTTP response with the encoded process_data
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            # Yield the frame as an HTTP response
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/process_data')
def process_data():
    global processed_data
    if processed_data is not None:
        return jsonify(processed_data)
    else:
        return jsonify({
            "status": "Done"})


@app.route('/clear_all')
def clear_all_func():
    global process_data
    process_data = None
    global video_capture
    global exercise
    exercise = None
    if video_capture is not None:
        video_capture.release()
    return redirect(url_for('index'))


@app.route('/', endpoint='index')
def home():
    return render_template('index.html')


@app.route('/tnc/<path:video>')
def check_tnc(video):
    global exercise
    print('video --- ', video)
    exercise = video.split('.')[0].lower()
    return render_template('tnc.html', video=video)


@app.route('/play_video/<path:video>')
def play_video(video):
    print(video)
    return send_from_directory('videos', video)


@app.route('/process_frame', methods=['POST', 'GET'])
def process_frame():
   # Process the received image data
    image_data = request.json['image_data']

    # Convert the base64 encoded image data to PIL Image object
    image_bytes = io.BytesIO(base64.b64decode(image_data.split(',')[1]))
    image = Image.open(image_bytes)

    # Get the image dimensions
    image_dimensions = {
        'width': image.width,
        'height': image.height
    }

    image_bytes = io.BytesIO(base64.b64decode(image_data.split(',')[1]))
    image = Image.open(image_bytes).convert('L')  # Convert to grayscale

    matrix = np.array(image)

    grayscale_image_path = os.path.join('static', 'grayscale_image.jpg')
    grayscale_image = Image.fromarray(matrix).convert('L')
    grayscale_image.save(grayscale_image_path)

    grayscale_image_url = f"/{grayscale_image_path}"
    # Return the response JSON with image dimensions
    response_data = {
        'image_dimensions': image_dimensions
    }
    return jsonify(response_data)


@app.route('/feed/<path:video>')
def feed(video):
    if video.split('.')[0].lower() == 'bicep_curl':
        fields = ["Shoulder", "Elbow", "wrist", "Hip", 'Ankle']
    elif video.split('.')[0].lower() == 'push_ups':
        fields = ["Hip", "Ankle", "Elbow", "Shoulder", "Wrist"]
    elif video.split('.')[0].lower() == 'plank':
        fields = ["Hip", "Ankle", "Elbow", "Shoulder", "Wrist"]

    return render_template('feed.html', video_name=video, data_fields=fields)


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
