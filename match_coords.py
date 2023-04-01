# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 1/28/2023
# Bio97 Thesis Project
# Matches the cells tracked by each tracker to their global ID and puts their coordinates in a global FrameConnector
# data structure
import math

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
        coords_list = [x for x in coords_list if x]         # remove empty lists
        center_coords_list = [x[0] for x in coords_list]    # the center coordinate of each tracker in the first frame
        frame_0 = cpframe_list[0].get_frame_id()        # the name of the first frame
        new_coords_list = []

        # match center coordinates of trackers at first frame of first video to trackers in first frame of current video
        first_vid_cells_list = frame_connector.get_first_vid_list()

        for coord in first_vid_cells_list:
            coord = tuple(coord)
            near_point = near(coord, center_coords_list, 5)     # if point is nearby a point in the list, Euclidean distance 5
            if near_point:
                c_index = center_coords_list.index(near_point)      # coord, index of the center coordinate of the tracker in the current video
                new_coords_list.append(coords_list[c_index])        # coordinates of the cell the tracker is tracking
            else:
                new_coords_list.append(None)

    # for each frame, match center coordinate of ordered trackers to cell and add to FrameConnector
    for i in range(len(cpframe_list)):
        frame = cpframe_list[i].get_frame_id()

        # get list of shapely Polygons formed by the coordinates of each cell in the CPFrame
        poly_list = []
        outlines_list = cpframe_list[i].get_outlines_list()
        for outline in outlines_list:
            poly_list.append(Polygon(outline))

        for j in range(len(new_coords_list)):
            if new_coords_list[j] is None:      # tracker did not match any cells in the first video
                continue
            elif i >= len(new_coords_list[j]):     # if the tracker terminated before the video completed
                continue
            elif not new_coords_list[j][i]:     # coordinate is None, tracker was aborted before the video completed
                continue

            cell_center = Point(new_coords_list[j][i])     # the cell center of the tracker at the given frame
            # get the coordinates in the outline of the cell containing the given point, if this cell exists
            coords = get_cell_containing_point(poly_list, outlines_list, cell_center)
            if coords is not None:
                # coords_list = [new_coords_list[j][i], coords]       # cell center first for easier debugging
                frame_connector.add_cell(j, frame, coords)


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

# return True if a point is near (defined by the user) a point in the second list
# inputs: point -- an (x, y) point
#         point_list -- second list of points
#         near_cutoff -- inclusive cutoff for distance between "near" points, Euclidean distance
# output: the nearby point's coordinates (x, y) if the given point is near a point in the point list, False if not
def near(point, point_list, near_cutoff):

    point_distance = lambda p1, p2: math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))  # Euclidean distance
    for p in point_list:
        if point_distance(point, p) <= near_cutoff:
            return p

    return False
