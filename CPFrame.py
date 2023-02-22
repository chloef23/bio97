# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/7/22
# Bio97 Thesis Project
# CPFrame is an object that holds the data for each frame converted from a single .npy file

import numpy as np
from operator import itemgetter
from shapely.geometry import Point, Polygon, MultiPoint

class CPFrame:

    # outlines_list - list of the pixels contained within each cell outline
    # size - tuple of the number of (x, y) pixels in the image
    # frame_id - name of specific frame whose info is contained by this CPFrame, for later analysis
    # embryo_boundaries - coordinates of user-specified ROI in order [(left x, y), (right x, y)]
    # pix_to_id - 2D array mapping every pixel to the cell temp_id it belongs to
    def __init__(self, outlines_list, size, frame_id):
        self.outlines_list = outlines_list
        self.size = size
        self.frame_id = frame_id
        self.embryo_boundaries = []
        self.pix_to_id = self.create_pix_to_id()

    # creates a 2D array mapping every pixel to the cell temp_id it belongs to for later efficiency of access
    # output: 2D array of cell_temp_ids corresponding to the pixel they belong to, with (0,0) at top right,
    #         pixels with no corresponding cell are marked with -1
    def create_pix_to_id(self):
        ret_array = np.full(self.size, -1)

        for i in range(len(self.outlines_list)):
            for j in range(len(self.outlines_list[i])):
                x, y = self.outlines_list[i][j]
                ret_array[x, y] = i

        # uncomment to return cells that are completely filled in -- note, program will be considerably slower
        # ret_array = self.assign_pix_to_cells(ret_array)

        return ret_array

    # assigns every pixel within a cell to that cell in the outlines array
    # if a pixel is not located within a cell, it retains the -1 from the outlines array
    # input: outlines_array - 2D array containing pixels containing the outlines of cells marked by the cell_id (an
    #                         integer 0 to n) and pixels not containing any outline with -1
    # output 2D array where all pixels contained within a cell are marked by the cell_id
    def assign_pix_to_cells(self, outlines_array):
        k = 0
        min_max = self.get_cell_min_max()
        for cell in self.outlines_list:
            min = (min_max[k][0])
            max = (min_max[k][1])
            for i in range(min[0], max[0] + 1):     # min to max x coordinates
                for j in range(min[1], max[1] + 1):     # min to max y coordinates
                    poly = Polygon(cell)
                    point = Point(i,j)
                    if point.intersects(poly):
                        outlines_array[i,j] = k
            k += 1
        return outlines_array


    # returns the list of coordinates contained within each cell outline
    def get_outlines_list(self):
        return self.outlines_list

    # returns the list of coordinates associated with a temp_id
    # input: temp_id - the temp_id of the cell
    # output: list of coordinates associated with the temp_id
    def get_cell_coords(self, temp_id):
        return self.outlines_list[temp_id]

    # returns frame_id of the cp_frame
    # input: None
    # output: the frame_id of the cp_frame
    def get_frame_id(self):
        return self.frame_id

    # returns the minimum and maximum coordinates of a theoretical box around each cell
    # output: list of list of two tuples giving the top right and bottom left coordinates of the box
    #         for each cell in form [[(min x, min y), (max x, max y)]...]
    #         note: (0, 0) is at the top left
    def get_cell_min_max(self):
        min_max_list = []

        for cell in self.outlines_list:
            temp_list = []
            min_x = min(cell, key=itemgetter(0))[0]
            max_x = max(cell, key=itemgetter(0))[0]
            min_y = min(cell, key=itemgetter(1))[1]
            max_y = max(cell, key=itemgetter(1))[1]
            temp_list.append((min_x, min_y))
            temp_list.append((max_x, max_y))
            min_max_list.append(temp_list)

        return min_max_list

    # returns the cell containing a given coordinate
    # input: coord - an (x,y) tuple representing a coordinate
    # output: the integer temp_id of the cell containing that coordinate, or -1 if no such cell exists,
    #         or -2 if the coordinate is out of bounds
    def get_cell_from_coord(self, coord):

        # check that provided coordinate is in bounds
        if (coord[0] > self.size[0]) or (coord[1] > self.size[1]) or (coord[0] < 0) or (coord[1] < 0):
            return -2

        temp_id = self.pix_to_id[coord]    # will return the temp_id of the cell, or -1 is no cell exists at that coord

        return temp_id

    # sets the left and right embryo boundaries in the CPFrame
    # input: c1 - left (x,y) coordinates of bounding box
    #         c2 - right (x,y) coordinates of bounding box
    def set_boundaries(self, c1, c2):
        self.embryo_boundaries = [c1, c2]

    # checks that the provided x-coordinates of the bounding box are inside the user-specified ROI, returns boolean
    # input: c1 - left (x, y) coordinates of bounding box
    #         c2 - right (x, y) coordinates of bounding box
    # output: True if bounding box is inside ROI, False otherwise
    def check_boundaries(self, c1, c2):
        if c1[0] < self.embryo_boundaries[0][0] or c1[1] < self.embryo_boundaries[0][1]:  # part of bounding box is to left of ROI
            return False
        elif c2[0] > self.embryo_boundaries[1][0] or c2[1] > self.embryo_boundaries[1][1]:    # part of bounding box is to right of ROI
            return False
        else:
            return True

    # prints the CPFrame in a pretty way
    def print_cpframe(self, cell_temp_id=None):
        print("CPFrame " + str(self.frame_id) + " is size " + str((self.size[0] - 1, self.size[1] - 1)))

        i = 0
        if not cell_temp_id:
            for cell in self.outlines_list:
                print(i)
                i += 1
                for coord in cell:
                    print(coord, end=" ")
                print("")
            print("")
        else:
            print(cell_temp_id)
            for coord in self.outlines_list[cell_temp_id]:
                print(coord, end=" ")
            print("")

