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


def average_or_one(idx1, idx2, keypoint_result):
    return ((keypoint_result[idx1][0] + keypoint_result[idx2][0])/2, (keypoint_result[idx1][1] + keypoint_result[idx2][1])/2)


def plank(keypoint_result):
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

    def deviation_in_waist(keypoint_result):
        shoulder = average_or_one(5, 6, keypoint_result)
        hip = average_or_one(11, 12, keypoint_result)
        ankle = average_or_one(15, 16, keypoint_result)

        try:
            if shoulder and hip and ankle:
                # calculate angle
                hip_angle = calculate_angle(shoulder, hip, ankle)
                # elbow_angle = calculate_angle(wrist, elbow, shoulder)
            else:
                return -1
        except TypeError as e:
            raise e

        # calculate percent deviation
        # deviation = (optimal_angle - angle_detected)/optimal_angle * 100
        return hip_angle, hip[1], shoulder[1]

    return deviation_in_waist(keypoint_result)


# HARDCODE
current_workout = plank

# Initialize fps counter
fps_time = 0

# Define the interval for processing frames (e.g., process every 10th frame)
frame_interval = 3
frame_counter = 0

# Load model
model = YOLO('./models/yolov8s-pose.pt')

# Initialize camera capture
cam = cv2.VideoCapture('./videos/Plank_error.mp4')
ret_val, image = cam.read()

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('./results/plank_outout.mp4', fourcc, 20.0, (852, 480))

# w = cam.get(cv2.CAP_PROP_FRAME_WIDTH)
# h = cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

# print(w)
# print(h)
rows, cols = image.shape[0], image.shape[1]
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
        hip_angle, hip_y, shoulder_y = analyze_workout(None, current_workout,
                                                       results[0].keypoints.xy[0])
    except IndexError as e:
        cv2.imshow('pose-estimation result', image)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break
        continue
    # Draw pose
    draw = results[0].plot(boxes=False, probs=False,
                           conf=False, workout='plank')

    if hip_angle >= 165 and hip_angle < 180:

        cv2.putText(image, "correct posture",
                    (10, 60),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 255), 2)
        # Draw angle
        cv2.putText(image,
                    "Hip Angle: {}".format(round(hip_angle, 2)),
                    (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        # Draw fps
        fps = 1.0 / (time.time() - fps_time)
        cv2.putText(image,
                    "FPS: {}".format(round(fps, 2)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('pose-estimation result', image)
        out.write(image)
    elif hip_angle < 165:
        if (hip_y > shoulder_y):
            cv2.putText(draw, "Low lower back position",
                        (10, 60),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            # Draw angle
            cv2.putText(draw,
                        "Hip Angle: {}".format(round(hip_angle, 2)),
                        (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

            # Draw fps
            fps = 1.0 / (time.time() - fps_time)
            cv2.putText(draw,
                        "FPS: {}".format(round(fps, 2)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            cv2.imshow('pose-estimation result', draw)
            out.write(draw)
        else:
            cv2.putText(draw, "High lower back position",
                        (10, 60),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            # Draw angle
            cv2.putText(draw,
                        "Hip Angle: {}".format(round(hip_angle, 2)),
                        (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

            # Draw fps
            fps = 1.0 / (time.time() - fps_time)
            cv2.putText(draw,
                        "FPS: {}".format(round(fps, 2)),
                        (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            cv2.imshow('pose-estimation result', draw)
            out.write(draw)

    else:
        # Draw angle
        cv2.putText(image,
                    "Hip Angle: {}".format(round(hip_angle, 2)),
                    (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        # Draw fps
        fps = 1.0 / (time.time() - fps_time)
        cv2.putText(image,
                    "FPS: {}".format(round(fps, 2)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('pose-estimation result', image)
        out.write(image)

    # Restart FPS counter
    fps_time = time.time()
#     time.sleep(1)
    if cv2.waitKey(1) == 27:
        break

# out.release()
cam.release()
cv2.destroyAllWindows()
