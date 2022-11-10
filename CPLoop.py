# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 11/8/22
# Bio97 Thesis Project
# Automation for running Cellpose on all images from a folder

# import packages
import argparse
import pathlib
import re
import os
import cv2
from PyQt5 import QtCore, QtWidgets
from cellpose import models, io
from cellpose import main as cp_main

PATH = "path"

def main(image_list, gpu_bool, start_z=0, end_z=None, switch_z=None, start_model="TN3", switch_model="TN2", pretrained=None):

    # user specifies if the GPU or CPU is used to run Cellpose
    if gpu_bool:
        gpu=True
    else:
        gpu=False

    # initiate Cellpose segmentation models
    model_cp_0 = models.Cellpose(gpu=gpu, model_type=start_model)      # primary model

    if switch_z:    # model to switch to at specified z, only if switch_z != None
        model_cp_1 = models.Cellpose(gpu=gpu, model_type=switch_model)

    if pretrained:      # if user wants to use pretrained (self-trained model)
        custom_cp = models.CellposeModel(gpu=True, pretrained_model=PATH)

    size_model = models.SizeModel(model_cp_0)
    diam, diam_style = size_model.eval(image_list)


# segments an image or list of images using Cellpose and saves it to a .npy file (and .png if png=True)
# please see Cellpose API documentation for specifics of cellpose.eval(), cellpose.io.masks_flows_to_seg and save_masks
# input: image_list - list of images (can be length 1) to segment
#        filename_list - list of desired filenames of saved .npy/.png files, in same order as image_list
#        cp_model - initialized Cellpose model
#        diameter - average diameter of cells calibrated through the SizeModel
#        png - boolean; if True, segmentation will be saved as .png and .npy, if false, it is only saved as a .npy
def segment_image(image_list, filename_list, cp_model, diameter=None, png=False):
    for i in range(len(image_list)):
        masks, flows, styles, diams = cp_model.eval(image_list[i])      # run Cellpose and get masks

        # wait for user key press to continue
        print("Press 'y' after manual correction to continue")
        k = cv2.waitKey(0) & 0xff

        if k == ord('y'):  # if 'ESC' is pressed
            # save segmentation as a .npy file
            npy_filename = filename_list[i] + ".npy"
            io.masks_flows_to_seg(image_list[i], masks, flows, diams, npy_filename)    # save as .npy

            # save segmentation as a .png file if png=True
            if png:
                png_filename = filename_list[i] + ".png"
                io.save_masks(image_list[i], masks, flows, png_filename, png=True)     # save as .png


# check that command line arguments are valid
# input: args - ArgumentParser-parsed command line arguments
# output: boolean - True if all arguments are valid, False if any are not
def check_args(args):
    ret = True
    z_max = 0
    t_max = 0
    model_list = ["cyto", "nuclei", "cyto2", "tissuenet", "TN1", "TN2", "TN3", "livecell",
                  "LC1", "LC2", "LC3", "LC4", "pretrained"]

    # check that file name is valid and get z_max and t_max
    for file in args.image_folder:
        if not re.match(r'.*\/?[z|Z]\d+[t|T]\d+$', file, re.I):  # check to see if file follows pattern PATH/Z001T001
            print("Error: File names do not match pattern PATH/Z__T__, where __ can be any number of integers")
            ret = False
        else:
            z, t = extract_zt(file)

            # find maximum z and t
            if z > z_max: z_max = z
            if t > t_max: t_max = t

    # check that layer to start segmentation on (switch_z) is positive and not greater than the number of z layers in the stack
    if args.s and args.s < 0 or args.s > z_max:
        print("Error: start_z must be be greater than 0 and less than the maximum z value")
        ret = False
    # check that layer to end segmentation on (end_z) is positive and not greater than the number of z layers in the stack
    if args.e and args.e < 0 or args.z > z_max:
        print("Error: end_z must be be greater than 0 and less than the maximum z value")
        ret = False
    # check that layer to switch segmentation model on (switch_z) is positive and not greater than the number of z layers in the stack
    if args.w and args.w < 0 or args.w > z_max:
        print("Error: switch_z must be be greater than 0 and less than the maximum z value")
        ret = False
    # check that first (or only) model has a valid model name
    if args.sm and args.sm not in model_list:
        print("Error: start_model is not a valid model. Must be one of: [cyto, nuclei, cyto2, tissuenet, TN1, TN2, TN3,"
              "livecell, LC1, LC2, LC3, LC4, pretrained]")
        ret = False
    # check that switch model has a valid model name
    if args.sw and args.sw not in model_list:
        print("Error: switch_model is not a valid model. Must be one of: [cyto, nuclei, cyto2, tissuenet, TN1, TN2,"
              "TN3, livecell, LC1, LC2, LC3, LC4, pretrained]")
        ret = False
    # check if pretrained PATH gives a valid file
    if args.p and not os.path.isfile(args.p):
        print("Error: pretrained model is not a valid file")
        ret = False

    return ret


# extracts the form z__t__ from a file PATH, where __ represent any number of integers
# note: assumes that the PATH has already been checked for valid syntax using r'.*\/?[z|Z]\d+[t|T]\d+$' or similar
# input: file_path - PATH to file
# output: filename - z__t__ form of the filename
def extract_ztname(file_path):
    file_path.lower()  # make file lowercase
    zt_form = re.match(r'z\d+t\d+$', file_path)

    return zt_form


# extracts the z and t integers from the file PATH (ex. z = 01 and t = 04 extracted from input PATH/z01t04)
# note: assumes that the PATH has already been checked for valid syntax using r'.*\/?[z|Z]\d+[t|T]\d+$' or similar
# input: file_path - PATH to file
# output: z, t - integers representing the t and z layers of the file
def extract_zt(file_path):
    zt_form = extract_ztname(file_path)
    z, t = re.split(r'[zt]', str(zt_form))

    return z, t


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    # define command line arguments
    parser.add_argument("image_folder", help="PATH to folder containing all images to segment using Cellpose")
    parser.add_argument("-g", "--gpu", help="use GPU to run Cellpose", action="store_true")
    parser.add_argument("-s", "--start_z", help="z stack layer to start segmentation on (inclusive)", type=int)
    parser.add_argument("-e", "--end_z", help="z stack layer to finish segmentation on (inclusive)", type=int)
    parser.add_argument("-w", "--switch_z", help="z stack layer on which to switch segmentation model", type=int)
    parser.add_argument("-sm", "--start_model", help="first (or only) model with which to segment images,"
                                                     "if pretrained type 'pretrained'")
    parser.add_argument("-sw", "--switch_model", help="model with which to segment images after switch, "
                                                      "if pretrained use 'pretrained'")
    parser.add_argument("-p", "--pretrained", help="PATH to pretrained model", type=pathlib.Path)

    # parse command line arguments
    args = parser.parse_args()
    if not check_args(args):
        exit()

    cp_main()  # start Cellpose and GUI