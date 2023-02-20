# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 9/26/2022
# Bio97 Thesis Project
# Runs the cell tracker for one video

# import packages
import load_npy
import frames_to_video
import tracker
import match_coords

# convert a list of .npy images to an .mp4 video, then runs the cell tracker for that video
# input: image_list - list of all .npy images in the order of the video
#        tracker_type - cv2 tracker algorithm to use, "TrackerCSRT" is recommended
#        frame_connector - initialized FrameConnector object, can be empty or can contain information
#        jump_limit - how far the tracker is allowed to move between frames
#        coords_list - optional, pass in a list of coordinates to bypass tracking
#        video_fps - int; frames per second of output .mp4 created from the .npys (not tracking video), default is 4
#        overwrite_images - boolean; if True, .pngs generated from .npys will be overwritten (if present), if False,
#                           .pngs will not be re-generated
# output: none
def run_tracker(image_list, tracker_type, frame_connector, jump_limit, coords_list=None, video_fps=4, overwrite_image=False):

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

    # convert pngs to mp4 video
    video_file_path = FOLDER_NAME + "/cell_tracker_video.mp4"
    frames_to_video.write_video(video_file_path, png_list, video_fps)

    if not coords_list:
        # run the tracker program on the video
        coords_list = tracker.track(video_file_path, frame_num, tracker_type, cpframe_list[0], jump_limit)

    # match trackers to cells and add their coordinates to FrameConnector
    print("Matching trackers...")
    match_coords.match(cpframe_list, frame_connector, coords_list)

    return frame_connector


# cycle through FrameConnector and print csv containing columns: cell (starting from 1), x coordinate, y coordinate,
# z oordinate (starting from 1), and frame number (time, starting from 1)
# inputs: frame_connector - filled frame connector
#         file_path - path to the folder the file will be created in
# output: csv containing information retrieved from FrameConnector
def format_output(frame_connector, file_path, z_max, t_max):
    if frame_connector.is_empty:
        print("Error: FrameConnector is empty")
        return -1
    elif not os.path.exists(file_path) or not os.path.isdir(file_path):
        print("Error: could not find folder")
        return -1

    file_loc = file_path + "/cptracker_output.csv"
    fp = open(file_loc, "w")

    if not fp:
        print("Error: could not create file in folder given")
        return -1

    # cycle through FrameConnector and retrieve information
    for i in range(len(frame_connector)):  # for each cell
        cell_dict = frame_connector.retrieve_frame_info(i)

        for j in range(t_max + 1):  # for each frame (timepoint) the cell is in
            for k in range(z_max + 1):  # for each z layer in the timepoint
                # TODO: get from frame name
                for n in cell_dict:
                    temp_string = str(i + 1) + "," + str(n[0]) + "," + str(n[1]) + "," + str(k + 1) + "," + str(j + 1)
                    fp.write(temp_string)

    fp.close()

    return 0


