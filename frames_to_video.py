# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/2/2022
# Bio97 Thesis Project
# Writes frames to an mp4 video file using OpenCV2, code modified from code at https://stackoverflow.com/questions/43048725/python-creating-video-from-images-using-opencv

import cv2

# writes frames to an mp4 video file
# inputs: file_path - path of outputted video, must end with .mp4
#         frames - list of images
#         fps - desired frame rate
# output: mp4 video at specified path
def write_video(file_path, frames, fps):
    # read images to cv2 images and add them to list
    im_list = []
    for image in frames:
        im_list.append(cv2.imread(image))

    # get dimensions of image
    h,w,l = im_list[0].shape

    # initialize video writer
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    writer = cv2.VideoWriter(file_path, fourcc, fps, (w, h))

    # write video
    for frame in im_list:
        writer.write(frame)

    writer.release()

# unit testing
if __name__ == "__main__":
    import os

    # png file
    FOLDER = ".npy test_1"
    frame_list = []
    for filename in os.scandir(FOLDER):
        if filename.is_file() and os.path.splitext(filename)[1] == ".png":
            frame_list.append(filename.path)

    write_video("video_unit_test.mp4", frame_list, 1)