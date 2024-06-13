## CPTracker
Work-in-progress.  
A cell tracking program that interfaces with [Cellpose](https://github.com/MouseLand/cellpose) .npy output files.  

Converts Cellpose .npy files to a .mp4 video, then uses a OpenCV2-based tracker to
track the cells across time and the z-axis. CPTracker automatically selects cells
to be tracked based on their boundaries. The tracker links information about a cell together across
the z axis and time so calculations can be performed on each cell.

### Structure
- main.py: executes the CPTracker program, the user inputs the name of the folder 
containing the .npy images
- load_npy.py: converts all .npy files in the user-inputted folder to .png images
- frames_to_video: converts the .png images to a .mp4 file
- tracker.py: using the .mp4 file, selects cells in frame, uses the CSRT tracking
algorithm to track cells across one video (either time or z)
- CPFrame.py: data structure to hold the cell information from every .npy file
