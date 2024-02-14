from calculate_angle import calculate_angle
import cv2
import time


def angle_one(idx, keypoint_result):
    return (keypoint_result[idx][0], keypoint_result[idx][1])


def average_or_one(idx1, idx2, keypoint_result):
    return ((keypoint_result[idx1][0] + keypoint_result[idx2][0])/2, (keypoint_result[idx1][1] + keypoint_result[idx2][1])/2)


def plank(keypoint_result):

    def deviation_in_waist(keypoint_result):
        shoulder = average_or_one(5, 6, keypoint_result)
        hip = average_or_one(11, 12, keypoint_result)
        ankle = average_or_one(15, 16, keypoint_result)
        wrist = average_or_one(9, 10, keypoint_result)
        elbow = average_or_one(7, 8, keypoint_result)
        try:
            if shoulder and hip and ankle:
                # calculate angle
                hip_angle = calculate_angle(shoulder, hip, ankle)
                elbow_angle = calculate_angle(wrist, elbow, shoulder)
                shoulder_angle = calculate_angle(elbow, shoulder, hip)
                # elbow_angle = calculate_angle(wrist, elbow, shoulder)
            else:
                return -1
        except TypeError as e:
            raise e

        # calculate percent deviation
        # deviation = (optimal_angle - angle_detected)/optimal_angle * 100
        return hip_angle, hip[1], shoulder[1], elbow_angle, shoulder_angle

    return deviation_in_waist(keypoint_result)


def perform_plank(frame, model):

    results = model(frame, verbose=False)

    try:
        # Analyze workout
        hip_angle, hip_y, shoulder_y, elbow_angle, shoulder_angle = plank(
            results[0].keypoints.xy[0])

    except IndexError as e:
        cv2.imshow('pose-estimation result', frame)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            return

    draw = results[0].plot(boxes=False, probs=False,
                           conf=False, workout='plank')

    shoulder_msg = 'Good'
    elbow_msg = 'Good'
    if hip_angle >= 165 and hip_angle < 180:
        hip_msg = 'Good'

    if elbow_angle >= 110 and elbow_angle < 70:
        elbow_msg = 'Adjust Shoulder Position'

    if shoulder_angle >= 110 and shoulder_angle < 70:
        shoulder_msg = 'Adjust Shoulder Position'

    elif hip_angle < 165:
        if (hip_y > shoulder_y):
            hip_msg = "Low lower back position"
        else:
            hip_msg = "High lower back position"
    else:
        hip_msg = 'Good'

    if hip_msg != 'Good' or shoulder_msg != 'Good' or elbow_msg != 'Good':
        return draw, hip_msg, elbow_msg, shoulder_msg
    else:
        return frame, hip_msg, elbow_msg, shoulder_msg
