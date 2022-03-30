#
# Module:       bag_to_image.py
# Description:  ROS bag exporter to image
#
# Author:       Yuseung Na (ys.na0220@gmail.com)
# Version:      1.0
#
# Revision History
#       March 29, 2022: Yuseung Na, Created
#

import os
import argparse
import csv
import cv2
import rosbag
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class BagToImage:
    def __init__(self, image_topic, output_dir):
        ## Set path
        self.root_dir = output_dir
        self.images_dir = os.path.join(self.root_dir, "images")
        
        ## Make directories
        try:
            if not (os.path.isdir(self.root_dir)):
                os.makedirs(os.path.join(self.root_dir))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print ("Failed to create directory!!!!!")
                raise     
                   
        try:
            if not (os.path.isdir(self.images_dir)):
                os.makedirs(os.path.join(self.images_dir))
        except OSError as e:
            if e.errno != errno.EEXIST:
                print ("Failed to create directory!!!!!")
                raise
        
        ## Set image topic properties
        self.image_topic = image_topic
        self.bridge = CvBridge()
        
        ## Set metadata properties
        self.seq = 0
        self.csv_file_path = os.path.join(self.root_dir, "meta.csv")
        self.csv_file = open(self.csv_file_path, "wb")
        self.meta_file = csv.writer(self.csv_file, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL)

    def processMsg(self, topic, msg, rostime, file_type):
        ## Set image encoding type
        cv_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
                
        ## Set image file name
        file_name = "{:05d}.{type}".format(self.seq, type=file_type)
        
        ## Save image
        cv2.imwrite(os.path.join(self.images_dir, file_name), cv_img)

        ## Write csv meta file
        self.meta_file.writerow([self.seq, rostime.to_sec(), file_name])
        
        self.seq += 1

    def writeHeader(self):
        ## Write csv meta file header
        self.meta_file.writerow(            
            ["sequence", "ros time [sec]", "file name"]
        )

    def __del__(self):
        self.csv_file.close()