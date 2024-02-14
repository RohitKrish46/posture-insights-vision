from ultralytics import YOLO
import cv2
keypoint_mapping = {
    "nose": 0,
    "left_eye": 1,
    "right_eye": 2,
    "left_ear": 3,
    "right_ear": 4,
    "left_shoulder": 5,
    "right_shoulder": 6,
    "left_elbow": 7,
    "right_elbow": 8,
    "left_wrist": 9,
    "right_wrist": 10,
    "left_hip": 11,
    "right_hip": 12,
    "left_knee": 13,
    "right_knee": 14,
    "left_ankle": 15,
    "right_ankle": 16
}

# Load a model
model = YOLO('yolov8l-pose.pt')  # load an official model
# model = YOLO('path/to/best.pt')  # load a custom model

# Predict with the model
results = model('curl_1.png', stream=False)  # predict on an image

keypoint_result = results[0].keypoints.xy[0]
nose_x, nose_y = keypoint_result[keypoint_mapping['nose']]
print(nose_x)
print(nose_y)
res_plotted = results[0].plot(boxes=False, probs=False, conf=False)
cv2.imshow("result", res_plotted)
cv2.waitKey(10000)
cv2.destroyAllWindows()
