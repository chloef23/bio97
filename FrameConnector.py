# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/31/22
# Bio97 Thesis Project
# Wrapper class for CPTracker that connects the CPFrames across all frames and videos

import matplotlib.pyplot as plt
import numpy as np
import os

class FrameConnector:

    # cell_dict_list - list of cell dictionaries, dictionaries are of each cell's coordinates, key is frame ID
    #                  note: global cell IDs are assigned from cells present in the first frame of the time
    #                  (z-constant) video
    # first_vid_list - list of the center coordinates of each cell in the first video
    def __init__(self):
        self.cell_dict_list = []
        self.first_vid_list = []

    # creates a dictionary for each global cell_id if not already created, then adds the cell coordinates to
    # the dictionary with the key as the frame_id
    # note: in the first frame when this is called, cells must be passed in in the order of their cell_ids
    # input: cell_id - the global cell id, must be an integer >= 0
    #        frame_id - the ID of the video frame, recommended that it is in form zx_tx
    #        coords - list of the coordinates of the cells in the frame
    def add_cell(self, cell_id, frame_id, coords):
        if cell_id > (len(self.cell_dict_list) - 1):  # if global cell_id not already in dictionary
            temp_dict = {}
            temp_dict[frame_id] = coords
            self.cell_dict_list.append(temp_dict)
        else:
            temp_dict = self.cell_dict_list[cell_id]
            temp_dict[frame_id] = coords

    # retrieves the coordinates corresponding to a cell and frame, if given
    # inputs: cell_id - the global ID of a given cell
    #         frame_id - defaults to None, the ID for a given frame
    # output: if both cell_id and frame_id are valid, returns a list of coordinates
    #         if frame_id is present but invalid, returns -2
    #         if cell_id is valid and frame_id is None, returns a 2D list of coordinates labelled by frame
    #         if cell_id is invalid and frame_id is None, returns -1
    def retrieve_frame_info(self, cell_id, frame_id=None):
        frame = None

        # check that cell_id and frame_id are valid inputs
        # returns -1 if the cell_id is not valid and -2 is the frame_id is not valid
        if (cell_id < len(self.cell_dict_list)) and (cell_id > 0):
            cell = self.cell_dict_list[cell_id]
        else:
            return -1
        if frame_id:
            if frame_id in self.cell_dict_list[cell_id]:
                frame = self.cell_dict_list[cell_id][frame_id]
        else:
            return -2

        # fetch given cell coordinates from dictionary and given frame, if applicable
        if frame:
            ret = frame
        elif cell:
            ret = cell
        else:
            ret = -3

        return ret

    # returns the coordinates of all cells at a given frame ID
    # input: frame_id - the frame_id to return cells from
    # output: coords_list - the list of the coordinates of each cell in that frame, in order of their global_id
    #         note: appends -1 to the list if the cell is not present in the frame_id
    def get_cells_in_frame(self, frame_id):
        coords_list = []
        for cell in self.cell_dict_list:
            if frame_id in cell:
                coords_list.append(cell[frame_id])
            # else:
            #     coords_list.append(-1)

        return coords_list

    # returns the entire cell dictionary list structure
    # inputs: None
    # output: returns the entire cell dictionary list structure
    def get_dict_list(self):
        return self.cell_dict_list

    # returns if the FrameConnector object is empty or not
    # inputs: None
    # output: returns True if the object is empty, False if not
    def is_empty(self):
        if len(self.cell_dict_list) == 0:
            return True
        else:
            return False

    # returns the first video cell center list
    # inputs: None
    # output: the first video cell center list in form [[cell 0 center coord], [cell 1 center coord] ... ]
    def get_first_vid_list(self):
        return self.first_vid_list

    # set the first video cell center list
    # inputs: first-vid_list - the first video cell center list in form [[cell 0 center coord], [cell 1 center coord] ... ]
    # output: None
    def set_first_vid_list(self, first_vid_list):
        self.first_vid_list = first_vid_list

    # prints the FrameConnector dictionaries in a pretty way
    def print_FC(self):
        cell_id = 0
        for i in self.cell_dict_list:
            print("cell_id " + str(cell_id) + ": " + str(i))
            cell_id += 1

    # print the FrameConnector dictionaries in a pretty way, without all the cell coordinates
    def print_FC_simple(self):
        cell_id = 0
        for i in self.cell_dict_list:
            print("cell_id " + str(cell_id) + ": " + str(i.keys()))
            cell_id += 1

    # plot the cells in the FrameConnector dictionaries
    # each cell is one color, and each time point is a different point marker (up to 5 unique timepoints)
    # input - array_num - if the cell dictionaries contain multiple values, user can input the desired one
    # output - plot of the cells in the FrameConnector dictionaries
    def plot_cells(self, array_num=None):

        # for each cell in the cell dictionary list
        for i in range(len(self.cell_dict_list)):
            c = np.random.rand(3,)

            # for each frame the cell is in
            for frame, coords in self.cell_dict_list[i].items():
                if array_num:
                    coords_arr = np.array(coords[array_num])
                else:
                    coords_arr = np.array(coords)
                x, y = coords_arr.T
                plt.scatter(x, y, color=c, s=1)


        plt.show()
        plt.cla()


# unit testing
if __name__ == "__main__":
    frame_connector = FrameConnector()

    print("\nAdd a cell (ID = 0) to an empty FrameConnector structure:")
    frame_connector.add_frame(1, "test_frame_00", [(0, 0), (0, 1)])
    frame_connector.print_FC()

    print("\nAdd a cell (ID = 1) to a FrameConnector structure:")
    frame_connector.add_frame(1, "test_frame_00", [(1, 2), (1, 1)])
    frame_connector.print_FC()

    print("\nAdd new frame to existing cell")
    frame_connector.add_frame(1, "test_frame_01", [(2, 2), (2, 1)])
    frame_connector.print_FC()

    print("\nRewrite existing cell (ID = 0) coordinates at existing frame (test_frame_00):")
    frame_connector.add_frame(0, "test_frame_00", [(2, 0), (2, 1)])
    frame_connector.print_FC()

    print("\nTest retrieving coordinates of valid cell (1) at valid frame (test_frame_00):")
    print(frame_connector.retrieve_frame_info(1, "test_frame_00"))

    print("\nTest retrieving coordinates of valid cell (1) at invalid frame (test_frame_iv):")
    print(frame_connector.retrieve_frame_info(1, "test_frame_iv"))

    print("\nTest retrieving coordinates of valid cell (1) with no frame:")
    print(frame_connector.retrieve_frame_info(1))

    print("\nTest retrieving coordinates of an invalid cell (5) with no frame:")
    print(frame_connector.retrieve_frame_info(5))

    print("\nTest retrieving coordinates of an invalid cell (5) with an invalid frame (test_frame_iv):")
    print(frame_connector.retrieve_frame_info(5, "test_frame_iv"))

    print("\nTest retrieving coordinates of a valid frame (test_frame_00):")
    print(frame_connector.get_cells_in_frame("test_frame_00"))

    print("\nTest retrieving coordinates of an invalid frame (test_frame_iv):")
    print(frame_connector.get_cells_in_frame("test_frame_iv"))

    print("\nSimple FrameConnector print:")
    print(frame_connector.print_FC_simple())

    print("Plot cells on graph:")
    print(frame_connector.plot_cells())
