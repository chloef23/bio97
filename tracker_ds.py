# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 2/4/2023
# Bio97 Thesis Project
# Data structure to hold the information for each tracker

import math
import numpy as np


class TrackerDs:

    # input: tracker - an initialized cv2 tracker
    # color - the random RGB color tuple associated with the tracker, for visualizing on the tracking video
    # coords - list of center coordinates of the tracker at each frame
    # out_frame - boolean, initializes as False and sets to True if a tracker exits the frame
    def __init__(self, tracker):
        self.tracker = tracker
        self.coords = []
        self.removed_bool = False

        # set color
        temp_color = tuple(np.random.choice(range(256), size=3))
        self.color = (int(temp_color[0]), int(temp_color[1]), int(temp_color[2]))

    # checks if the tracker has moved too far from the previous frame using the Euclidean distance formula
    # inputs: jump_limit - how far the tracker is allowed to move between frames
    #         center_coord - the current center coord of the tracker, before it's been added to the self.coords list
    # output - boolean: True if tracker has moved more than the jump limit, false if not
    def check_jump(self, jump_limit, center_coord):
        x2 = center_coord[0]
        y2 = center_coord[1]
        x1 = self.coords[-1][0]     # last item in list, x coord
        y1 = self.coords[-1][1]     # last item in list, y coord

        distance = math.sqrt(math.pow(x2 - x1, 2) + pow(y2 - y1, 2))

        if distance > jump_limit:
            return True
        else:
            return False

    # allows the user to add a center coordinate to the self.coords list
    # input: coordinate, tuple or list
    def add_coord(self, coord):
        self.coords.append(coord)

    # removes the last coord from the self.coords list
    def remove_last_coord(self):
        self.coords.pop()

    # returns the list of coordinates contained in self.coords
    def get_coords(self):
        return self.coords

    # allows the user to access the tracker's color
    # output - self.color, a tuple of a random RGB color
    def get_color(self):
        return self.color

    # returns True if the tracker has been removed (out_frame = True), false if not
    def removed(self):
        if self.removed_bool:
            return True
        else:
            return False

    # allows the user to set self.removed, sets self.coords equal to None
    # input: bool - True or False
    def set_removed(self, bool):
        self.removed_bool = bool
        self.coords = None
