#!/usr/bin/env python
# coding: utf-8

# In[2]:


#importing libraries
import numpy as np
import cv2
from scipy.optimize import curve_fit
from scipy import ndimage


# In[4]:


#line equation function
def objective(x, a, b):
    return a *x + b  


# In[1]:


#defining rotation class to detect surface, calculate tilt angle (automatically/manually), and rotate the image
class Rotation:
    #defining initial variables
    #the horizontal_search_area_start and horizontal_search_area_end define the desired area horizontally
    #the starting_height defines the starting point to start searching vertically downward to find the surface
    #the object_detection_threshold select pixels with less than 200 intensity (more black) as the surface line topmost pixels
    def __init__(self,starting_height=350,horizontal_search_area_start=0,
                 horizontal_search_area_end=300,object_detection_threshold=200):
        self.starting_height = starting_height
        self.horizontal_search_area_start = horizontal_search_area_start
        self.horizontal_search_area_end = horizontal_search_area_end
        self.object_detection_threshold = object_detection_threshold
    
    #the surface detection
    def detect_surface(self,img):
        img_detected=img.copy() #making a copy
        img_binarized=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #making the image black and white
        x_detected=[]
        y_detected=[]
        horizontal_search_area=np.arange(self.horizontal_search_area_start, self.horizontal_search_area_end) 
        for x in horizontal_search_area:#covering horizontal search area
            for y in range(self.starting_height,img_binarized.shape[0]): #starting from upside (starting_height) to downside in order to find the surface
                #making the one-fifth of the searching area green to show it visually
                if x%5==0: 
                    img_detected[y,x,:]=[0,255,0] 
                #finding the coordinates of the surface line pixels
                if img_binarized[y,x]<self.object_detection_threshold: 
                    x_detected.append(x)
                    y_detected.append(y)
                    break
        #visualizing the horizontal line
        horizontal_line=int(np.round(np.mean(y_detected))) 
        img_detected[horizontal_line,:horizontal_search_area[0],:]=[255,0,0]
        img_detected[horizontal_line,horizontal_search_area[-1]:,:]=[255,0,0]
        img_detected[y_detected,x_detected,:]=[[0,0,255]]*len(horizontal_search_area)
        
        return(img_detected,x_detected,y_detected,horizontal_line)
            
        
    #the tilt angle measurement
    def tilt_calculation(self, x_detected,y_detected):
        #fitting a line to the surface line coordinates
        popt, _ = curve_fit(objective, x_detected, max(y_detected)-np.array(y_detected))
        a, b = popt
        x_line = np.arange(min(x_detected), max(x_detected), 1)
        y_line = objective(x_line, a, b)
        #the tilt angle calculation
        dy=y_line[-1]-y_line[0]
        dx=x_line[-1]-x_line[0]
        gradian=np.arctan((dy)/(dx))
        angle=gradian*180/np.pi
        
        return(angle)
    
        #the rotation
    def rotate(self,img,angle,mode='reflect'):
        # rotating the image based on calculated angle to make it horizontal
        rotated_image=ndimage.rotate(img, -angle,mode=mode,reshape=0).copy()#{‘reflect’, ‘grid-mirror’, ‘constant’, ‘grid-constant’, ‘nearest’, ‘mirror’, ‘grid-wrap’, ‘wrap’}
        return(rotated_image)
    
        #manually rotation for the specific situations (transparent samples)
    def manually_rotation(self, img, angle=0, surface_line=520,mode='reflect'):
        img_edited=ndimage.rotate(img, -angle,mode=mode,reshape=0).copy()#{‘reflect’, ‘grid-mirror’, ‘constant’, ‘grid-constant’, ‘nearest’, ‘mirror’, ‘grid-wrap’, ‘wrap’}
        img_edited[surface_line,:,:]=np.array([[0,0,255]]*img_edited.shape[1])
        img_edited[surface_line+1,:,:]=np.array([[0,0,255]]*img_edited.shape[1])

        return(img_edited)

