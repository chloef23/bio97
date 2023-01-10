# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/31/22
# Bio97 Thesis Project
# Wrapper class for CPTracker that connects the CPFrames across all frames and videos

class FrameConnector:

    # cell_dict_list - list of cell dictionaries, dictionaries are of each cell's coordinates, key is frame ID
    #                  note: global cell IDs are assigned from cells present in the first frame of the time
    #                  (z-constant) video
    def __init__(self):
        self.cell_dict_list = []

    # creates a dictionary for each global cell_id if not already created, then adds the cell coordinates to
    # the dictionary with the key as the frame_id
    # note: in the first frame when this is called, cells must be passed in in the order of their cell-ids
    # input: cell_id - the global cell id, must be an integer >= 0
    #        frame_id - the id of the video frame, recommended that it is in form zx_tx
    #        coords - list of the coordinates of the cells in the frame
    def add_frame(self, cell_id, frame_id, coords):
        if cell_id > (len(self.cell_dict_list) - 1):      # if global cell_id not already in dictionary
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

    # prints the FrameConnector dictionary in a pretty way
    def print_FC(self):
        cell_id = 0
        for i in self.cell_dict_list:
            print("cell_id " + str(cell_id) + ": " + str(i))
            cell_id += 1


# unit testing
if __name__ == "__main__":

    frame_connector = FrameConnector()

    print("\nAdd a cell (ID = 0) to an empty FrameConnector structure:")
    frame_connector.add_frame(1, "test_frame_00", [(0,0), (0,1)])
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
