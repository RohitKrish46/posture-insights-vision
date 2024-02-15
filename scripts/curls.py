from calculate_angle import calculate_angle
import cv2
import time

# function to find key point values given index


def angle_one(idx, keypoint_result):
    return (keypoint_result[idx][0], keypoint_result[idx][1])


def curlR(keypoint_result):

    def horizontal_deviation_of_elbow(keypoint_result):

        shoulder = angle_one(6, keypoint_result)
        elbow = angle_one(8, keypoint_result)
        hip = angle_one(12, keypoint_result)
        wrist = angle_one(10, keypoint_result)
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

    return horizontal_deviation_of_elbow(keypoint_result)


def curlL(keypoint_result):

    def horizontal_deviation_of_elbow(keypoint_result):

        shoulder = angle_one(5, keypoint_result)
        elbow = angle_one(7, keypoint_result)
        hip = angle_one(11, keypoint_result)
        wrist = angle_one(9, keypoint_result)

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
        return shoulder_angle, elbow_angle, elbow[1], wrist[1]

    return horizontal_deviation_of_elbow(keypoint_result)


def perform_curl(side, frame, model):

    results = model(frame, verbose=False)
    if side == 'L':
        try:
            # Analyze workout
            shoulder, elbow, el_y, wr_y = curlL(results[0].keypoints.xy[0])

        except IndexError as e:
            cv2.imshow('pose-estimation result', frame)
            fps_time = time.time()
            if cv2.waitKey(1) == 27:
                return
    else:
        try:
            # Analyze workout
            shoulder, elbow, el_y, wr_y = curlR(results[0].keypoints.xy[0])

        except IndexError as e:
            cv2.imshow('pose-estimation result', frame)
            fps_time = time.time()
            if cv2.waitKey(1) == 27:
                return

    # Draw pose
    draw = results[0].plot(boxes=False, probs=False,
                           conf=False, workout='curl')

    if shoulder > 18.0:
        shoulder_issue = 'Correct your posture'

    else:
        shoulder_issue = 'Good'

    if wr_y < el_y and elbow > 80:
        elbow_issue = 'Correct your posture'

    else:
        elbow_issue = 'Good'

    if wr_y < el_y and elbow > 100:
        elbow_issue = 'Good'

    else:
        elbow_issue = 'Correct your posture'

    if elbow_issue != 'Good' or shoulder_issue != 'Good':
        return draw, shoulder_issue, elbow_issue, wr_y
    else:
        return frame, shoulder_issue, elbow_issue, wr_y
