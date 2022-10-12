# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/7/22
# Bio97 Thesis Project
# CPFrame is an object that hold the data for each frame converted from a single .npy file

import numpy as np
from operator import itemgetter

class CPFrame:

    # cell_temp_id - list of all the cell temp_ids
    # outlines_list - list of the pixels contained within the outline, in the same order as the cell temp)id list
    # size - tuple of the number of (x, y) pixels in the image
    def __init__(self, cell_temp_id_list, outlines_list, size, frame_id):
        self.cell_temp_id = cell_temp_id_list
        self.outlines_list = outlines_list
        self.size = size
        self.frame_id = frame_id
        # self.pix_to_id = self.create_pix_to_id(cell_temp_id, outlines_list, size)

    # creates a 2D array mapping every pixel to the cell temp_if it belongs to for later efficiency of access
    # output: 2D array of cell_temp_ids corresponding to the pixel they belong to, with (0,0) at lower left,
    #         pixels with no corresponding cell are marked with -1
    def create_pix_to_id(self):
        ret_array = np.full(size, -1)

        for i in range(len(self.cell_temp_id)):
            for j in range(len(self.outlines_list[i])):
                x, y = self.outlines_list[i][j]
                # convert grid to (0,0) at bottom left using formula (x,y) -> (y, x_max - 1 - x)
                ret_array[self.size[0]-1-y,x] = self.cell_temp_id[i]

        return ret_array

    # returns the list of coordinates associated with a temp_id
    # input: temp_id - the temp_id of the cell
    # output: list of coordinates associated with the temp_id
    def get_cell_coords(self, temp_id):
        return self.outlines_list[temp_id]

    # returns the minimum and maxiumum coordinates of a theoretical box around each cell
    # output: list of list of two tuples giving the top right and bottom left coordinates of the box
    #         for each cell in form [[(min x, max y), (max x, min y)]...]
    def get_cell_min_max(self):
        min_max_list = []

        for cell in self.outlines_list:
            temp_list = []
            min_x = min(cell, key=itemgetter(0))[0]
            max_x = max(cell, key=itemgetter(0))[0]
            min_y = min(cell, key=itemgetter(1))[1]
            max_y = max(cell, key=itemgetter(1))[1]
            temp_list.append((min_x, max_y))
            temp_list.append((max_x, min_y))
            min_max_list.append(temp_list)

        return min_max_list

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
    cell_temp_id = [0, 1, 2, 3, 4]
    outlines_list = [[[0,4],[1,4],[0,3],[1,3]],
                     [[2,4],[2,3],[3,4],[4,4]],
                     [[2,2],[3,2],[3,3],[4,2],[4,3]],
                     [[0,0],[0,1],[1,0],[1,1],[0,2],[1,2]],
                     [[2,0],[2,1],[3,0],[3,1],[4,0],[4,1]]]
    size = (5,5)

    cpframe = CPFrame(cell_temp_id, outlines_list, size, 1)

    print("Get map of cells:")
    print(cpframe.create_pix_to_id())

    print("\nGet cell coordinates of cell number 2:")
    print(cpframe.get_cell_coords(2))

    print("\nPrint the CPFrame data structure:")
    cpframe.print_cpframe()

    print("\nPrint the CPFrame data structure of cell number 2:")
    cpframe.print_cpframe(cell_temp_id=2)

    print("\nGet the top left and bottom right coordinates of each cell:")
    print(cpframe.get_cell_min_max())

