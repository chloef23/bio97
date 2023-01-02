# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 9/26/2022
# Bio97 Thesis Project
# Runs the cell tracker for one video

# import packages
import load_npy
import frames_to_video
import tracker

# runs the cell tracker for one video
# input: image_list - list of all .npy images in the order of the video
#        tracker_type - cv2 tracker algorithm to use, "TrackerCSRT" is recommended
#        video_fps - int; frames per second of output .mp4 created from the .npys (not tracking video), default is 4
#        overwrite_images - boolean; if True, .pngs generated from .npys will be overwritten (if present), if False,
#                           .pngs will not be re-generated
# output:
def run_tracker(image_list, tracker_type, video_fps=4, overwrite_image=False):

    # convert all .npy in folder to pngs
    png_list = []
    cpframe_list = []
    frame_num = 0
    for npy in image_list:

        # check to see if the png already exists, if so, don't create again
        png_name = npy + ".png"
        if os.path.exists(png_name):
            # if overwrite_image == True, force-generate pngs by setting png_generate = False
            bool = not overwrite_image

            # load information contained in .npys, generate pngs only if png_generated == False
            png, cpframe = load_npy.load(npy, png_generated=bool)
            print(png + " found")

        # create png and load information from .npy
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
    frames_to_video.write_video(video_file_path, png_list, video_fps)

    tracker.track(video_file_path, frame_num, tracker_type, cpframe_list[0], set_bounds=False)


# unit test
if __name__ == "__main__":
    import os

    FOLDER_NAME = "z_tracking_test"  # name of the folder where .npy files are stored
    VIDEO_FPS = 4
    TRACKER_TYPE = "TrackerCSRT"

    # Get the folder containing .npy files of the image sequence
    video_folder = FOLDER_NAME
    img_list = []  # list containing all filenames of images in folder
    for filename in os.scandir(video_folder):
        if filename.is_file() and os.path.splitext(filename)[1] == ".npy":
            img_list.append(filename.path)

    run_tracker(img_list, TRACKER_TYPE, video_fps=VIDEO_FPS, overwrite_image=False)

