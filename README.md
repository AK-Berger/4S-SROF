# About 4S-SROF

The 4S-SROF toolkit is trying to address existing problems to analyze drop sliding motion on a tilted plate. It helps researchers conduct detailed studies with a broad range of variables considering their correlations. The 4S-SROF is able to enlarge images by up-scale ratio 3 using a super-resolution model trained on a dataset containing 14000 images from sliding drops. Then, different criteria are extracted from super-resolution images. Measuring contact angles is performed by an optimized polynomial explained in the manuscript.


![graphical abstract](https://user-images.githubusercontent.com/57271994/194614949-8736973c-4df3-4449-9a21-bc2423405648.png)

---
# Publication Information:

Title: Deep learning to analyze sliding drops

Authors: Sajjad Shumaly, Fahimeh Darvish, Xiaomei Li, Alexander Saal, Chirag Hinduja, Werner Steffen, Oleksandra Kukharenko, Hans-Jürgen Butt, Rüdiger Berger*

Journal:

Date:

DOI:

---
# Data Information:

### The tutorial

- tutorial.ipynb

    This tutorial contains examples and related outputs to explain how the toolkit works step-by-step. This file can be used by researchers to understand how each step     works and what the parameters are. A comprehensive example is provided at the end of this file that extracts all criteria related to a high-speed camera video.
    
### The drop profile video

- drop_profile.mp4

    The video shows a sliding drop on a sample with a defect in the middle. The first drop in the upper part of the video is a real drop image after preprocessing steps. The main steps of preprocessing included calculating the tilt angle and making the frames horizontal, removing noises and background, and detecting drop position (red lines). The second drop image which is bigger than the first one is the drop image after using a super-resolution model. Below that, the drop contour is extracted and different parameters including CAs, drop height, and drop length are displayed. On the left, four figures are getting plotted to analyze how a drop slides on a sample with a defect.
    
    https://user-images.githubusercontent.com/57271994/194625754-6250b70f-d77e-4519-8815-165735eb803c.mp4

### The ESPCN super-resolution model weights: 

- SuperRes_weights.h5

    A modified ESPCN super-resolution model has been trained based on 14000 sliding drops images. SuperRes_weights.h5 is the wight file related to the trained model.

### .py files: 

- angle_detection.py

- baseline_detection.py

- criteria_definition.py

- edge_superres.py

- tools.py

- visualization.py

    Mentioned .py files contains toolkit's functions to helps researchers to do related image processing.

### The dataset: 

- This is provided in research supporting information. 14000 sliding drop images were used as the dataset to train the modified super-resolution model. [Download the dataset](https://www.kaggle.com/datasets/sajjdeus/4s-srof).

### Samples: 

- This is provided in research supporting information. Two sliding drop examples can be found in this folder. There are examples and pre-runed output in "tutorial.ipynb". Nevertheless, if someone wishes to run each cell, they must add the "samples" folder to the relevant working directory or replace the video frames with another appropriate one.

---
# Dependencies 

- tensorflow 2.5.0; https://pypi.org/project/tensorflow/

- keras 2.9.0; https://pypi.org/project/keras/

- cv2 4.5.4; https://pypi.org/project/opencv-python/

- scipy 1.7.1; https://pypi.org/project/scipy/

- PIL 8.4.0; https://pypi.org/project/PIL/

- numpy 1.20.3; https://pypi.org/project/numpy/

- pandas 1.3.4; https://pypi.org/project/pandas/

- matplotlib 3.4.3; https://pypi.org/project/matplotlib/

---
# Support

You can communicate with us using the following e-mails:

- shumalys@mpip-mainz.mpg.de
- berger@mpip-mainz.mpg.de
---
