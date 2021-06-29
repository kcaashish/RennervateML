import numpy as np


def midpoint(p1, p2):
    "for calculating the midpoint between two points"
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def euclidean_distance(leftx, lefty, rightx, righty):
    "for calculating the distance between two points"
    return np.sqrt((leftx - rightx) ** 2 + (lefty - righty) ** 2)


def eye_aspect_ratio(eye_point, facial_landmark):
    "for calculating the eye aspect ratio"
    left_point = [
        facial_landmark.part(eye_point[0]).x,
        facial_landmark.part(eye_point[0]).y,
    ]
    right_point = [
        facial_landmark.part(eye_point[3]).x,
        facial_landmark.part(eye_point[3]).y,
    ]

    top_point = midpoint(
        facial_landmark.part(eye_point[1]), facial_landmark.part(eye_point[2])
    )
    bottom_point = midpoint(
        facial_landmark.part(eye_point[4]), facial_landmark.part(eye_point[5])
    )

    horizontal_dist = euclidean_distance(
        left_point[0], left_point[1], right_point[0], right_point[1]
    )
    vertical_dist = euclidean_distance(
        top_point[0], top_point[1], bottom_point[0], bottom_point[1]
    )

    EAR = vertical_dist / horizontal_dist
    return EAR


def mouth_aspect_ratio(mouth_point, landmark):
    "for calculating mouth aspect ratio"
    # calculating distance of the horizontal line
    left_horizontal = [landmark.part(mouth_point[0]).x, landmark.part(mouth_point[0]).y]
    right_horizontal = [
        landmark.part(mouth_point[6]).x,
        landmark.part(mouth_point[6]).y,
    ]
    horizontal_dist = euclidean_distance(
        left_horizontal[0], left_horizontal[1], right_horizontal[0], right_horizontal[1]
    )

    # calculating distance of left vertical line
    top_left_vertical = [
        landmark.part(mouth_point[2]).x,
        landmark.part(mouth_point[2]).y,
    ]
    bot_left_vertical = [
        landmark.part(mouth_point[10]).x,
        landmark.part(mouth_point[10]).y,
    ]
    left_vertcal_dist = euclidean_distance(
        top_left_vertical[0],
        top_left_vertical[1],
        bot_left_vertical[0],
        bot_left_vertical[1],
    )

    # calculating distance of mid vertical line
    top_mid_vertical = [
        landmark.part(mouth_point[3]).x,
        landmark.part(mouth_point[3]).y,
    ]
    bot_mid_vertical = [
        landmark.part(mouth_point[9]).x,
        landmark.part(mouth_point[9]).y,
    ]
    mid_vertical_dist = euclidean_distance(
        top_mid_vertical[0],
        top_mid_vertical[1],
        bot_mid_vertical[0],
        bot_mid_vertical[1],
    )

    # calculating distance of right vertical line
    top_right_vertical = [
        landmark.part(mouth_point[4]).x,
        landmark.part(mouth_point[4]).y,
    ]
    bot_right_vertical = [
        landmark.part(mouth_point[8]).x,
        landmark.part(mouth_point[8]).y,
    ]
    right_vertical_dist = euclidean_distance(
        top_right_vertical[0],
        top_right_vertical[1],
        bot_right_vertical[0],
        bot_right_vertical[1],
    )

    MAR = (left_vertcal_dist + mid_vertical_dist + right_vertical_dist) / (
        3 * horizontal_dist
    )
    return MAR
