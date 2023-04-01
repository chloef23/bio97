# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 11/2/2022
# Bio97 Thesis Project
# CPTracker -- 4D cell tracking program that interfaces with the .npy outputs from Cellpose

import os
import re
import shutil
import pandas as pd

import run_tracker
import FrameConnector

#######################################################################################################################
#######################################################################################################################

# user-specified inputs
FOLDER_NAME = "20230207_0002_npys"     # name of the folder where .npy files are stored
VIDEO_FPS = 5    # frames per second desired in mp4 video, cannot be less than 0.01
                 # note: this does not affect the speed of the tracker - that is solely determined by the number of
                 #       items to track

ZVALUE = 16     # the user-selected z-stack value to split each z-stack (t-constant) video at
TVALUE = [1, 5, 10, 15]        # the user-selected t values to run z-stack (t-constant) video at
JUMP_LIMIT = 15                 # the user-selected threshold for the maximum distance cells can travel over one frame

# algorithm used for tracker
TRACKER_TYPE = "TrackerCSRT"    # recommended algorithm
# tracker_type = "TrackerKCF"

#######################################################################################################################
#######################################################################################################################

# cycles through the .npys in the folder and splits them into a single t video (at z = ZVALUE) and two z videos
# for every timepoint (from ZVALUE to 0 and ZVALUE to the bottom), then, initializes an empty FrameConnector and
# runs the tracker on every video
# inputs: user-specified inputs at top of file
# outputs: the FrameConnector containing the coordinates contained within each cell at each timepoint
def main():

    # generate folder with correctly-named copies of the .npy files
    gen_dir_name = "__CPTracker_folder__"      # CPTracker generates folder with correctly-named .npys to cycle through
    dir_path = FOLDER_NAME + '/' + gen_dir_name

    if os.path.exists(dir_path) and os.path.isdir(dir_path):    # if generated folder exists
        print("exists")

    else:   # generate CPTracker folder
        os.makedirs(dir_path)

    # cycle through the folders and extract the txxzxx name
    file_list = []  # list of all of the generated file names

    for filename in os.scandir(FOLDER_NAME):
        if filename.is_file() and os.path.splitext(filename)[1] == ".npy":      # if the file is a .npy
            match = re.search(r't[0-9]{3}_z[0-9]{3}', filename.path)
            if match:
                new_filename = dir_path + "/" + str(match.group(0)) + ".npy"
                shutil.copy(filename.path, new_filename)
                file_list.append(str(match.group(0)))
            else:
                print("Error: file name " + filename.path + " not formatted correctly")
                print("Please include txxx_zxxx in the filename, where xxx are three integers,\n"
                      "with txxx representing the t_value of the frame and zxxx representing the z-value of the frame")
                continue

    if len(file_list) > 0:      # if any files match the correct formatting
        vids_list = generate_video_lists(file_list, ZVALUE, TVALUE, dir_path)     # generate lists of .npys to create videos with
        print(vids_list)
    else:
        print("\nError: No files could be processed. Please check filename format and try again.")
        return -1

    # cycle through lists of .npys and run the tracker program
    frame_connector = FrameConnector.FrameConnector()       # initialize FrameConnector object
    i = 0
    for v in range(len(vids_list)):
        video = vids_list[v]
        if not (i % 2) == 0:     # need to reverse the direction of the upper videos (index 1, 3, etc.)
            video = video[::-1]

        # true if this is the first video
        if i == 0:
            first_video_bool = True
        else:
            first_video_bool = False

        run_tracker.run_tracker(video, TRACKER_TYPE, frame_connector, JUMP_LIMIT, dir_path,
                               video_fps=VIDEO_FPS, first_video=first_video_bool, overwrite_image=False)
        i += 1

    format_output(frame_connector, dir_path)

