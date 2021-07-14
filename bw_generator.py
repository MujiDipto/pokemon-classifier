"""
@author: Mujibul Islam Dipto
This script visits a list of directories containing images and converts the images from color to 
greyscale (to one channel)
"""

import math
import os
import cv2
import sys
from shutil import copyfile

# check usage
if len(sys.argv) != 2:
    sys.exit("Usage: python3 bw_generator.py directory_name")


# cd into the dataset directory
os.chdir(sys.argv[1])
dirs = os.listdir()
if ".DS_Store" in dirs:
    dirs.remove(".DS_Store")


for d in dirs:
    # cd into directory of each pokemon
    os.chdir(d)
    print("Currently in directory:", d)
    print("Files in this directory:", os.listdir())
    print("/n")
    # get the list of images
    images = os.listdir()

    # only iterate through 15% of the list
    n = math.floor(len(images) * 0.15)
    
    for i in range(n):
        img_file = images[i]
        img = cv2.imread(img_file)
        
        # only convert colored images to greyscale
        if len(img.shape) > 2:
            grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        filename =  "gs_" + str(img_file) + ".jpg"
        cv2.imwrite(filename, grey_img)

    os.chdir("../")
