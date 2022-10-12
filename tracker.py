# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/3/2022
# Bio97 Thesis Project
# OpenCV2 video object tracker, code modified from code at https://broutonlab.com/blog/opencv-object-tracking

import cv2

def track(video_file_path, frame_num, tracker_type, speed="fast"):

    if speed == "slow":
        s = 300
    elif speed == "medium":
        s = 200
    elif speed == "fast":
        s = 100

    # create tracker
    if tracker_type == "TrackerKCF":
        tracker = cv2.TrackerKCF_create()
    elif tracker_type == "TrackerMOSSE":
        tracker = cv2.legacy.TrackerMOSSE_create()
    elif tracker_type == "TrackerCSRT":
        tracker = cv2.TrackerCSRT_create()
    else:   # default
        tracker = cv2.TrackerCSRT_create()

    video = cv2.VideoCapture(video_file_path)
    ret, frame = video.read()

    frame_height, frame_width = frame.shape[:2]
    # Resize the video for a more convinient view
    frame = cv2.resize(frame, [frame_width // 2, frame_height // 2])
    # Initialize video writer to save the results
    output = cv2.VideoWriter(f'{tracker_type}.avi',
                             cv2.VideoWriter_fourcc(*'XVID'), 60.0,
                             (frame_width // 2, frame_height // 2), True)
    if not ret:
        print("Video cannot be read from file.")

    # Select the bounding box in the first frame
    bbox = cv2.selectROI(frame, False)
    ret = tracker.init(frame, bbox)

    # Start tracking
    for i in range(0, frame_num - 1):
        ret, frame = video.read()
        if not ret:
            print("Video could not be read to tracker.")
            break
        frame = cv2.resize(frame, [frame_width // 2, frame_height // 2])

        timer = cv2.getTickCount()
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