# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/3/2022
# Bio97 Thesis Project
# OpenCV2 video object tracker, code modified from code at https://broutonlab.com/blog/opencv-object-tracking

import cv2
import os
import math
import numpy as np

# sets automatics bounding boxes, tracks the cells contained within the bounding boxes during the video
# inputs: video_file_path - the PATH to the .mp4 video
#         frame_num - the number of frames the video has
#         tracker_type - cv2 tracker algorithm to use, "TrackerCSRT" is recommended
#         cpframe_list - the initialized CPFrame object for the first frame of the video
#         set_bounds - whether the user will be prompted to manually set the bounds of the embryo, defaults to False
# output: center_coords_list - list of lists containing the center coordinate information of each tracker for each
#         frame in the video, in form:
#        [[tracker 1 center_coord frame 0, 1, 2, ...], [tracker 2 center_coord frame 0, 1, 2...]. ...]

def track(video_file_path, frame_num, tracker_type, init_cpframe, set_bounds=False):

    # set speed of tracking video
    # to freeze at first frame, set speed to 0 (can move through frames by pressing space)
    # note: this is only relevant for videos with few trackers - speed decreases as more trackers are added
    s = 1

    # check that video exists and is in mp4 format
    if not os.path.exists(video_file_path):
        print("Video file could not be found.")
        exit()
    if os.path.splitext(video_file_path)[1] != ".mp4":
        print("Video file is not of type mp4.")
        exit()

    # read mp4 video found at inputted file path
    video = cv2.VideoCapture(video_file_path)
    ret, frame = video.read()

    # initialize video display
    frame_height, frame_width = frame.shape[:2]     # resize the video for a more convenient view
    # initialize video output
    output = cv2.VideoWriter(f'{tracker_type}.avi',     # initialize video writer to save the results
                             cv2.VideoWriter_fourcc(*'XVID'), 60.0,
                             (frame_width, frame_height), True)
    if not ret:
        print("Video cannot be read from file.")

    # allow the user to set the boundaries of the embryo or ROI, if desired
    if set_bounds:
        print("\nClick and drag to select the bounds of the embryo or desired tracking area.\n"
              "Press enter to confirm selection.")

        embryo_bounds = cv2.selectROI(frame, False)     # user manually selects ROI
        c1 = (embryo_bounds[0], embryo_bounds[1])
        c2 = (embryo_bounds[0] + embryo_bounds[2], embryo_bounds[1] + embryo_bounds[3])
        init_cpframe.set_boundaries(c1, c2)
        cv2.destroyAllWindows()     # close ROI selection window

    print("\nInitializing tracker...")
    print("Press 'ESC' at any time to exit.")

    multi_tracker = []    # list of all the trackers

    count = 0
    # select the bounding boxes in the first frame of the video
    for cell in init_cpframe.get_cell_min_max():

        # if count > 6:
        #     count += 1
        #     continue

        x1 = cell[0][0]
        y1 = cell[0][1]
        x2 = cell[1][0]
        y2 = cell[1][1]
        bbox = (x1, y1, abs(x2 - x1), abs(y2 - y1))   # (x, y, w, h)

        # uncomment below for manual selection of cells
        # bbox = cv2.selectROI(frame, False)

        temp_tracker = create_tracker(tracker_type)
        temp_tracker.init(frame, bbox)
        multi_tracker.append(temp_tracker)

        count += 1

    fps = 0

    # create list of lists containing the center coordinate information of each tracker for each frame in the video
    # [[tracker 1 center_coord frame 0, 1, 2, ...], [tracker 2 center_coord frame 0, 1, 2...]. ...]
    center_coords_list = []
    for tracker in multi_tracker:
        temp_list = []
        center_coords_list.append(temp_list)

    # start tracking frame-by-frame
    for i in range(frame_num - 1):
        ret, frame = video.read()
        if not ret:     # error with video reading
            print("Video could not be read to tracker.")
            break

        timer = cv2.getTickCount()      # for calculation of frames per second

        # multi_tracker cycles through every tracker and updates each tracker individually
        j = 0

        for tracker in multi_tracker:

            if not tracker:
                j += 1
                continue

            ret, bbox = tracker.update(frame)   # update individual cell tracker
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)     # calculate FPS

            # update displayed bounding box for next frame or remove tracker if bounding box is out of frame/ROI
            if ret:
                # calculate coordinates of bounding box
                # bbox (bounding box): (upper left x, y, lower right x, y)
                p1 = (int(bbox[0]), int(bbox[1]))                           # upper left side of bounding box
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))       # lower right side

                # TODO: remove trackers that have jumped to a different cell
                # TODO: remove trackers that have too much purple

                # check if any part of the bounding box has exited frame or user-selected ROI
                if p1[0] < 0 or p2[0] > frame_width or p1[1] < 0 or p2[1] > frame_height:
                    cv2.rectangle(frame, p1, p2, (0, 0, 150), 2, 1)     # red box
                    multi_tracker[j] = None      # remove tracker from list to be updated next frame
                    center_coords_list[j] = None    # remove coordinates

                # if user has set boundaries, check that inside boundaries
                elif set_bounds and not init_cpframe.check_boundaries(p1, p2):
                    cv2.rectangle(frame, p1, p2, (0, 0, 150), 2, 1)
                    multi_tracker[j] = None    # red box
                    center_coords_list[j] = None

                else:
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)     # blue box
                    # cv2.rectangle(frame, p1, p2, tuple(color_list[j]), 2, 1)  # multi-colored boxes

                    # update cell information in CPFrame based on new tracker location
                    # tracker_center is the integer center (rounded up) coordinate of the tracking box
                    tracker_center = (math.ceil(0.5*int(p1[0]) + 0.5*int(p2[0])), math.ceil(0.5*int(p1[1]) + 0.5*int(p2[1])))
                    center_coords_list[j].append(tracker_center)

            # if desired, display the user-selected ROI
            if set_bounds:
                cv2.rectangle(frame, embryo_bounds, (0, 150, 0), 2, 1)  # green box

            j += 1

        # print frames per second on the tracking window
        if fps < 1:
            fps_str = "< 1"
        else:
            fps_str = str(int(fps))
        cv2.putText(frame, "FPS : " + fps_str, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # show the updated frame
        cv2.imshow("Tracking", frame)
        output.write(frame)
        k = cv2.waitKey(s) & 0xff
        if k == 27:     # if 'ESC' is pressed
            break
        if k == 49:     # if 'SPACE' is pressed
            continue

    video.release()
    output.release()
    cv2.destroyAllWindows()

    return center_coords_list


# create tracker with specified algorithm
# input: tracker_type - desired tracker type, as inputted by user (CSRT is recommended and default)
# output: cv2 tracker of specified type
def create_tracker(tracker_type):
    if tracker_type == "TrackerKCF":
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == "TrackerCSRT":
        tracker = cv2.TrackerCSRT_create()
    else:   # default
        tracker = cv2.TrackerCSRT_create()

    return tracker
