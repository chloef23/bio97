# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 10/31/22
# Bio97 Thesis Project
# Wrapper class for CPTracker that connects the CPFrames across all frames and videos

class FrameConnector:

    # cell_dict_list - list of cell dictionaries, dictionaries are of each cell's coordinates, key is frame ID
    #                  note: global cell IDs are assigned from cells present in the time (z-constant) video
    def __init__(self):
        self.cell_dict_list = []

    # creates a dictionary for each global cell_id if not already created, then adds the cell coordinates to
    # the dictionary with the key as the frame_id
    # note: in the first frame when this is called, cells must be passed in in the order of their cell-ids
    # input: cell_id - the global cell id, must be an integer >= 0
    #        frame_id - the id of the video frame, recommended that it is in form zx_tx
    #        coords - list of the coordinates of the cell at the frame
    def add_frame(self, cell_id, frame_id, coords):
        if cell_id > len(self.cell_dict_list):      # if global cell_id not already
            temp_dict = {}
            temp_dict[frame_id] = coords
            self.cell_dict_list.append(temp_dict)
        else:
            temp_dict = self.cell_dict_list[cell_id]
            temp_dict[frame_id] = coords


