## About ##

This code is about .bag (ROS bag) to .png or .jpg (image) converting tool.  
You can convert all the .bag files (sorted in ascending order by file name) in the directory.  

## How to use ##
### 1. Install python libraries ###
`$ pip install numpy`  
`$ pip install argparse`  
`$ pip install tqdm`  
(to be updated...)

### 2. Launch python file ###
`$ python exporter.py --bag_file={path of input ROS bag file directory} --output_dir={path of output image file directory} --type={type of output image (png, jpg)}`

#### Parameters ####
|Name|Description|Default value|
|:---|:---|:---|
|bag_file|.bag file path|"/home/user/rosbag"|
|bin_path|.png/.jpg file path|"/home/user/image"|
|file_name|image file type|"png"|
