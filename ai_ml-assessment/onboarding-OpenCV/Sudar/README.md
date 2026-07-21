# Week 2 - embedUR | Structured Training Program (AI & ML)

## Overview

This week's work covers image processing fundamentals using OpenCV. The tasks move from basic operations like color space conversion and geometric transforms, through noise handling, edge and contour detection, thresholding, feature matching, face detection, and real-time video processing, and finally into camera calibration and lens undistortion. All experiments were run on a self-captured image and video set (normal light photo, low light photo, an objects photo, a form/text page photo, a short video clip, and a second objects photo from a different angle), plus a separate set of chessboard images for calibration.

## Tasks Completed

- Task 0 - Capture image set: Captured all required raw images and one short video, stored in a single folder for reuse across tasks.
- Task 1 - Color space conversion: Converted the low light photo to Grayscale, HSV, and RGB, and compared how each HSV channel holds up in dark regions.
- Task 2 - Image blending via feature matching: Detected ORB keypoints on the normal and low light photos, matched them, estimated a homography with RANSAC, warped one image onto the other, and blended the pair at different alpha/beta values.
- Task 3 - Geometric transformations: Computed a personal angle and scale value, then applied translation, rotation, scaling, and a general affine transform to the objects photo, reading out each resulting matrix.
- Task 4 - Noise and filtering: Added Gaussian noise to the text page photo, then compared Mean, Gaussian, Median, and Bilateral filters against an initial prediction.
- Task 5 - Edge and contour detection: Ran Canny edge detection at different thresholds until a clean, closed set of contours was found, then used findContours with area filtering and morphological closing to auto-count the objects.
- Task 6 - Thresholding and morphology: Applied Otsu's thresholding to the text page photo, then tested different closing kernel sizes to repair broken text strokes without merging characters.
- Task 7 - Feature matching across photos: Took a sixth photo from a different angle and ran ORB matching against the original objects photo, filtering matches by distance.
- Task 8 - Face detection: Ran a Haar cascade face detector on the normal light photo at different minNeighbors values and examined a false positive on a shirt pattern.
- Task 9 - Real-time video processing: Built a set of switchable real-time effects (edge detection, face detection, channel views, keypoints, noise) applied frame by frame to the video clip, with output saved through VideoWriter.
- Task 10 - Camera calibration and lens undistortion: Captured chessboard images from different angles, detected and refined internal corners, ran calibrateCamera to get the intrinsic matrix and distortion coefficients, and used them to undistort a doorway photo.

## Observations

- Task 1 -  In low light, the HSV Value channel keeps the most visible structure since it directly reflects brightness, while Hue is mostly noisy due to weak color information.
- Task 2 - The homography between the normal and low light photos came out close to identity, since both photos were taken from the same fixed angle with only lighting changed; alpha values around 0.70-0.90 gave the most natural-looking blend.
- Task 3 - The rotation, scaling, and combined rotation+scaling matrices matched the expected cos/sin and scale patterns, with OpenCV automatically adding translation terms to keep the transform centered on the image rather than the origin.
- Task 4 - Bilateral filtering preserved text edges best at a small diameter, since a smaller neighborhood limits smoothing to genuinely similar pixels; at larger diameters it converged toward the Gaussian filter's behavior on this black-and-white image. Median filtering struggled the most under Gaussian noise.
- Task 5 - Canny thresholds needed to be pushed lower than the default (50, 150) down to (25, 27) to get fully closed contours; the resulting edge map still needed area filtering and morphological closing to avoid overcounting from background wrinkles.
- Task 6 - A 3x1 closing kernel gave the best repair for broken text strokes; smaller kernels weren't strong enough and larger kernels caused nearby characters to bleed together, given the image's font size and resolution.
- Task 7 - ORB matching across the two angled objects photos worked best on objects with irregular, textured surfaces (a keychain and a metal idol), while a smooth glass surface produced very few reliable keypoints.
- Task 8 - The Haar cascade face detector produced a false positive on a checked shirt pattern at minNeighbors=1, since the fabric's contrast pattern resembled a face-like gradient; increasing minNeighbors to 5 removed it.
- Task 9 - Building the real-time video pipeline surfaced a few real bugs along the way: calling np.median instead of np.median(frame2), trying to concatenate a single-channel edge map with a BGR frame, and displaying the frame before applying the selected effect. Each was fixed by correcting the function call, converting the edge map back to BGR, and reordering the effect application before display.
- Task 10 - Camera calibration gave low reprojection error overall, a few chessboard images were discarded because a hand partially covered one edge of the board, which broke corner detection. The undistorted doorway image showed a visible correction, though the original photo already had very little distortion due to the phone's built-in lens correction, suggesting the estimated distortion coefficients may be a slight overestimate for this camera.

## Project Structure

```
.
├── raw_captures/
│   ├── sudar.jpg                 # normal light photo
│   ├── sudar_low_light.jpg       # low light photo
│   ├── objects.jpeg              # objects photo
│   ├── objects_rotated.jpeg      # objects photo, different angle
│   ├── form.jpeg                 # text/form page photo
│   ├── short_clip.mp4            # short video clip
│   └── output.mp4                # processed video output (Task 9)
├── distortion/
│   └── *.jpeg                    # chessboard calibration images
├── haarcascade_frontalface_default.xml # model weights related file for face detection
├── A4_chessboard_9x6.pdf         # chessboard used for calibration
├── doorway.jpeg                  # input photo for undistortion (Task 10)
├── doorway_undistorted.jpg       # output after undistortion (Task 10)
└── image_processing.ipynb        # main notebook with all tasks
```

## References

- [Detecting and Tracking object using ORB - siromer | Medium](https://medium.com/thedeephub/detecting-and-tracking-objects-with-orb-using-opencv-d228f4c9054e)
- [Homograph/Feature Matching by jeffcrouse](https://forum.derivative.ca/t/feature-matching-homography-with-orb-sift-brisk-etc/622687)
- [Homograph - GFG](https://www.geeksforgeeks.org/computer-vision/what-is-homography-how-to-estimate-homography-between-two-images/)
- [Wrap Perspective - The AI Learner](https://theailearner.com/tag/cv2-warpperspective/)
- [Blend Image - GFG](https://www.geeksforgeeks.org/computer-vision/image-blending-using-opencv/)
- [Concept of rotation in OpenCV](https://data-flair.training/blogs/geometric-transformations-of-images-using-opencv/)
- [Affine Transformation, rotation code - OpenCV 5.0 documentation](https://docs.opencv.org/5.0/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html#affine-transformation)
- [Adding noise to image - askpython](https://www.askpython.com/python/examples/adding-noise-images-opencv)
- [OpenCV Smoothing and Blurring - Adrian Rosebrock](https://pyimagesearch.com/2021/04/28/opencv-smoothing-and-blurring/)
- [Count Objects using Canny - GFG](https://www.geeksforgeeks.org/computer-vision/count-number-of-object-using-python-opencv/)
- [Morphological Operations with OpenCV - Medium](https://mamuncseru.medium.com/a-brief-discussion-on-morphological-operators-using-opencv-ccf6be076896)
- [Face detection with Cascade Classifier - GFG](https://www.geeksforgeeks.org/python/face-detection-using-cascade-classifier-using-opencv-python/)
- [Camera Calibration and 3D Reconstruction - OpenCV 5.0 documentation](https://docs.opencv.org/5.0/py_tutorials/py_calib3d/py_calibration/py_calibration.html)
- [OpenCv Python Camera Calibration by Kevin Wood  - Youtube](https://youtu.be/H5qbRTikxI4?si=_HKxrKnZCqNhJVeS)