# unit test
if __name__ == "__main__":
    import os
    import FrameConnector

    FOLDER_NAME = "z_tracking_test_0"  # name of the folder where .npy files are stored
    VIDEO_FPS = 4
    TRACKER_TYPE = "TrackerCSRT"
    JUMP_LIMIT = 10

    verbose = False     # when verbose == True, files that are unable to load will print error statements

    frame_connector = FrameConnector.FrameConnector()

    # get the folder containing .npy files of the image sequence
    video_folder = FOLDER_NAME
    img_list = []  # list containing all filenames of images in folder
    for filename in os.scandir(video_folder):
        if filename.is_file() and os.path.splitext(filename)[1] == ".npy":
            img_list.append(filename.path)
        elif verbose:
            print("Error: unable to load file" + filename.path + " in folder")

    rev_img_list = img_list[::-1]

    # coords_list = [[(387, 12), (387, 13), (406, 17), (407, 16), (407, 17), (407, 18), (406, 19), (406, 19), (405, 19), (404, 20), (405, 20), (403, 20), (404, 20), (404, 20), (402, 20), (403, 21), (402, 21), (403, 21), (406, 14), (405, 19), (399, 21), (396, 23), (404, 25), (401, 24), (402, 28), (391, 39), (388, 39), (396, 31), (405, 37), (399, 27), (386, 26), (384, 23), (374, 22), (375, 22), (364, 28), (359, 30), (358, 29), (351, 28), (352, 39), (352, 41)], [(337, 14), (337, 16), (338, 13), (339, 14), (340, 15), (340, 16), (341, 14), (340, 16), (341, 16), (341, 14), (341, 14), (342, 17), (342, 17), (341, 16), (342, 16), (342, 17), (345, 17), (344, 17), (345, 16), (338, 23), (328, 16), (329, 19), (12, 13), (638, 16), (639, 16), (376, 91), (386, 85), (393, 89), (385, 90)], [(375, 27), (373, 29), (391, 30), (392, 25), (390, 32), (387, 39), (388, 39), (389, 33), (340, 30), (335, 19), (340, 20), (345, 15), (356, 22), (374, 20), (385, 23), (396, 24), (391, 23), (389, 19), (380, 18), (380, 19), (368, 25), (364, 27), (362, 25), (356, 24), (356, 35), (357, 38), (12, 12), (634, 16), (364, 88), (368, 91), (368, 90)], [(317, 29), (317, 29), (317, 28), (318, 28), (319, 29), (318, 29), (319, 29), (321, 29), (322, 27), (324, 28), (324, 27), (324, 26), (323, 27), (323, 28), (324, 29), (325, 29), (328, 31), (330, 30), (345, 38), (340, 45), (338, 38), (334, 40), (389, 41), (385, 42), (386, 45), (387, 42), (384, 42), (381, 48), (378, 44), (384, 44), (381, 43), (368, 41), (359, 40), (360, 40), (349, 45), (343, 47), (343, 47), (336, 45), (336, 56), (337, 59), (625, 21), (629, 18), (635, 16)], [(354, 30), (355, 31), (355, 31), (354, 31), (354, 31), (365, 48), (365, 50), (365, 50), (365, 52), (365, 52), (365, 52), (367, 53), (366, 55), (368, 56), (370, 56), (368, 54), (368, 55), (379, 61), (379, 56), (388, 45), (385, 38), (383, 40), (497, 57), (512, 64), (515, 63), (529, 50), (542, 38), (542, 36), (555, 28), (574, 31), (576, 29), (571, 28), (582, 41), (581, 42), (577, 43), (574, 41), (581, 36), (598, 39), (613, 44), (612, 43), (608, 41), (618, 33), (617, 31)], [(415, 39), (415, 38), (415, 40), (414, 40), (414, 40), (413, 43), (414, 42), (431, 29), (430, 29), (429, 29), (429, 31), (427, 30), (428, 30), (440, 20), (439, 21), (438, 21), (438, 22), (437, 22), (437, 23), (449, 35), (464, 47), (481, 53), (339, 51), (339, 40), (342, 42), (344, 39), (347, 44), (362, 45), (358, 42), (365, 43), (362, 43), (365, 40), (356, 41), (357, 40), (353, 49), (362, 53), (362, 51), (356, 49), (355, 60), (358, 62)], [(332, 40), (332, 40), (332, 41), (333, 39), (333, 39), (334, 39), (334, 38), (344, 53), (345, 53), (345, 53), (346, 53), (347, 54), (346, 56), (349, 56), (351, 56), (349, 55), (348, 57), (352, 42), (347, 39), (338, 45), (341, 39), (337, 41), (388, 41), (383, 41), (385, 44), (387, 40), (384, 40), (382, 48), (379, 44), (385, 42), (382, 43), (388, 44), (380, 44), (381, 44), (372, 50), (364, 51), (363, 51), (357, 50), (356, 59), (357, 62)], [(371, 50), (369, 51), (368, 51), (367, 50), (367, 50), (367, 49), (364, 50), (364, 50), (363, 52), (367, 53), (369, 53), (370, 54), (369, 56), (373, 57), (374, 57), (372, 56), (371, 56), (378, 61), (378, 56), (386, 44), (384, 38), (383, 40), (401, 20), (398, 20), (398, 23), (390, 20), (377, 19), (369, 14), (379, 16), (393, 20), (387, 20), (385, 16), (376, 15), (375, 16), (364, 21), (360, 24), (358, 23), (352, 22), (352, 33), (353, 35), (346, 35), (348, 30), (354, 86), (352, 86)], [(396, 46), (398, 46), (398, 49), (409, 38), (413, 37), (413, 38), (412, 37), (412, 37), (412, 37), (411, 37), (412, 38), (410, 37), (407, 38), (406, 38), (407, 38), (405, 38), (407, 38), (401, 22), (403, 17), (404, 16), (396, 16), (393, 18), (324, 65), (324, 55), (326, 56), (329, 53), (332, 57), (348, 59), (344, 56), (350, 57), (346, 57), (351, 55), (344, 54), (344, 54), (336, 61), (329, 61), (328, 61), (322, 59), (322, 70), (322, 73), (327, 82), (338, 87), (348, 90)], [(315, 52), (314, 51), (316, 52), (315, 51), (317, 51), (316, 52), (317, 52), (319, 51), (323, 49), (324, 50), (325, 49), (326, 49), (326, 50), (328, 51), (329, 51), (327, 51), (329, 52), (333, 51), (331, 54), (324, 59), (324, 52), (320, 56), (387, 44), (381, 43), (383, 46), (387, 43), (384, 44), (381, 51), (378, 46), (384, 44), (382, 46), (388, 46), (379, 46), (380, 46), (372, 52), (363, 53), (363, 54), (356, 52), (356, 62), (357, 64), (346, 37), (348, 33), (350, 87)], [(347, 54), (347, 55), (346, 57), (346, 56), (346, 57), (362, 52), (364, 52), (365, 53), (365, 54), (367, 55), (366, 55), (367, 57), (367, 59), (369, 59), (370, 59), (369, 58), (369, 58), (376, 64), (376, 58), (384, 46), (382, 40), (381, 43), (368, 46), (362, 45), (364, 48), (367, 45), (386, 41), (398, 30), (409, 34), (423, 36), (422, 28), (422, 36), (432, 41), (363, 51), (356, 50), (355, 59), (356, 62), (346, 36), (348, 31), (353, 87), (350, 87)], [(384, 62), (383, 61), (388, 82), (384, 86), (389, 81), (388, 81), (384, 86), (387, 80), (387, 80), (384, 86), (383, 87), (384, 89), (371, 98), (371, 99), (369, 103), (371, 99), (368, 104), (371, 99), (362, 55), (364, 46), (362, 47), (389, 42), (384, 42), (387, 44), (390, 40), (386, 40), (381, 49), (380, 45), (386, 42), (384, 43), (388, 43), (379, 44), (380, 44), (372, 50), (327, 63), (326, 61), (320, 60), (319, 70), (320, 74), (325, 81), (337, 87), (346, 90)], [(327, 70), (326, 69), (326, 70), (326, 70), (327, 69), (331, 69), (331, 67), (343, 55), (345, 52), (346, 55), (345, 54), (347, 55), (346, 57), (349, 57), (350, 58), (349, 54), (350, 56), (356, 65), (379, 58), (388, 45), (386, 39), (384, 41), (343, 71), (343, 61), (344, 62), (348, 60), (351, 64), (347, 60), (342, 58), (348, 58), (344, 57), (347, 56), (342, 55), (343, 55), (334, 61), (326, 62), (326, 62), (318, 60), (318, 70), (319, 74), (323, 82), (336, 87), (345, 91)], [(407, 67), (409, 69), (409, 68), (408, 66), (410, 68), (409, 69), (409, 70), (409, 69), (410, 68), (407, 69), (407, 70), (406, 70), (404, 70), (402, 71), (403, 72), (402, 70), (400, 69), (398, 69), (350, 59), (343, 66), (343, 59), (338, 61), (343, 72), (343, 62), (344, 63), (347, 60), (351, 64), (347, 59), (341, 57), (347, 57), (343, 58), (347, 55), (341, 54), (342, 55), (333, 61), (348, 91)], [(346, 76), (347, 78), (345, 82), (348, 75), (346, 74), (350, 74), (350, 76), (347, 76), (348, 76), (347, 77), (348, 76), (348, 76), (347, 77), (352, 75), (352, 74), (350, 76), (354, 74), (354, 70), (363, 93), (359, 84), (345, 82), (342, 83), (409, 90), (371, 76), (369, 78), (366, 76), (364, 85), (366, 86), (364, 85)], [(365, 77), (365, 78), (366, 78), (367, 77), (367, 77), (368, 76), (368, 77), (366, 78), (367, 78), (367, 78), (368, 79), (369, 79), (372, 98), (371, 99), (370, 102), (371, 100), (368, 102), (372, 99), (403, 90), (409, 88), (406, 85), (413, 87), (410, 48), (407, 48), (409, 52), (402, 64), (394, 67), (390, 73), (388, 69), (386, 66), (380, 68), (383, 69), (384, 71), (380, 70), (378, 75)], [(388, 87), (388, 88), (389, 87), (389, 87), (389, 85), (390, 87), (390, 89), (387, 85), (390, 87), (389, 91), (402, 98), (405, 98), (404, 93), (403, 93), (404, 92), (405, 90), (403, 91), (408, 39), (408, 40), (407, 41), (405, 45)], [(409, 91), (410, 91), (412, 92), (411, 93), (410, 93), (409, 93), (410, 92), (408, 93), (409, 91), (409, 90), (404, 98), (406, 96), (393, 111), (406, 42), (406, 42), (406, 44)], [(330, 94), (331, 94), (328, 98), (328, 94), (329, 94), (336, 93), (336, 94), (348, 99), (349, 99), (350, 100), (350, 99), (351, 98), (403, 38), (403, 42)], [(352, 99), (355, 103), (370, 105), (370, 103), (370, 105), (370, 102), (369, 103), (371, 105), (372, 104), (387, 111)], [(372, 103), (373, 103), (371, 103), (369, 104), (372, 104), (372, 103), (369, 104), (373, 104), (374, 103), (392, 105), (409, 43), (405, 37)], [(392, 107), (393, 108), (392, 107), (390, 108), (391, 106), (392, 106), (390, 108), (390, 105), (391, 104), (408, 41)], [(392, 34), (394, 35), (391, 31), (408, 37), (410, 38), (409, 39), (410, 38), (409, 39), (409, 39)]]

    frame_connector = run_tracker(rev_img_list, TRACKER_TYPE, frame_connector, JUMP_LIMIT,
                                  coords_list=None, video_fps=VIDEO_FPS, overwrite_image=False)

    frame_connector.plot_cells(array_num=1)
    # frame_connector.print_FC()

    # format_output(frame_connector, FOLDER_NAME, 16, 0)
