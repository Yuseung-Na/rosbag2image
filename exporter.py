#
# Module:       exporter.py
# Description:  ROS bag exporter
#
# Author:       Yuseung Na (ys.na0220@gmail.com)
# Version:      1.0
#
# Revision History
#       March 29, 2022: Yuseung Na, Created
#

import os
import argparse
import rosbag
from tqdm import tqdm
from bag_to_image import BagToImage

def main():
    ## Add parser
    parser = argparse.ArgumentParser(description="Extract data from ROS bag.")
    parser.add_argument(
        "--bag_file",
        help=".bag file path", 
        type=str, 
        required=True
    )
    parser.add_argument(
        "--output_dir",
        help="output image file path",
        type=str,
        default="/home/user/image"
    )
    parser.add_argument(
        "--image_topic",
        help="input image topic name",
        type=str,
        default="/image_raw"
    )
    parser.add_argument(
        "--file_type",
        help="output image file type",
        type=str,
        default="png"
    )
    args = parser.parse_args()

    ## Find all bag files
    bag_file_list = []    
    bag_file_path = os.path.realpath(args.bag_file)
    
    if os.path.isfile(bag_file_path) and bag_file_path[-4:] == ".bag":
        bag_file_list.append(bag_file_path)
    else:
        bag_file_list = [
            os.path.join(bag_file_path, f)
            for f in os.listdir(bag_file_path)
            if f[-4:] == ".bag"
        ]

    ## Sort bag files by file name
    bag_file_list.sort()
    print ("\nTotal number of bag files: {}\n".format(len(bag_file_list)))
    for f in bag_file_list:
        print (f)

    ## Converting process
    print("Converting process start!")
    for i, bag_file in enumerate(bag_file_list):
        ## Set output path
        out_path = os.path.join(args.output_dir, bag_file.split("/")[-1][:-4])
        
        ## Make BagToImage object
        b2i = BagToImage(args.image_topic, out_path)
        
        ## Write csv meta file header
        b2i.writeHeader()

        ## Open bag file
        try:
            bag = rosbag.Bag(bag_file, "r")
        except:
            print ("File path is wrong, {}".format(bag_file))
            continue

        ## Get topics from bag file
        msg_num = bag.get_message_count(args.image_topic)

        ## Convert current bag file
        print ("\nStart data parsing: {}\n".format(bag_file))
        for topic, msg, rostime in tqdm(bag.read_messages(topics=[args.image_topic]), total=msg_num):
            if topic == args.image_topic:
                b2i.processMsg(topic, msg, rostime, args.file_type)

        bag.close()
        del b2i
    
    print ("Converting process finished!")

if __name__ == "__main__":
    main()