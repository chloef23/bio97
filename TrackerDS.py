# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 2/4/2023
# Bio97 Thesis Project
# Data structure to hold the information for each tracker

import math
import numpy as np


class TrackerDS:

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
    # output: boolean - True if tracker has moved more than the jump limit, false if not
    def check_jump(self, jump_limit):

        if len(self.coords) < 2:
            return False

        x2 = self.coords[-2][0]     # second-to-last item in list (last coordinate)
        y2 = self.coords[-2][1]
        x1 = self.coords[-1][0]     # last item in list (cuurent coordiante)
        y1 = self.coords[-1][1]

        distance = math.sqrt(math.pow(x2 - x1, 2) + pow(y2 - y1, 2))
        # print(distance)

        if distance > jump_limit:
            return True
        else:
            return False

    # allows the user to add a center coordinate to the self.coords list
    # input: coordinate, tuple or list
    def add_coord(self, coord):
        self.coords.append(coord)
        print(self.coords)

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
    #        keep - defaults to False, deletes the data in self.coords unless set to True
    #               if set to True, deletes the last coordinate in self.coords
    def set_removed(self, bool, keep=False):
        self.removed_bool = bool
        if not keep:
            self.coords = None
        else:
            self.coords.pop()
            self.coords.append(None)

