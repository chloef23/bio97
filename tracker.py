# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/3/2022
# Bio97 Thesis Project
# OpenCV2 video object tracker, code modified from code at https://broutonlab.com/blog/opencv-object-tracking

import cv2
import os
import math

# sets automatics bounding boxes, tracks the cells contained within the bounding boxes during the video
# inputs: video_file_path - the PATH to the .mp4 video
#         frame_num - the number of frames the video has
#         tracker_type - cv2 tracker algorithm to use, "TrackerCSRT" is recommended
#         cpframe_list - the list of initialized CPFrame objects for each frame of the video
#         set_bounds - whether the user will be prompted to manually set the bounds of the embryo, defaults to False
# output: none

def track(video_file_path, frame_num, tracker_type, cpframe_list, set_bounds=False):

    # set speed out output video
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

    # set first CPFrame object as the CPFrame from the first .npy frame of the video
    init_cpframe = cpframe_list[0]

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

    # select the bounding boxes in the first frame of the video
    for cell in init_cpframe.get_cell_min_max():
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

    # start tracking frame-by-frame
    for i in range(0, frame_num - 1):
        ret, frame = video.read()
        if not ret:     # error with video reading
            print("Video could not be read to tracker.")
            break

        cur_cpframe = cpframe_list[i]       # the CPFrame corresponding to the current frame being tracked

        timer = cv2.getTickCount()      # for calculation of frames per second

        # multi_tracker cycles through every tracker and updates each tracker individually
        for tracker in multi_tracker:
            ret, bbox = tracker.update(frame)   # update individual cell tracker
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)     # calculate FPS

            # update displayed bounding box for next frame or remove tracker if bounding box is out of frame/ROI
            if ret:
                # calculate coordinates of bounding box
                # bbox (bounding box): (upper left x, y, lower right x, y)
                p1 = (int(bbox[0]), int(bbox[1]))                           # upper left side of bounding box
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))       # lower right side

                # remove trackers that have jumped to a different cell

                # check if any part of the bounding box has exited frame or user-selected ROI
                if p1[0] < 0 or p2[0] > frame_width or p1[1] < 0 or p2[1] > frame_height:
                    cv2.rectangle(frame, p1, p2, (0, 0, 150), 2, 1)     # red box
                    multi_tracker.remove(tracker)      # remove tracker from list to be updated next frame
                elif set_bounds and not cur_cpframe.check_boundaries(p1, p2):
                    cv2.rectangle(frame, p1, p2, (0, 0, 150), 2, 1)
                    multi_tracker.remove(tracker)
                else:
                    cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)     # blue box

                    # update cell information in CPFrame based on new tracker location
                    # tracker_center is the integer center (rounded up) coordinate of the tracking box
                    tracker_center = (math.ceil(0.5*int(p1[0]) + 0.5*int(p2[0])), math.ceil(0.5*int(p1[1]) + 0.5*int(p2[1])))
                    cell_temp_id = cur_cpframe.get_cell_from_coord(tracker_center)

            # display the user-selected ROI
            if set_bounds:
                cv2.rectangle(frame, embryo_bounds, (0, 150, 0), 2, 1)  # green box

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

    video.release()
    output.release()
    cv2.destroyAllWindows()


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
