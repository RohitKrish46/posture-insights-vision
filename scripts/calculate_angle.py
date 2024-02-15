import math
import numpy


# def calculate_angle(v1, v0, v2):
#     x1, x2 = v1[0] - v0[0], v2[0] - v0[0]
#     y1, y2 = v1[1] - v0[1], v2[1] - v0[1]
#     dot_product = x1 * x2 + y1 * y2
#     norm_product = math.sqrt(((x1 * x1) + (y1 * y1)) * ((x2 * x2) + (y2 * y2)))

#     if (norm_product == 0):
#         return -1

#     return numpy.arccos(dot_product / norm_product)


import numpy as np


def calculate_angle(joint_a, joint_b, joint_c):
    # Convert the joint coordinates to numpy arrays
    vector_a = np.array(joint_a)
    vector_b = np.array(joint_b)
    vector_c = np.array(joint_c)

    radians = np.arctan2((vector_c[1] - vector_b[1]), (vector_c[0] - vector_b[0])) - \
        np.arctan2((vector_a[1] - vector_b[1]), (vector_a[0] - vector_b[0]))

    angle = np.abs(radians*180.0/np.pi)

    if angle > 180:
        angle = 360-angle

    return angle

    # # Calculate the vectors between the joints
    # vector_ab = vector_b - vector_a
    # vector_bc = vector_c - vector_b

    # # Calculate the dot product of the vectors
    # dot_product = np.dot(vector_ab, vector_bc)

    # # Calculate the magnitudes of the vectors
    # magnitude_ab = np.linalg.norm(vector_ab)
    # magnitude_bc = np.linalg.norm(vector_bc)

    # # Calculate the cosine of the angle using the dot product and magnitudes
    # cosine_angle = dot_product / (magnitude_ab * magnitude_bc)

    # # Calculate the angle in radians
    # angle_radians = np.arccos(cosine_angle)

    # # Convert the angle to degrees
    # angle_degrees = np.degrees(angle_radians)

    # return angle_degrees
