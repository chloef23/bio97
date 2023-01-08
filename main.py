# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 11/2/2022
# Bio97 Thesis Project
# CPTracker -- 4D cell tracking program that interfaces with the .npy outputs from Cellpose

# user-specified inputs
FOLDER_NAME = "z_tracking_test"     # name of the folder where .npy files are stored
VIDEO_FPS = 1    # frames per second desired in mp4 video, cannot be less than 0.01
                 # note: this does not affect the speed of the tracker - that is solely determined by the number of
                 # items to track
TVALUE = 19

# algorithm used for tracker
tracker_type = "TrackerCSRT"    # recommended algorithm
# tracker_type = "TrackerKCF"

