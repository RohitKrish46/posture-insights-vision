from calculate_angle import calculate_angle
from ultralytics import YOLO
import cv2
import time
# analyzing bicep curls


def angle_one(idx, keypoint_result):
    return (keypoint_result[idx][0], keypoint_result[idx][1])


def analyze_workout(side, workout_func, keypoint_result):
    if side:
        return workout_func(side, keypoint_result)
    else:
        return workout_func(keypoint_result)


def curl(side, keypoint_result):
    """
    side - left or right, depending on user

    Problems:
    ->  Horizontal deviation in humerous to upper body:
        Body parts:
            L//R Shoulder
            L//R Elbow
            L//R Hip
        Percent Deviation:
            (OptimalAngle - AngleDetected)/OptimalAngle * 100
        Params:
            OptimalAngle = 0
            Threshold = 0.1
    """

    def horizontal_deviation_of_elbow(side, keypoint_result):
        try:
            if side == 'L':
                shoulder = angle_one(5, keypoint_result)
                elbow = angle_one(7, keypoint_result)
                hip = angle_one(11, keypoint_result)
                wrist = angle_one(9, keypoint_result)
            elif side == 'R':
                shoulder = angle_one(6, keypoint_result)
                elbow = angle_one(8, keypoint_result)
                hip = angle_one(12, keypoint_result)
                wrist = angle_one(10, keypoint_result)
            else:
                return -1
        except KeyError as e:
            return -1

        try:
            if shoulder and hip and elbow and wrist:
                # calculate angle
                shoulder_angle = calculate_angle(elbow, shoulder, hip)
                elbow_angle = calculate_angle(wrist, elbow, shoulder)
            else:
                return -1
        except TypeError as e:
            raise e

        # calculate percent deviation
        # deviation = (optimal_angle - angle_detected)/optimal_angle * 100
        return shoulder_angle, elbow_angle, elbow[1], wrist[1]

    return horizontal_deviation_of_elbow(side, keypoint_result)


# HARDCODE
current_workout = curl

# Initialize fps counter
fps_time = 0

# Define the interval for processing frames (e.g., process every 10th frame)
frame_interval = 3
frame_counter = 0

# Load model
model = YOLO('./models/yolov8s-pose.pt')

# Initialize camera capture
cam = cv2.VideoCapture('./videos/curls2.mp4')
ret_val, image = cam.read()

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('./results/output.mp4', fourcc, 20.0, (270, 480))

# w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

rows, cols = image.shape[0], image.shape[1]
temp = []
# Read loop
while True:
    # Read from camera
    ret_val, image = cam.read()

    if not ret_val:
        break

    frame_counter += 1
    if frame_counter % frame_interval == 0:
        results = model(image, verbose=False)
    else:
        continue

    try:
        # Analyze workout
        shoulder, elbow, el_y, wr_y = analyze_workout('L', current_workout,
                                                      results[0].keypoints.xy[0])
    except IndexError as e:
        cv2.imshow('pose-estimation result', image)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        continue

    # Draw pose
    draw = results[0].plot(boxes=False, probs=False,
                           conf=False, workout='curl')

    if shoulder > 17.0:
        cv2.putText(draw, "Loose Upper Arm",
                    (10, 70),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 0, 255), 2)
        # Draw angle
        cv2.putText(draw,
                    "Shoulder Angle: {}".format(round(shoulder, 2)),
                    (10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        cv2.putText(draw,
                    "Elbow Ang: {}".format(round(elbow, 2)),
                    (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        # Draw fps
        fps = 1.0 / (time.time() - fps_time)
        cv2.putText(draw,
                    "FPS: {}".format(round(fps, 2)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('pose-estimation result', draw)
        # out.write(draw)

    if wr_y < el_y and elbow > 80:
        cv2.putText(draw, "Weak peak contraction",
                    (10, 70),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 255), 2)

        # Draw angle
        cv2.putText(draw,
                    "Shoulder Angle: {}".format(round(shoulder, 2)),
                    (10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        cv2.putText(draw,
                    "Elbow Ang: {}".format(round(elbow, 2)),
                    (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        # Draw fps
        fps = 1.0 / (time.time() - fps_time)
        cv2.putText(draw,
                    "FPS: {}".format(round(fps, 2)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('pose-estimation result', draw)
        # out.write(draw)

    else:
        # Draw angle
        cv2.putText(image,
                    "Shoulder Angle: {}".format(round(shoulder, 2)),
                    (10, 50),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.putText(image,
                    "Elbow Ang: {}".format(round(elbow, 2)),
                    (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        # Draw fps
        fps = 1.0 / (time.time() - fps_time)
        cv2.putText(image,
                    "FPS: {}".format(round(fps, 2)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('pose-estimation result', image)
        # out.write(image)

    # Show image
    # out.write(draw)

    # Restart FPS counter
    fps_time = time.time()
#     time.sleep(1)
    if cv2.waitKey(1) == 27:
        break

# out.release()
cam.release()
cv2.destroyAllWindows()
