# camera-calibration
find the camera parameters (calibrate.py)
and remove the distortion from images (undistorted.py)

```
python calibrate.py ./example_calibration/input/chessboard.avi ./example_calibration/output/parameters.yaml

```

```
python undistorted.py ./example_undistortion/input/parameters.yaml ./example_undistortion/input ./example_undistortion/output

```
