# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 1/28/2023
# Bio97 Thesis Project
# Matches the cells tracked by each tracker to their global ID and puts their coordinates in a global FrameConnector
# data structure

import FrameConnector
import CPFrame

# matches the cells tracked by each tracker to their global_id and adds them to the FrameConnector
# inputs: cpframe_list - list of the CPFrame data structures extracted from the .npy images
#         frame_connector - initialized FrameConnector object, can be empty or can contain information
#         coords_list - list of lists containing the center coordinate information of each tracker for each
#                       frame in the video, in form:
#                       [[tracker 1 center_coord frame 0, 1, 2, ...], [tracker 2 center_coord frame 0, 1, 2...]. ...]
# output: None
def match(cpframe_list, frame_connector, coords_list):

    # match each coordinate in the coordinate list to a cell in the given frame of the video
    for i in range(len(cpframe_list)):
        frame_id = cpframe_list[i].get_frame_id()

        # get list of all center cell coordinates during the current CPFrame
        tracker_center_list = []  # the center coordinate for each tracker in the current frame
        for track in coords_list:
            if i < len(track):
                tracker_center_list.append(track[i])

        go_tracker_order = [-2 for x in range(len(coords_list))]  # the tracker's cell's global_id, in order of the trackers in this cp_frame

        # for first frame in a t-constant (z) video, need to match trackers to cell global_ids
        if not frame_connector.is_empty() and i == 0:  # first frame in t-constant video

            # add the center coordinate of the tracker (coord[0]) in their global cell_id order
            go_coords = frame_connector.get_cells_in_frame(frame_id)  # list of cell coordinates in their global_id order
            go_center_list = []

            for coord in go_coords:
                go_center_list.append(coord[0])

            # make list of tracker's cell's global_ids, list in order of trackers in this cp_frame
            j = 0

            for center in tracker_center_list:  # for the center coordinate of every tracker
                if center in go_center_list:  # if it matches the center coordinate of a tracker in the t (z-constant) CPFrame
                    index = go_center_list.index(center)
                    go_tracker_order[j] = index
                else:
                    go_tracker_order[j] = -1
                j += 1


            # don't need to add cells to FrameConnector because this CPFrame has already been added during
            # the t (z-constant) video

        # match trackers to global cell_ids and add them to the FrameConnector
        k = 0       # tracker count
        for track in coords_list:

            if i > len(track) - 1:   # if tracker was aborted before this frame
                continue
            elif go_tracker_order[k] == -1:     # if tracker is not tracking a cell
                continue

            # match tracker center coordinate to cell in CPFrame
            cell_id = cpframe_list[i].get_cell_from_coord(track[i])  # get the temp_id of the cell at that coordinate

            if cell_id == -1:  # if tracker not tracking a cell
                continue

            # get list of all coordiantes belonging to that cell
            cell_coords = cpframe_list[i].get_cell_coords(cell_id)  # get the list of pixels within the cell

            # add cells to FrameConnector
            # cell coordinate data stored in structure [[center coordinate], [cell coordinate 0, ..., n]]
            center_coord = tracker_center_list[k]
            coords_data = [center_coord, cell_coords]  # list of [[center coordinate], [cell coordinate 0, ..., n]]

            if frame_connector.is_empty():  # this is the first frame in the first video
                frame_connector.add_frame(k, cpframe_list[i].get_frame_id, coords_data)
            else:
                frame_connector.add_frame(go_tracker_order[k], cpframe_list[i].get_frame_id, coords_data)