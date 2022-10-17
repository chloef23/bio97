# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/3/2022
# Bio97 Thesis Project
# OpenCV2 video object tracker, code modified from code at https://broutonlab.com/blog/opencv-object-tracking

import cv2
import os

def track(video_file_path, frame_num, tracker_type, init_cpframe, speed="fast"):

    # set speed out output video
    if speed == "slow":
        s = 300
    elif speed == "medium":
        s = 200
    elif speed == "fast":
        s = 100

    # read mp4 video found at inputted file path
    if not os.path.exists(video_file_path):
        print("Video file could not be found.")
        exit()
    if os.path.splitext(video_file_path)[1] != ".mp4":
        print("Video file is not of type mp4.")
        exit()

    video = cv2.VideoCapture(video_file_path)
    ret, frame = video.read()

    # initialize video display
    frame_height, frame_width = frame.shape[:2]     # resize the video for a more convenient view
    frame = cv2.resize(frame, [frame_width // 2, frame_height // 2])
    # initialize video output
    output = cv2.VideoWriter(f'{tracker_type}.avi',     # initialize video writer to save the results
                             cv2.VideoWriter_fourcc(*'XVID'), 60.0,
                             (frame_width // 2, frame_height // 2), True)
    if not ret:
        print("Video cannot be read from file.")

    # Select the bounding box in the first frame
    multi_tracker = []    # list of all the trackers
    for cell in range(1, 5): #init_cpframe.get_cell_min_max():
        # print(cell[0][0], cell[0][1], cell[1][0], cell[1][1])
        # bbox = (cell[0][0], cell[0][1], cell[1][0] - cell[0][0], cell[0][1] - cell[1][1])   # (x, y, w, h)
        # p1 = (int(bbox[0]), int(bbox[1]))
        # p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        # cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

        bbox = cv2.selectROI(frame, False)
        print(bbox)
        temp_tracker = create_tracker(tracker_type)
        temp_tracker.init(frame, bbox)
        multi_tracker.append(temp_tracker)

    print(multi_tracker)


    # Start tracking
    for i in range(0, frame_num - 1):
        ret, frame = video.read()
        if not ret:
            print("Video could not be read to tracker.")
            break
        frame = cv2.resize(frame, [frame_width // 2, frame_height // 2])

        timer = cv2.getTickCount()
        for tracker in multi_tracker:
            ret, bbox = tracker.update(frame)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            if ret:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
            else:
                cv2.putText(frame, "Tracking failure detected", (100, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.putText(frame, tracker_type + " Tracker", (100, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
        cv2.imshow("Tracking", frame)
        output.write(frame)
        k = cv2.waitKey(s) & 0xff
        if k == 27:
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
    elif tracker_type == "TrackerMOSSE":
        tracker = cv2.TrackerMOSSE_create()
    elif tracker_type == "TrackerCSRT":
        tracker = cv2.TrackerCSRT_create()
    else:   # default
        tracker = cv2.TrackerCSRT_create()

    return tracker