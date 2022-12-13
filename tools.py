#!/usr/bin/env python
# coding: utf-8

# In[4]:


#importing libraries
import pandas as pd
import numpy as np
import cv2
import os


# In[42]:


#a function to load all similar formats pictures in a folder 
def load_files(add,formatt='tif'):
    FileNames=[]
    FileName=os.listdir(add)
    for i in range(len(FileName)):
        try:
            if FileName[i].split(".")[1]==formatt:
                FileNames=FileNames+[FileName[i]]
        except:
            pass
    return(FileNames)

#checking if the frame is suitable to start analyzing or not
def drop_check(diff_img,surface_y, pic_y_length=150, vertical_margin=10 , horizontal_margin=10):
    #noise removing 
    kernel = np.ones((3,3),np.uint8) #3 is maximum allowed number
    diff_img=cv2.morphologyEx(np.array(diff_img), cv2.MORPH_CLOSE, kernel)
    #edge detection
    diff_img=cv2.Canny(diff_img,100,200)
    #background removing
    diff_img=diff_img[surface_y-pic_y_length:surface_y,:]

    #checking if there is any droplet in the image or not
    horiz_check_line=pic_y_length-horizontal_margin
    drop_existance=0
    for i in range(diff_img.shape[1]):
        if diff_img[horiz_check_line,i]==255:
            drop_existance=1
            break

    #checking if the drop is going out and a part of the droplet is outside or not
    left_vert_check_line_1=0
    left_drop_1=0
    for j in range(diff_img.shape[0]):
        if diff_img[j,left_vert_check_line_1]==255:
            left_drop_1=1
            break
    left_vert_check_line_2=vertical_margin
    left_drop_2=0
    for j in range(diff_img.shape[0]):
        if diff_img[j,left_vert_check_line_2]==255:
            left_drop_2=1
            break


    #checking if the drop is coming in and a part of the droplet is outside or not
    right_vert_check_line_1=diff_img.shape[1]-1
    right_drop_1=0
    for j in range(diff_img.shape[0]):
        if diff_img[j,right_vert_check_line_1]==255:
            right_drop_1=1
            break
    right_vert_check_line_2=diff_img.shape[1]-1-vertical_margin
    right_drop_2=0
    for j in range(diff_img.shape[0]):
        if diff_img[j,right_vert_check_line_2]==255:
            right_drop_2=1
            break

    #create an image to make sure everything is working
    diff_img[horiz_check_line,:]=255
    diff_img[:,left_vert_check_line_1]=255
    diff_img[:,left_vert_check_line_2]=255
    diff_img[:,right_vert_check_line_1]=255
    diff_img[:,right_vert_check_line_2]=255

    return(drop_existance, left_drop_1, left_drop_2, right_drop_1, right_drop_2,diff_img)

