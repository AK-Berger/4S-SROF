#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing libraries
import numpy as np
import cv2
import angle_detection
import tools
from angle_detection import Rotation


# In[1]:


class Baseline:
    
    #middle_drop_height is a margin upside of the surface line where we can say surely is not in the reflection part
    #drop_start_height is a margin upside of the surface line, searching to find baseline will start vertically from drop_middle_y to drop_start downward
    #object_detection_threshold is a threshold to find objects on the image
    def __init__(self, surface_line ,middle_drop_height=20,drop_start_height=0, object_detection_threshold=40):
        self.object_detection_threshold=object_detection_threshold
        self.drop_start=surface_line-drop_start_height 
        self.drop_middle_y=self.drop_start-middle_drop_height
    
    #drop_existence help to find out if there is any droplet in the frame or not
    #it is starting to search for the droplet edge horizontally
    def drop_existence(self,diff_img):
        len_x_diff_img=diff_img.shape[1]
        
        for x_left in range(len_x_diff_img):
            if diff_img[self.drop_middle_y,x_left,0]>self.object_detection_threshold:
                break
        drop_existence=  x_left< len_x_diff_img-2
        
        return(drop_existence,x_left)
    
    #drop_cropping finds the droplet position then crop it based on input margin values (x_left_margin,x_right_margin,y_up_margin)
    def drop_cropping(self,diff_img, x_left_margin=30, x_right_margin=60,y_up_margin=10):
        len_x_diff_img=diff_img.shape[1]
    
        #calculating left side cropping position
        for x_left in range(len_x_diff_img):
            if diff_img[self.drop_middle_y,x_left,0]>self.object_detection_threshold:
                break
        x_left=x_left-x_left_margin
        
        #calculating right side cropping position
        len_x_diff_img=diff_img.shape[1]
        for x_right in np.arange(len_x_diff_img-1,0,-1):
            if diff_img[self.drop_middle_y,x_right,0]>self.object_detection_threshold:
                break
        x_right=x_right+x_right_margin
        
        #calculating down side cropping position
        x_position=0
        for y_down in range(self.drop_middle_y,self.drop_start):
            if x_position >len_x_diff_img-2:
                break
            for x_position in range(x_left,len_x_diff_img):
                if diff_img[y_down,x_position,0]>self.object_detection_threshold:
                    break  
        
        #calculating up side cropping position
        len_y_diff_img=diff_img.shape[0]
        x_position=0
        for y_up in range(self.drop_middle_y,0,-1):
            if x_position ==len_x_diff_img-1:
                break
            for x_position in range(x_left,len_x_diff_img):
                if diff_img[y_up,x_position,0]>self.object_detection_threshold:
                    break
        y_up=y_up-y_up_margin
        drop_reflection=diff_img[y_up:y_down,x_left:x_right]
        return(drop_reflection,x_left,x_right,y_up,y_down)
    
#baseline detection based on canny edge detection algorithm
#drop_check_height is a margin upside of the surface line where we can say surely is not in the reflection part
def edgebased_baseline_detection(drop_reflection,drop_check_height=20):
    j_list=[]
    i_list=[]
    #calculate edge based on canny
    canny_diff_drop=cv2.Canny(drop_reflection,100,200)

    #finding the coordinates of the outermost pixels of the edge of the advancing part of the droplet
    for j in range(canny_diff_drop.shape[0]-drop_check_height,canny_diff_drop.shape[0]):
        for i in range(canny_diff_drop.shape[1]):
            if canny_diff_drop[j,i]!=0:
                j_list.append(j)
                i_list.append(i)
                break    
                
    #removing the downside of the droplet where the reflection is not recognizable well
    for base_line_index in range(len(i_list)-1):
        if abs(i_list[base_line_index+1]-i_list[base_line_index])>4:
            break

    #find the baseline based on the pixels' coordinates, the first maximum i value will be considered as the baseline
    i_list=np.array(i_list[:base_line_index+1])
    j_list=np.array(j_list[:base_line_index+1])
    i_max=max(i_list)
    j_max=max(j_list[i_list==i_max])
    counter=0
    while True:
        if i_list[j_list==j_max-counter-1]==i_max:
            counter+=1
        else:
            break
    base_line=j_max-counter

    just_drop=drop_reflection[:base_line,:,:]
    return(just_drop,canny_diff_drop,base_line)