# generate list of filenames for each video to run -- one z-constant video at the user-specified ZVALUE,
# and then t-constant videos for each user-specified TVALUE
# inputs: gen_file_list -- a list of the files in the generated directory with correctly named .npy files
#         zvalues -- user-specified value to split the z-stack (t-constant) videos at and create t-constant video at
#         tvalue -- user-specififed values to create t-constant (z-stack) videos of
#         dir_path -- the path to the directory containing the images
# output: vids_list -- nested list of file names that belonging to first, the t (z-constant) video, then
#                      each z-stack (t-constant) video in the user-specified order, split at the TVALUE, with
#                      lists in order [upper z0, lower z0, upper z1, lower z1, ... upper zn, lower zn]
def generate_video_lists(gen_file_list, zvalue, tvalues, dir_path):

    vids_list = []      # output nested list of files in t- and z-constant videos

    # get maximum z and t to create dataframe
    z_max = 0
    t_max = 0
    for file in gen_file_list:
        z_num = int(re.search(r'z[0-9]{3}', file).group(0)[1:])
        if z_num > z_max:
            z_max = z_num
        t_num = int(re.search(r't[0-9]{3}', file).group(0)[1:])
        if t_num > t_max:
            t_max = t_num

    frame_df = pd.DataFrame(index=range(z_max),columns=range(t_max))            # create dataframe with time as columns
                                                                                # and z as rows
    # add filenames to their appropriate cell in the dataframe
    for file in gen_file_list:
        z_num = int(re.search(r'z[0-9]{3}', file).group(0)[1:])
        t_num = int(re.search(r't[0-9]{3}', file).group(0)[1:])
        frame_df.at[z_num, t_num] = file

    # extract (t) z-constant video file names
    t_list = frame_df.loc[[zvalue]].to_numpy()[0]
    t_list = list(t_list[~pd.isna(t_list)] ) # remove NaNs and append to video list
    if not len(t_list) == 0:
        path_t_list = []
        for i in t_list:
            path_t_list.append(dir_path + "/" + str(i) + ".npy")  # add full path to file names
        vids_list.append(path_t_list)

    # extract upper and lower (z) t-constant video file names
    for z in tvalues:
        upper_z_list = frame_df.loc[0:zvalue][z].to_numpy()
        upper_z_list = upper_z_list[~pd.isna(upper_z_list)]     # remove NaNs and append to video list
        if not len(upper_z_list) == 0:
            path_upper_z_list = []
            for i in upper_z_list:
                path_upper_z_list.append(dir_path + "/" + str(i) + ".npy")     # add full path to file names
            vids_list.append(path_upper_z_list)

        lower_z_list = frame_df.loc[zvalue:z_max][z].to_numpy()
        lower_z_list = lower_z_list[~pd.isna(lower_z_list)]
        if not len(lower_z_list) == 0:
            path_lower_z_list = []
            for i in lower_z_list:
                path_lower_z_list.append(dir_path + "/" + str(i) + ".npy")  # add full path to file names
            vids_list.append(path_lower_z_list)

    return vids_list


# cycle through FrameConnector and print csv containing columns: cell (starting from 1), x coordinate, y coordinate,
# z oordinate (starting from 1), and frame number (time, starting from 1)
# inputs: frame_connector - filled frame connector
#         file_path - path to the folder the file will be created in
# output: csv containing information retrieved from FrameConnector
def format_output(frame_connector, file_path):

    if frame_connector.is_empty():
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

    # uncomment for headers for the .csv
    # fp.write("Cell,X-Coord,Y-Coord,Z-Coord,Time\n")

    # cycle through FrameConnector and retrieve information
    cell_dict_list = frame_connector.get_dict_list()
    for i in range(len(cell_dict_list)):  # for each cell
        cell_dict = cell_dict_list[i]

        j = 0
        for key, value in cell_dict.items():    # for each time frame
            print(key)
            # get z value and frame number from cell dictionary key (originally from filename)
            zt = re.search(r't[0-9]{3}_z[0-9]{3}', key)
            if zt:
                zt = zt.group(0)
                z = int(re.search(r'z[0-9]{3}', zt).group(0)[1:])  # z layer number
                t = int(re.search(r't[0-9]{3}', zt).group(0)[1:])  # frame (timepoint) number
            else:
                print("Error: z and t values could not be extracted from the file names, have been replaced with -1")
                z = -1
                t = -1
            j += 1

            for n in value:      # for each coordinate
                temp_string = str(i + 1) + "," + str(n[0]) + "," + str(n[1]) + "," \
                              + str(z) + "," + str(t) + "\n"
                fp.write(temp_string)

    fp.close()

    return 0



# run the CPTracker
if __name__ == "__main__":
    main()