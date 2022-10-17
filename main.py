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
import pandas as pd

# user-specified inputs
FOLDER_NAME = "long_test"     # name of the folder where .npy files are stored
VIDEO_FPS = 1    # frames per second desired in video, cannot be less than 0.01

# algorithm used for tracker
tracker_type = "TrackerCSRT"    # recommended algorithm
# tracker_type = "TrackerKCF"
# tracker_type = "TrackerMOSSE"


def main():
    # Get the folder containing .npy files of the image sequence
    video_folder = FOLDER_NAME
    img_list = []  # list containing all filenames of images in folder
    for filename in os.scandir(video_folder):
        if filename.is_file() and os.path.splitext(filename)[1] == ".npy":
            img_list.append(filename.path)

    # convert all .npy in folder to pngs
    png_list = []
    cpframe_list = []
    frame_num = 0
    for npy in img_list:

        # check to see if the png already exists, if so, don't create again
        png_name = npy + ".png"
        if os.path.exists(png_name):
            png, cpframe = load_npy.load(npy, png_generated=True)
            print(png + " found")

        # create png from .npy
        else:
            png, cpframe = load_npy.load(npy)
            if not png:
                print("Error:" + npy + " could not be converted to a PNG. "
                                         "Please check the format and restart the program.")
                break
            print(png + " loaded")

        png_list.append(png)
        cpframe_list.append(cpframe)
        frame_num += 1

    # convert list of images to mp4 video
    video_file_path = FOLDER_NAME + "/cell_tracker_video.mp4"
    frames_to_video.write_video(video_file_path, png_list, VIDEO_FPS)

    print(cpframe_list[0])
    tracker.track(video_file_path, frame_num, tracker_type, cpframe_list[0])


if __name__ == "__main__":
    main()

