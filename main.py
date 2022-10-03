# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 9/26/2022
# Bio97 Thesis Project
# Cell tracker -- tracks 2D cells across time
# code modified from code at https://broutonlab.com/blog/opencv-object-tracking

import numpy as np
import cv2
import os
import load_npy
import frames_to_video

# folder
FOLDER_NAME = ".npy test_1"
VIDEO_FPS = 1

tracker = cv2.TrackerKCF_create()
# tracker = cv2.legacy.TrackerMOSSE_create()
# tracker = cv2.TrackerCSRT_create()

# Get the folder containing .npy files of the image sequence
video_folder = FOLDER_NAME
img_list = []  # list containing all filenames of images in folder
for filename in os.scandir(video_folder):
    if filename.is_file() and os.path.splitext(filename)[1] == ".npy":
        img_list.append(filename.path)

# check to make sure all images in tiff folder are valid
png_list = []
for npy in img_list:
    png = load_npy.load(npy)
    if not png:
        print("Error: .npy " + npy + " could not be converted to a PNG. "
                                     "Please check the format and restart the program.")
        break
    png_list.append(png)
    print(png + " loaded")

# convert list of images to mp4 video
video_file_path = FOLDER_NAME + "/cell_tracker_video.mp4"
frames_to_video.write_video(video_file_path, png_list, VIDEO_FPS)

# # tracking
# video = cv2.VideoCapture("walking.mp4")
# ret, frame = video.read()
#
# frame_height, frame_width = frame.shape[:2]
# # Resize the video for a more convinient view
# frame = cv2.resize(frame, [frame_width // 2, frame_height // 2])
# # Initialize video writer to save the results
# output = cv2.VideoWriter(f'{tracker_type}.avi',
#                          cv2.VideoWriter_fourcc(*'XVID'), 60.0,
#                          (frame_width // 2, frame_height // 2), True)
# if not ret:
#     print('cannot read the video')
#
# # Select the bounding box in the first frame
# bbox = cv2.selectROI(frame, False)
# ret = tracker.init(frame, bbox)
#
# # Start tracking
# while True:
#     ret, frame = video.read()
#     frame = cv2.resize(frame, [frame_width // 2, frame_height // 2])
#     if not ret:
#         print('something went wrong')
#         break
#     timer = cv2.getTickCount()
#     ret, bbox = tracker.update(frame)
#     fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
#     if ret:
#         p1 = (int(bbox[0]), int(bbox[1]))
#         p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#         cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
#     else:
#         cv2.putText(frame, "Tracking failure detected", (100, 80),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
#     cv2.putText(frame, tracker_type + " Tracker", (100, 20),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
#     cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
#     cv2.imshow("Tracking", frame)
#     output.write(frame)
#     k = cv2.waitKey(1) & 0xff
#     if k == 27: break
#
# video.release()
# output.release()
# cv2.destroyAllWindows()


