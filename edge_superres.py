#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing libraries
import numpy as np
import cv2
from tensorflow import keras
from tensorflow.keras import layers
from PIL import Image
import PIL
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array


# In[22]:


#building the model structure and loading the trained weight on it
def model_architecture(weight_address):
    #initial values
    upscale_factor=3
    channels=1
    conv_args = {
        "activation": "relu",
        "kernel_initializer": "Orthogonal",
        "padding": "same",
    }
    #model structure
    inputs = keras.Input(shape=(None, None, channels))
    x = layers.Conv2D(64, 5, **conv_args)(inputs)
    x = layers.Conv2D(64, 3, **conv_args)(x)
    x = layers.Conv2D(32, 3, **conv_args)(x)
    x = layers.Conv2D(channels * (upscale_factor ** 2), 3, **conv_args)(x)
    outputs = tf.nn.depth_to_space(x, upscale_factor)
    #loading model
    model=keras.Model(inputs, outputs)
    model.load_weights(weight_address)

    return(model)

#converting the low-resolution image to super-resolution image and related preprocessing
def upscale_image(model, img):
    ycbcr = img.convert("YCbCr")
    y, cb, cr = ycbcr.split()
    y = img_to_array(y)
    y = y.astype("float32") / 255.0

    input = np.expand_dims(y, axis=0)
    
    out = model.predict(input)
    out_img_y = out[0]
    out_img_y *= 255.0
    out_img_y = out_img_y.clip(0, 255)
    out_img_y = out_img_y.reshape((np.shape(out_img_y)[0], np.shape(out_img_y)[1]))
    out_img_y = PIL.Image.fromarray(np.uint8(out_img_y), mode="L")
    
    out_img_cb = cb.resize(out_img_y.size, PIL.Image.BICUBIC)
    out_img_cr = cr.resize(out_img_y.size, PIL.Image.BICUBIC)
    out_img = PIL.Image.merge("YCbCr", (out_img_y, out_img_cb, out_img_cr)).convert("RGB")
    out_img=cv2.GaussianBlur(np.array(out_img),(3,3),0)
    return (out_img)

#edge detection using canny and removing extra detected pixels
def edge_extraction_canny( upscaled_image, canny_v1=100, canny_v2=200):

    j_list_left=[]
    i_list_left=[]
    upscaled_image_canny=cv2.Canny(np.array(upscaled_image),canny_v1,canny_v2)
    #finding the external left side pixels
    for j in range(upscaled_image_canny.shape[0]-1,0,-1):
        for i in range(0,upscaled_image_canny.shape[1]):
            if upscaled_image_canny[j,i]!=0:
                j_list_left.append(j)
                i_list_left.append(i)
                break
    i_list_left=np.array(i_list_left)
    j_list_left=np.array(j_list_left)
    #finding the external right side pixels
    j_list_right=[]
    i_list_right=[]
    for j in range(upscaled_image_canny.shape[0]-1,0,-1):
        for i in range(upscaled_image_canny.shape[1]-1,0,-1):
            if upscaled_image_canny[j,i]!=0:
                j_list_right.append(j)
                i_list_right.append(i)
                break
    i_list_right=np.array(i_list_right)
    j_list_right=np.array(j_list_right)
    #finding the external up side pixels
    j_list_up=[]
    i_list_up=[]
    for i in range(upscaled_image_canny.shape[1]):
        for j in range(upscaled_image_canny.shape[0]):
            if upscaled_image_canny[j,i]!=0:
                j_list_up.append(j)
                i_list_up.append(i)
                break
    j_list_up=np.array(j_list_up)
    j_list_up=np.array(j_list_up)
    #merging all the external pixels   
    i_list= list(i_list_left) + list(i_list_right) + list(i_list_up)
    j_list= list(j_list_left) + list(j_list_right) + list(j_list_up)
    #delete duplicates
    i_list,j_list=list(zip(*list(set(zip(i_list,j_list)))))

    j_list=max(j_list)-j_list

    return(i_list,j_list)

#edge detection using a simple threshold to detect objects and removing extra detected pixels
def edge_extraction(upscaled_image, thr=40):

    j_list_left=[]
    i_list_left=[]
    upscaled_image=cv2.cvtColor(np.array(upscaled_image),cv2.COLOR_BGR2GRAY)
    #finding the external left side pixels
    for j in range(upscaled_image.shape[0]-1,0,-1):
        for i in range(0,upscaled_image.shape[1]):
            if upscaled_image[j,i]>thr:
                j_list_left.append(j)
                i_list_left.append(i)
                break
    i_list_left=np.array(i_list_left)
    j_list_left=np.array(j_list_left)
    #finding the external right side pixels
    j_list_right=[]
    i_list_right=[]
    for j in range(upscaled_image.shape[0]-1,0,-1):
        for i in range(upscaled_image.shape[1]-1,0,-1):
            if upscaled_image[j,i]>thr:
                j_list_right.append(j)
                i_list_right.append(i)
                break
    i_list_right=np.array(i_list_right)
    j_list_right=np.array(j_list_right)
    #finding the external up side pixels
    j_list_up=[]
    i_list_up=[]
    for i in range(upscaled_image.shape[1]):
        for j in range(upscaled_image.shape[0]):
            if upscaled_image[j,i]>thr:
                j_list_up.append(j)
                i_list_up.append(i)
                break
    j_list_up=np.array(j_list_up)
    j_list_up=np.array(j_list_up)
    #merging all the external pixels 
    i_list= list(i_list_left) + list(i_list_right) + list(i_list_up)
    j_list= list(j_list_left) + list(j_list_right) + list(j_list_up)
    #delete duplicates
    i_list,j_list=list(zip(*list(set(zip(i_list,j_list)))))

    j_list=max(j_list)-j_list

    return(i_list,j_list)

