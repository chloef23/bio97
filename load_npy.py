# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 9/28/22
# Bio97 Thesis Project
# Load .npy files outputted by Cellpose (by MouseLand, https://github.com/MouseLand/cellpose)
# Code modified from code in Cellpose documentation (https://cellpose.readthedocs.io/en/latest/outputs.html#seg-npy-output)

# import packages
import numpy as np
from matplotlib import pyplot as plt
import cv2

# loads a .npy file and saves a PNG with cell boundary outlines shown as a red line, outputs name of file
# note: this function will override any files named [file_name].png
# inputs: file_name - the name of the .npy file
#         print_file - boolean, defaults to false, prints the text of the .npy file if true
#         show_plot - boolean, defaults to false, displays the matplotlib plot if true
#                     note: if show_plot is True, the saved image will be blank
# output: png_name - name of the file containing the PNG

def load(file_name, print_file=False, show_plot=False):
    # load numpy file
    file = np.load(file_name, allow_pickle=True).item()
    if print_file:
        print(file)

    # get list of pixels containing the outlines from file
    outlines = outlines_list(file['masks'])
    plt.imshow(file['img'])
    for o in outlines:
        plt.plot(o[:, 0], o[:, 1], color='r')
    if show_plot:      # note: if show_plot is True, saved file will be blank
        plt.show()

    # save plot as PNG
    png_name = file_name + ".png"
    plt.savefig(png_name)

    # clear the figure from the plot
    plt.clf()

    # return the name of the saved PNG
    return png_name

# code from Cellpose documentation, gets the outlines of cells and returns them as a list for plotting
# input: list of masks from the .npy file (file['masks'])
# output: list of the pixels in the masks

def outlines_list(masks):
    outpix=[]
    for n in np.unique(masks)[1:]:
        mn = masks==n
        if mn.sum() > 0:
            contours = cv2.findContours(mn.astype(np.uint8), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
            contours = contours[-2]
            cmax = np.argmax([c.shape[0] for c in contours])
            pix = contours[cmax].astype(int).squeeze()
            if len(pix)>4:
                outpix.append(pix)
            else:
                outpix.append(np.zeros((0,2)))
    return outpix

# unit testing
if __name__ == "__main__":
    # .npy file
    FILE = ".npy test_1/20220428_ECadGFP_02-z1-50t10034_seg.npy"

    load(FILE, show_plot=False)     # if show_plot is true, saved file will be blank
