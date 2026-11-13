# import math
# from gesture_recognition import is_thumb_folded
# from gesture_recognition import is_finger_closed_over_thumb

# def get_distance(p1, p2):
#     return math.dist(p1, p2)


# def get_thumb_fold_ratio(points):

#     if len(points) != 21:
#         return None
    
#     def is_thumb_folded(points, threshold=0.8):
#         ratio=get_thumb_fold_ratio(points)
#         if ratio is None:
#             return False
#         return ratio< threshold
    
#     def is_fingers_closed_over_thumb(points, threshold=0.45):
        
#         if len(points) != 21:
#             return False
#         palm_width=get_distance(points[5], points[17])
#         if palm_width<1:
#             return False
#         thumb_tip=points[4]
#         finger_tips=[points[8], points[12], points[16], points[20]]
#         close_count=0
#         for tip in finger_tips:
#             distance=get_distance(tip, thumb_tip)
#             ratio=distance/palm_width
#             if ratio<threshold:
#                 close_count+=1
#         return close_count>=3

#     palm_ids = [0, 5, 9, 13, 17]

#     palm_x = sum(points[i][0] for i in palm_ids) / 5
#     palm_y = sum(points[i][1] for i in palm_ids) / 5

#     palm_center = (palm_x, palm_y)

#     palm_width = get_distance(points[5], points[17])

#     if palm_width < 1:
#         return None

#     thumb_distance = get_distance(points[4], palm_center)

#     return thumb_distance / palm_width





##new code 


import math
import time


def get_distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
    )


def get_palm_width(points):
    return get_distance(points[5], points[17])


def is_open_palm(points):
    if len(points) != 21:
        return False

    fingers = [(8, 6), (12, 10), (16, 14), (20, 18)]

    count = 0

    for tip, pip in fingers:
        if points[tip][1] < points[pip][1]:
            count += 1

    return count >= 3


def is_thumb_folded(points, threshold=0.65):
    if len(points) != 21:
        return False

    palm_width = get_palm_width(points)

    if palm_width < 1:
        return False

    ratio = get_distance(points[4], points[5]) / palm_width

    return ratio < threshold


def is_fingers_closed_over_thumb(points, threshold=0.75):
    if len(points) != 21:
        return False

    palm_width = get_palm_width(points)

    if palm_width < 1:
        return False

    palm_center = (
        sum(points[i][0] for i in [0, 5, 9, 13, 17]) / 5,
        sum(points[i][1] for i in [0, 5, 9, 13, 17]) / 5
    )

    count = 0

    for tip in [8, 12, 16, 20]:
        ratio = get_distance(points[tip], palm_center) / palm_width

        if ratio < threshold:
            count += 1

    return count >= 3


class GestureSequenceDetector:

    def __init__(self):
        self.stage = 0
        self.start_time = None
        self.last_alert_time = 0

    def update(self, points):

        now = time.time()

        if self.start_time and now - self.start_time > 5:
            self.stage = 0
            self.start_time = None

        open_palm = is_open_palm(points)
        thumb_folded = is_thumb_folded(points)
        fingers_closed = is_fingers_closed_over_thumb(points)

        if open_palm:
            self.stage = 1
            self.start_time = now

        elif self.stage == 1 and thumb_folded:
            self.stage = 2

        elif self.stage == 2 and fingers_closed:
            if now - self.last_alert_time > 5:
                self.last_alert_time = now
                self.stage = 0
                self.start_time = None
                return True

        return False
