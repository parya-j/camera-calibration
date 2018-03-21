#!/usr/bin/env python
import numpy as np
import cv2
import os
import argparse
import yaml
from glob import glob

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Undistort images based on camera calibration.')
    parser.add_argument('calibration', help='camera parameters file')
    parser.add_argument('input_directory', help='input directory')
    parser.add_argument('out', help='output directory')
    args = parser.parse_args()
    
    with open(args.calibration) as fr:
        c = yaml.load(fr)
    files = glob(args.input_directory +'/*.jpg')
    for fn in files:
        print ('processing %s...' % fn),
        img = cv2.imread(fn)
        if img is None:
            print("Failed to load " + fn)
            continue

        K_undistort = np.array(c['camera_matrix'])
        img_und = cv2.undistort(img, np.array(c['camera_matrix']), np.array(c['dist_coefs']),
                                newCameraMatrix=K_undistort)
                                name, ext = os.path.splitext(os.path.basename(fn))
cv2.imwrite(os.path.join(args.out, name + '_und' + ext), img_und)

print ('ok')

