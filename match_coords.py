# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 1/28/2023
# Bio97 Thesis Project
# Matches the cells tracked by each tracker to their global ID and puts their coordinates in a global FrameConnector
# data structure

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

# matches the cells tracked by each tracker to their global_id and adds them to the FrameConnector
# inputs: cpframe_list - list of the CPFrame data structures extracted from the .npy images
#         frame_connector - initialized FrameConnector object, can be empty or can contain information
#         coords_list - list of lists containing the center coordinate information of each tracker for each
#                       frame in the video, in form:
#                       [[tracker 1 center_coord frame 0, 1, 2, ...], [tracker 2 center_coord frame 0, 1, 2...]. ...]
# output: None
def match(cpframe_list, frame_connector, coords_list):

    # list the cell coordinates in the global order of the cell trackers
    if frame_connector.is_empty():      # this is the first video in the list (the time/z-constant video)
        new_coords_list = coords_list

    else:     # this is a z (time-constant) video
        center_coords_list = [x[0] for x in coords_list]    # the center coordinate of each tracker in the first frame
        frame_0 = cpframe_list[0].get_frame_id()        # the name of the first frame
        new_coords_list = []

        # match center coordinates of trackers at first frame of first video to trackers in first frame of current video
        for coord in frame_connector.get_cells_in_frame(frame_0)[0]:
            if coord in center_coords_list:
                c_index = center_coords_list.index(coord)
                new_coords_list.append(coords_list[c_index])

    # for each frame, match center coordinate of ordered trackers to cell and add to FrameConnector
    for i in range(len(cpframe_list)):
        frame = cpframe_list[i].get_frame_id()

        # get list of shapely Polygons formed by the coordinates of each cell in the CPFrame
        poly_list = []
        outlines_list = cpframe_list[i].get_outlines_list()
        for outline in outlines_list:
            poly_list.append(Polygon(outline))

        for j in range(len(new_coords_list)):

            if i >= len(new_coords_list[j]):     # if the tracker terminated before the video completed
                continue
            elif not new_coords_list[j][i]:     # coordinate is None, tracker was aborted before the video completed
                continue

            cell_center = Point(new_coords_list[j][i])     # the cell center of the tracker at the given frame
            # get the coordinates in the outline of the cell containing the given point, if this cell exists
            coords = get_cell_containing_point(poly_list, outlines_list, cell_center)
            if coords is not None:
                coords_list = [new_coords_list[j][i], coords]       # cell center first for easier debugging
                frame_connector.add_cell(j, frame, coords_list)


# return the outline of a cell that contains a point, if one exists
# input: polygon_list - a list containing the shapely Polygons of each cell in the frame
#        outline_list - a 2D list containing the coordinates making up the outline of each cell
#                        in form [[(cell 0 x0, y0), (cell 0 x1, y1) ... ], ... [(cell n x0, y0), ..., (cell n xn, yn)]]
#                        note: outlines list must be in the same order as polygon_list
#        point - a shapely Point
# output: cell_coords_list - list of coordiantes of the outline of the cell containing the point, or None if
#                            there is no cell that contains the point
def get_cell_containing_point(polygon_list, outline_list, point):
    if not point:       # point is None
        return None

    # cycle through the polygons and check if a cell is within or on the border of the polygon
    for i in range(len(polygon_list)):
        poly = polygon_list[i]
        if poly.contains(point):
            return outline_list[i]      # return the corresponding list of coordinates

    return None














    # go_tracker_order = [-2 for x in range(len(coords_list))]  # the tracker's cell's global_id, in order of the trackers in this cp_frame
    #                                                           # fill list with -2 to indicate empty cell
    #
    # # match each coordinate in the coordinate list to a cell in the given frame of the video
    # for i in range(len(cpframe_list)):
    #     frame_id = cpframe_list[i].get_frame_id()
    #
    #     # get list of all center cell coordinates during the current CPFrame
    #     tracker_center_list = []  # the center coordinate for each tracker in the current frame
    #     for track in coords_list:
    #         if not track:
    #             continue
    #         elif i < len(track):        # OJO: changed from -1
    #             tracker_center_list.append(track[i])
    #
    #     # for first frame in a t-constant (z) video, need to match trackers to cell global_ids
    #     if not frame_connector.is_empty() and i == 0:  # first frame in t-constant video
    #
    #         # add the center coordinate of the tracker (coord[0]) in their global cell_id order
    #         go_coords = frame_connector.get_cells_in_frame(frame_id)  # list of cell coordinates in their global_id order
    #         go_center_list = []
    #
    #         for coord in go_coords:
    #             go_center_list.append(coord[0])
    #
    #         # make list of tracker's cell's global_ids, list in order of trackers in this cp_frame
    #         j = 0
    #
    #         for center in tracker_center_list:  # for the center coordinate of every tracker
    #             if center in go_center_list:  # if it matches the center coordinate of a tracker in the t (z-constant) CPFrame
    #                 index = go_center_list.index(center)
    #                 go_tracker_order[j] = index
    #             else:
    #                 go_tracker_order[j] = -1
    #             j += 1
    #     elif frame_connector.is_empty and i == 0:
    #         for k in range(len(coords_list)):
    #             go_tracker_order[k] = k
    #         # don't need to add cells to FrameConnector because this CPFrame has already been added during
    #         # the t (z-constant) video
    #
    #     # match trackers to global cell_ids and add them to the FrameConnector
    #     print("tracker list len " + str(len(tracker_center_list)))
    #     print(coords_list)
    #     print("coords list len " + str(len(coords_list)))
    #     for k in range(len(coords_list)):
    #         print("k " + str(k))
    #         track = coords_list[k]
    #         print("track len " + str(len(track)))
    #
    #         if len(tracker_center_list) == 0:
    #             continue
    #         if not track:   # tracker slot is empty
    #             continue
    #         elif i > len(track) - 1:   # if tracker was aborted before this frame
    #             continue
    #         elif go_tracker_order[k] == -1 or go_tracker_order[k] == -2:     # if tracker is not tracking a cell
    #             continue
    #
    #         # match tracker center coordinate to cell in CPFrame
    #         cell_id = cpframe_list[i].get_cell_from_coord(track[i])  # get the temp_id of the cell at that coordinate
    #         # print("local id " + str(cell_id))
    #         # print("center coord " + str(track[i]))
    #
    #         if cell_id == -1:  # if tracker not tracking a cell
    #             continue
    #
    #         # get list of all coordiantes belonging to that cell
    #         cell_coords = cpframe_list[i].get_cell_coords(cell_id)  # get the list of pixels within the cell
    #
    #         # add cells to FrameConnector
    #         # cell coordinate data stored in structure [[center coordinate], [cell coordinate 0, ..., n]]
    #         center_coord = tracker_center_list[k]
    #         coords_data = [center_coord, cell_coords]  # list of [[center coordinate], [cell coordinate 0, ..., n]]
    #         frame_id = str(cpframe_list[i].get_frame_id())
    #
    #         if frame_connector.is_empty():  # this is the first frame in the first video
    #             # print("global id " + str(k))
    #             frame_connector.add_frame(k, frame_id, coords_data)
    #         else:
    #             # print("calc global id " + str(go_tracker_order[k]))
    #             frame_connector.add_frame(go_tracker_order[k], frame_id, coords_data)