# unit testing
if __name__ == "__main__":
    # cell_temp_id = [0, 1, 2, 3, 4, 5]
    # outlines_list = [[[0,4],[1,4],[0,3],[1,3]],
    #                  [[2,4],[2,3],[3,4],[4,4]],
    #                  [[2,2],[3,2],[3,3],[4,2],[4,3]],
    #                  [[0,0],[0,1],[1,0],[1,1],[0,2],[1,2]],
    #                  [[2,0],[2,1],[3,0],[3,1],[4,0]],
    #                  [[4,1]]]
    # size = (5,5)
    #
    # cpframe = CPFrame(outlines_list, size, 1)

    cell_temp_id = [0, 1, 2, 3, 4, 5]
    outlines_list = [[[0,5],[1,5],[2,5],[0,6],[2,6]],
                    [[1,0],[0,1],[2,1],[0,2],[2,2],[0,3],[2,3],[1,4]],
                    [[2,0],[3,0],[4,0],[5,0],[3,1],[6,1],[3,2],[6,2],[3,3],[6,3],[4,4],[5,4]],
                    [[6,4],[3,5],[4,5],[5,5],[6,5],[3,6],[4,6],[5,6],[6,6]]]


    size = (7,7)

    cpframe = CPFrame(outlines_list, size, 2)

    print("Get map of cells:")
    print("Note: (0, 0) is at the top left, the x axis is vertical, and the y axis is horizontal")
    print(cpframe.create_pix_to_id())

    print("\nGet cell coordinates of cell number 2:")
    print(cpframe.get_cell_coords(2))

    print("\nGet the cell at coordinates (2,2):")
    print(cpframe.get_cell_from_coord((2,2)))

    print("\nPrint the CPFrame data structure:")
    cpframe.print_cpframe()

    print("\nPrint the CPFrame data structure of cell number 2:")
    cpframe.print_cpframe(cell_temp_id=2)

    print("\nGet the top left and bottom right coordinates of each cell:")
    print("Note: (0, 0) is at the top right")
    print(cpframe.get_cell_min_max())

    print("\nGet frame ID:")
    print(cpframe.get_frame_id())

