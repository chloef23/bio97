# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 9/26/2022
# Bio97 Thesis Project
# Cell tracker -- tracks 2D cells across time

# import packages
import cv2
import os
import load_npy
import frames_to_video
import tracker

# user-specified inputs
FOLDER_NAME = ".npy test_1"     # name of the folder where .npy files are stored
VIDEO_FPS = 0.01    # frames per second desired in video, cannot be less than 0.01

# algorithm used for tracker
tracker_type = "TrackerKCF"
# tracker_type = "TrackerMOSSE"
# tracker_type = "TrackerCSRT"


# Get the folder containing .npy files of the image sequence
video_folder = FOLDER_NAME
img_list = []  # list containing all filenames of images in folder
for filename in os.scandir(video_folder):
    if filename.is_file() and os.path.splitext(filename)[1] == ".npy":
        img_list.append(filename.path)

# check to make sure all images in tiff folder are valid
png_list = []
frame_num = 0
for npy in img_list:
    png = load_npy.load(npy)
    if not png:
        print("Error: .npy " + npy + " could not be converted to a PNG. "
                                     "Please check the format and restart the program.")
        break
    png_list.append(png)
    frame_num += 1
    print(png + " loaded")

# convert list of images to mp4 video
video_file_path = FOLDER_NAME + "/cell_tracker_video.mp4"
frames_to_video.write_video(video_file_path, png_list, VIDEO_FPS)

tracker.track(video_file_path, frame_num, tracker_type)


