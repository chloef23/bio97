# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 11/2/2022
# Bio97 Thesis Project
# CPTracker -- 4D cell tracking program that interfaces with the .npy outputs from Cellpose

import os

#######################################################################################################################
#######################################################################################################################

# user-specified inputs
FOLDER_NAME = "t_test_short"     # name of the folder where .npy files are stored
VIDEO_FPS = 5    # frames per second desired in mp4 video, cannot be less than 0.01
                 # note: this does not affect the speed of the tracker - that is solely determined by the number of
                 #       items to track

ZVALUE = 15     # the user-selected z-stack value to split each z (t-constant) video at

# algorithm used for tracker
TRACKER_TYPE = "TrackerCSRT"    # recommended algorithm
# tracker_type = "TrackerKCF"

#######################################################################################################################
#######################################################################################################################

# cycles through the .npys in the folder and splits them into a single t video (at z = ZVALUE) and two z videos
# for every timepoint (from ZVALUE to 0 and ZVALUE to the bottom), then, initializes an empty FrameConnector and
# runs the tracker on every video
# inputs: user-specified inputs at top of file
# outputs: the FrameConnector containing the coordinates contained within each cell at each timepoint
def main():

    # cycle through the folders and extract the txxzxx name
    for file in os.scandir(FOLDER_NAME):
        print(file)


# run the CPTracker
if __name__ == "__main__":
    main()