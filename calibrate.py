#!/usr/bin/env python
import numpy as np
import cv2
import os
import argparse
import yaml
import pickle
from glob import glob
from cv2 import __version__
__version__

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calibrate camera using a video of a chessboard or a sequence of images.')
    parser.add_argument('input', help='input video file or glob mask')
    parser.add_argument('out', help='output calibration yaml file')
    args = parser.parse_args()


    if '*' in args.input:
        source = glob(args.input)
    else:
        source = cv2.VideoCapture(args.input)

    if( source.isOpened() ):
        print ('is Open ')    
    else :
        print( 'not open' )

    print( args.input )
    print( args.out )

    pattern_size = (7, 5)
    pattern_points = np.zeros((np.prod(pattern_size), 3), np.float32)
    pattern_points[:, :2] = np.indices(pattern_size).T.reshape(-1, 2)
    # pattern_points *= square_size

    obj_points = []
    img_points = []
    h, w = 0, 0
    i = -1
    while True:
        i += 1
        if isinstance(source, list):
            # glob
            if i == len(source):
                break
            img = cv2.imread(source[i])
            print( img )
        else:
            # cv2.VideoCapture
            
            retval, img = source.read()
            print ( retval )
            if not retval:
                break
            if i % args.framestep != 0:
                continue

        print('Searching for chessboard in frame ' + str(i) + '...'),
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = img.shape[:2]
        found, corners = cv2.findChessboardCorners(img, pattern_size, cv2.CALIB_CB_FILTER_QUADS)
        if found:
            term = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 0.1)
            cv2.cornerSubPix(img, corners, (5, 5), (-1, -1), term)
        if args.debug_dir:
            img_chess = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            cv2.drawChessboardCorners(img_chess, pattern_size, corners, found)
            cv2.imwrite(os.path.join(args.debug_dir, '%04d.png' % i), img_chess)
        if not found:
            print ('not found')
            continue
        img_points.append(corners.reshape(1, -1, 2))
        obj_points.append(pattern_points.reshape(1, -1, 3))

        print ('ok')

    if args.corners:
        with open(args.corners, 'wb') as fw:
            pickle.dump(img_points, fw)
            pickle.dump(obj_points, fw)
            pickle.dump((w, h), fw)

    
    print('\nPerforming calibration...')
    rms, camera_matrix, dist_coefs, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, (w, h), None, None)
    print ("RMS:", rms)
    print ("camera matrix:\n", camera_matrix)
    print ("distortion coefficients: ", dist_coefs.ravel())

    calibration = {'rms': rms, 'camera_matrix': camera_matrix.tolist(), 'dist_coefs': dist_coefs.tolist() }
    with open(args.out, 'w') as fw:
        yaml.dump(calibration, fw)