#baseline detection based on differentiation in color 
def colorbased_baseline_detection(drop_reflection):
    #calculating the whiteness of every row
    list_mean_whiteness=[]
    for i in range(drop_reflection.shape[0]):
        white_pixels=drop_reflection[i,:,0]
        list_mean_whiteness=list_mean_whiteness+[np.mean(white_pixels)]
    
    #calculating the derivativeof the whiteness of every row
    list_mean_whiteness_derivative=[]
    for i in range(drop_reflection.shape[0]-1):
        derivative=list_mean_whiteness[i+1]-list_mean_whiteness[i]
        list_mean_whiteness_derivative=list_mean_whiteness_derivative+[derivative]
    list_mean_whiteness_derivative=list_mean_whiteness_derivative+[0]
    return(list_mean_whiteness_derivative.index(min(list_mean_whiteness_derivative)))

#test if angle, surface line, and baseline measured correctly
def test_baseline_detection(address, angle, surface_line, startingframe_index, endingframe_index, baseline_method="edgebased",
                            frame_index=0, interval=5, alpha = 0.95, up_margin= 50, down_margin= 50):
    
    #loading the frame
    name_files=tools.load_files(address,formatt='tif')
    img=cv2.imread(address+"\\"+name_files[frame_index]) 
    #rotate the frame
    Rotate=Rotation(starting_height=450,horizontal_search_area_start=600,horizontal_search_area_end=800,object_detection_threshold=200) 
    rotated_image_frame=Rotate.rotate(img,angle)
    #load the first drop image to make reference image
    img=cv2.imread(address+"\\"+name_files[startingframe_index]) 
    rotated_image_drop=Rotate.rotate(img,angle)
    diff_img_ref=cv2.absdiff(rotated_image_drop, rotated_image_frame)

    #loading all drop images, extracting droplet part and adding it to reference image
    baseline_list=[]
    counter=0
    for i in np.arange(startingframe_index,endingframe_index,interval):
        counter+=1
        print(i,end=", ")
        #loading and rotating images
        img=cv2.imread(address+"\\"+name_files[i]) 
        rotated_image_drop=Rotate.rotate(img,angle)
        #calculating diff image
        diff_img=cv2.absdiff(rotated_image_drop, rotated_image_frame)
        #extracting drop part
        BaseL=Baseline(surface_line, middle_drop_height=25,drop_start_height=0, object_detection_threshold=40)
        if counter==1:
            drop_reflection,*dim=BaseL.drop_cropping(diff_img, x_left_margin=30, x_right_margin=30,y_up_margin=up_margin)
        else:
            drop_reflection, dim[0],dim[1],_,dim[3]=BaseL.drop_cropping(diff_img, x_left_margin=30, x_right_margin=30,y_up_margin=up_margin)
        #choosing the method 
        if baseline_method =="edgebased":
            baseline=edgebased_baseline_detection(drop_reflection)[2]
        if baseline_method =="colorbased":
            baseline=colorbased_baseline_detection(drop_reflection)
        baseline_list=baseline_list+[baseline]
        #make droplets' images transparent
        diff_img_ref = cv2.addWeighted(diff_img_ref, alpha, diff_img, 1,0 )
    #calculate baseline based on all images
    baseline=int(np.round(np.median(baseline_list)))
    diff_img_ref[dim[2]+baseline,:,:]=[255,0,0]
    diff_img_ref=diff_img_ref[dim[2]:dim[2]+baseline+down_margin,:,:]
    return(diff_img_ref,baseline_list)

