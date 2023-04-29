# Chloe Fugle (chloe.m.fugle.23@dartmouth.edu)
# 4/15/2023
# Bio97 Thesis Project
# Analyzes .csv output from CPTracker

import pandas as pd
import numpy as np
import os

########################################################################################################################
FILE_PATH = "20230324_0010_npys/__CPTracker_folder__/cptracker_output_run1.csv"      # PATH to .csv outputted from CPTracker
OUTPUT_PATH = "20230324_0010_npys/__CPTracker_folder__/cptracker_summary.csv"   # PATH to desired output file
TVALUE = [1, 5, 10, 15, 20, 25, 27]         # list of t-values of interest for z-tracking (likely same as from CPTracker)

########################################################################################################################

# get the minimum and maximum t that was tracked as well as the range of z values tracked for each t
# input:
# output:
def analyze_data(file_path, output_path):

    # check that provided path exists and is a .csv file
    if not os.path.isfile(file_path):
        print("Error: file" + str(file_path) + "could not be found")
        return -1
    elif os.path.splitext(file_path)[1] != ".csv":
        print("Error: file" + str(file_path) + "is not of form .csv")
        return -1

    # open file for writing
    # if os.path.exists(output_path) or os.path.isfile(output_path):
    #     print("Error: ouput file already exists! Please rename the file or change the desired path to "
    #           "avoid rewriting the file")
    #     return -1
    fp = open(output_path, "w")

    data_df = pd.read_csv(file_path, names=["cell", "x", "y", "z", "t"])

    # process the data
    try:
        # get the minimum and maximum t for each cell
        t_max = data_df.loc[data_df.groupby('cell')['t'].idxmax()]
        t_max_name = t_max[["cell", "t"]]
        t_max_name.columns = ["cell", "t_max"]

        t_min = data_df.loc[data_df.groupby('cell')['t'].idxmin()]
        t_min_name = t_min[["cell", "t"]]
        t_min_name.columns = ["cell", "t_min"]

        t_merge = pd.merge(t_min_name, t_max_name, on='cell')

        # get z range (z max - z min) for each timepoint
        z_t_group = data_df[data_df['t'].isin(TVALUE)]
        min_z = z_t_group.loc[z_t_group.groupby(['cell', 't'])['z'].idxmin()]
        z_min_name = min_z[["cell", "z", "t"]]
        z_min_name.columns = ["cell", "z_min", "t"]

        z_t_group = data_df[data_df['t'].isin(TVALUE)]
        max_z = z_t_group.loc[z_t_group.groupby(['cell', 't'])['z'].idxmax()]
        z_max_name = max_z[["cell", "z", "t"]]
        z_max_name.columns = ["cell", "z_max", "t"]

        min_max_merge = pd.merge(z_min_name, z_max_name, on=['t', 'cell'])
        min_max_merge['diff'] = min_max_merge['z_max'] - min_max_merge['z_min']
        print(min_max_merge)
        z_min_max = min_max_merge[['cell', 't', 'diff']]

    except:
        print("Error: unable to read file. Please check that it is the output from CPTracker")

    else:       # output summary data as file

        print(z_min_max)
        print(t_merge)
        # get list of all cell ids
        d_cell_list = np.concatenate((pd.Series.unique(t_merge['cell']), pd.Series.unique(z_min_max['cell'])))
        cell_list = np.unique(d_cell_list)

        for cell in cell_list:
            cell_z = z_min_max[z_min_max['cell'] == cell]
            cell_t = t_merge[t_merge['cell'] == cell]

            # get the range of the cell over z for each t
            t_string = ""
            for t in np.unique(cell_z['t']):
                diff = cell_z[cell_z['t'] == t]['diff'].to_string().split()[1]
                t_string += (str(t) + ":" + str(diff) + ", ")
            t_string = t_string[:-2]

            # get the range over t
            t_min = cell_t['t_min'].to_string().split()[1]
            t_max = cell_t['t_max'].to_string().split()[1]

            fp.write(str(cell) + ", " + str(t_min) + ", " + str(t_max) + ", " + t_string + "\n")

    finally:
        fp.close()


# run the analysis
if __name__ == "__main__":
    analyze_data(FILE_PATH, OUTPUT_PATH)


