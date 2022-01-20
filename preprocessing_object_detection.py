"""
preprocessing_object_detection.py

This script:
    - Reads all images and corrects filenames:
        -[ Removes any unnecesaary "." in file name and replaces it with "_"]
        -[Changes file extensions to lower case. Eg: .JPG -> .jpg ]
    - Convert HEIC / heic file format to jpg.
    - Identifies missing XML Files
    - Ensures XML file name matches with corresponding image file. 
    
Created by : Ashish John Stanley
Created Date : 17rd January
Updated : 17th January

Usage : -i /Users/ashishjohnstanley/utils/PreProcessing/5thJan22-FasterRCNNTestResults/Image_GroundTruth/test -x /Users/ashishjohnstanley/utils/PreProcessing/5thJan22-FasterRCNNTestResults/Image_GroundTruth/test -o /Users/ashishjohnstanley/utils/PreProcessing/Results

Future Improvement :
    - 
"""


import os
import pathlib

import argparse

import shutil
import subprocess

ap = argparse.ArgumentParser()

ap.add_argument('-i','--input_image_dir', required=True, help="Input (Root) Directory which contains the input images")
ap.add_argument('-x','--input_xml_dir', required=True, help="Input (Root) Directory which contains the ground truth annotations")
ap.add_argument('-o','--output_dir', required=True, help="Output Directory to store Results. ")

args = vars(ap.parse_args()) 

INPUT_IMAGE_DIR = os.path.abspath(args['input_image_dir'])
INPUT_XML_DIR = os.path.abspath(args['input_xml_dir'])
OUTPUT_DIR = os.path.abspath(args['output_dir'])



# Sanity Check to ensure that the Input Source FolderS exist:
if pathlib.Path(INPUT_IMAGE_DIR).exists() and pathlib.Path(INPUT_IMAGE_DIR).is_dir():
    print("[INFO] Input image directory valid")
else:
    print("[ERROR] INPUT_IMG_DIR does not exist!")
if pathlib.Path(INPUT_XML_DIR).exists() and pathlib.Path(INPUT_XML_DIR).is_dir():
    print("[INFO] INPUT_XML_DIR valid")
else:
    print("[ERROR] INPUT_XML_DIR does not exist!")
if pathlib.Path(OUTPUT_DIR).exists() and pathlib.Path(OUTPUT_DIR).is_dir():
    print("[INFO] OUTPUT_DIR valid")
else:
    print("[ERROR] OUTPUT_DIR does not exist!")


#Creating list of acceptable images
acceptable_image_extensions =(".png", ".jpg", ".jpeg", ".heic")
image_paths=[]
for root, dirs, files in os.walk(INPUT_IMAGE_DIR, topdown=True):  

    for file_name in files:
        # Skip if the files i .DS_Store. This is specific to Mac OS
        if file_name == ".DS_Store":
            continue
        #if file_name.lower().endswith(acceptable_video_extensions):
        if file_name.lower().endswith(acceptable_image_extensions):
            ith_file_path = os.path.abspath(os.path.join(root, file_name))
            #print(ith_file_path)
            image_paths.append(ith_file_path)


print("Number of images:", len(image_paths))
for i in image_paths:

    basename_image = os.path.basename(i)
    basename=os.path.splitext(basename_image)

    #Get extension of file image:
    extension = basename[1]

    #Convert all extensions to lowercases:
    if basename[1].isupper():
        extension = basename[1].lower()
    

    #Replace all unnecessary "." with "_":
    new_basename = basename[0].replace(".","_")
    newname_image = os.path.join(OUTPUT_DIR , new_basename+extension)


    #Get XML file for corresponding Image:
    xml_file = os.path.join(INPUT_XML_DIR, basename[0]+".xml")

    #Check if XML files exists for coresponding image:
    if os.path.isfile(xml_file):
        #Correct xml file name based on new_basename- 
        newname_xml = os.path.join(OUTPUT_DIR, new_basename+".xml")

        #Copy XML file into results directory:
        dest1 = shutil.copy(xml_file,newname_xml)
        #Copy Image file into resuts directory:

        if extension == ".heic":
            # [Delay comment] Assigning x to store result from subprocess.call to stall script to wait for conversion to complete. 
            x = subprocess.call(['heic2jpg', '--keep',"--src", i])
            converted_image = os.path.join(INPUT_IMAGE_DIR , new_basename + ".jpg" )
            newname_image= os.path.join(OUTPUT_DIR, new_basename + ".jpg")
            dest = shutil.move(converted_image, newname_image)
        else:
            dest = shutil.copy(i, newname_image)
    else:
        print("[ERROR] - XML file for {} not found.".format(basename_image))


    




