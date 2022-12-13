#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
import numpy as np


# In[39]:


#selecting pixels of the advancing part
def advancing_pixel_selection( i_list,j_list, left_number_of_pixels=150):
    
    #selecting left side of the droplet
    i_list=np.array(i_list)
    j_list=np.array(j_list)
    i_left=i_list[(i_list<int(np.mean(i_list))) & (j_list<left_number_of_pixels)]
    j_left=j_list[(i_list<int(np.mean(i_list))) & (j_list<left_number_of_pixels)]
    i_left=i_left[j_left<max(j_left)-2]
    j_left=j_left[j_left<max(j_left)-2]
    
    #selecting the exact number of pixels based on the input
    j_left_selected=[]
    i_left_selected=[]
    for j in range(len(j_left)):
        remain_number=left_number_of_pixels-len(j_left_selected)
        if remain_number==0:
            break

        elif remain_number>=len(i_left[j_left==j]):
            i_left_selected=i_left_selected+list(i_left[j_left==j])
            j_left_selected=j_left_selected+list(j_left[j_left==j])

        elif remain_number<len(i_left[j_left==j]):
            final_remain=len(i_left[j_left==j])-remain_number
            i_sort=np.sort(i_left[j_left==j])
            i_left_selected=i_left_selected+list(i_sort[:final_remain])
            j_left_selected=j_left_selected+list(j_left[j_left==j][:final_remain])

    return(i_left_selected, j_left_selected)

#select pixels of the receding part
def receding_pixel_selection( i_list,j_list, right_number_of_pixels=65):

    #selecting left side of the droplet
    i_list=np.array(i_list)
    j_list=np.array(j_list)
    i_right=i_list[(i_list>int(np.mean(i_list))) & (j_list<right_number_of_pixels)]
    j_right=j_list[(i_list>int(np.mean(i_list))) & (j_list<right_number_of_pixels)]
    i_right=i_right[j_right<max(j_right)-2]
    j_right=j_right[j_right<max(j_right)-2]

    #selecting the exact number of pixels based on the input
    j_right_selected=[]
    i_right_selected=[]
    for j in range(len(j_right)):
        remain_number=right_number_of_pixels-len(j_right_selected)
        if remain_number==0:
            break

        elif remain_number>=len(i_right[j_right==j]):
            i_right_selected=i_right_selected+list(i_right[j_right==j])
            j_right_selected=j_right_selected+list(j_right[j_right==j])

        elif remain_number<len(i_right[j_right==j]):
            final_remain=len(i_right[j_right==j])-remain_number
            i_sort=np.sort(i_right[j_right==j])
            i_right_selected=i_right_selected+list(i_sort[:final_remain]) #i_sort[final_remain:] bood
            j_right_selected=j_right_selected+list(j_right[j_right==j][:final_remain])

    return(i_right_selected, j_right_selected)

#fitting the polynomial
def poly_fitting( i,j,polynomial_degree=3,line_space=100):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', np.RankWarning)
        y_polyequation_left = np.poly1d(np.polyfit(i,j,polynomial_degree))

    x_poly_left = np.linspace(min(i), max(i), line_space)
    y_poly_left=y_polyequation_left(x_poly_left)

    return(x_poly_left, y_poly_left)

#advancing angle calculations
def left_angle( i_poly_left, j_poly_left, tan_pixel_number=1):
    
    dx=i_poly_left[tan_pixel_number]-i_poly_left[0]
    dy=j_poly_left[tan_pixel_number]-j_poly_left[0]
    gradian=np.arctan((dy)/(dx))
    horizontal_angle=gradian*180/np.pi
    left_angle=90-horizontal_angle
    left_pixel_position=j_poly_left[0]    
    return(left_angle,left_pixel_position)

#receding angle calculations
def right_angle( i_poly_right, j_poly_right, tan_pixel_number=1):
    
    dx=i_poly_right[tan_pixel_number]-i_poly_right[0]
    dy=j_poly_right[tan_pixel_number]-j_poly_right[0]
    gradian=np.arctan((dy)/(dx))
    horizontal_angle=gradian*180/np.pi
    right_angle=90+horizontal_angle
    right_pixel_position=j_poly_right[0]
    return(right_angle,right_pixel_position)

#middel line angle calculations
def middle_angle( i_poly_right, j_poly_right):
    dx=i_poly_right[-2]-i_poly_right[-1]
    dy=j_poly_right[-2]-j_poly_right[-1]
    gradian=np.arctan((dy)/(dx))
    horizontal_angle=gradian*180/np.pi

    if dx<0:
        middle_angle=-horizontal_angle

    if dx>0:
        middle_angle=180+90-horizontal_angle

    middle_pixel_position=i_poly_right[-1]
    return(middle_angle,middle_pixel_position)

#horizontal center calculations
#the intersection margin variable is a margin from the top side of the edge to prevent some error in special cases
def horizontal_center( i_list,j_list,intersection_margin=4):

    #separating the drop into two right and left sides
    i_list, j_list = np.array(i_list), np.array(j_list)
    i_middle_vertical=int(np.mean(i_list[j_list==max(j_list)]))
    i_list_left, j_list_left= i_list[i_list<=i_middle_vertical],j_list[i_list<=i_middle_vertical]
    i_list_right, j_list_right= i_list[i_list>i_middle_vertical],j_list[i_list>i_middle_vertical]

    mean_list=[]
    j_location_list=[]
    total_weight=0
    sum_all=0
    for j_location in range(max(j_list_left)-intersection_margin):
        horizontal_pixels_left=i_list_left[j_list_left==j_location]
        for i in range(len(horizontal_pixels_left)):
            if max(horizontal_pixels_left)-i not in horizontal_pixels_left:
                i=i-1
                break
        try:
            left_pix=max(horizontal_pixels_left)-i
        except:
            if j_location==0:
                continue
            pass

        horizontal_pixels_right=i_list_right[j_list_right==j_location]
        for i in range(len(horizontal_pixels_right)):
            if min(horizontal_pixels_right)+i not in horizontal_pixels_right:
                i=i-1
                break  
        try:
            right_pix=min(horizontal_pixels_right)+i
        except:
            if j_location==0:
                continue
            pass

        weight=abs(right_pix-left_pix)
        mean=np.mean([right_pix,left_pix])
        mean_list=mean_list+[mean]
        j_location_list=j_location_list+[j_location]
        sum_all=sum_all+weight*mean
        total_weight=total_weight+weight
        horizontal_center=sum_all/total_weight
    return(horizontal_center,mean_list,j_location_list)

#vertical center calculations
#the intersection margin variable is a margin from the left side of the edge to prevent some error in special cases
def vertical_center( i_list,j_list,intersection_margin=4):
    down_pix=0  

    #deviding right and left
    i_list, j_list = np.array(i_list), np.array(j_list)
    i_middle_vertical=int(np.mean(i_list[j_list==max(j_list)]))
    i_list_left, j_list_left= i_list[i_list<=i_middle_vertical],j_list[i_list<=i_middle_vertical]
    i_list_right, j_list_right= i_list[i_list>i_middle_vertical],j_list[i_list>i_middle_vertical]

    #deviding left to up and down
    j_middle_horizontal_left=int(np.mean(j_list_left[i_list_left==min(i_list_left)]))
    i_list_left_down, j_list_left_down= i_list_left[j_list_left<=j_middle_horizontal_left],j_list_left[j_list_left<=j_middle_horizontal_left]
    i_list_left_up, j_list_left_up= i_list_left[j_list_left>j_middle_horizontal_left],j_list_left[j_list_left>j_middle_horizontal_left]

    #deviding right to up and down
    j_middle_horizontal_right=int(np.mean(j_list_right[i_list_right==max(i_list_right)]))
    i_list_right_down, j_list_right_down= i_list_right[j_list_right<=j_middle_horizontal_right],j_list_right[j_list_right<=j_middle_horizontal_right]
    i_list_right_up, j_list_right_up= i_list_right[j_list_right>j_middle_horizontal_right],j_list_right[j_list_right>j_middle_horizontal_right]

    #left intersection calculation
    mean_list_intersection_left=[]
    i_location_list_intersection_left=[]
    sum_all_intersection_left=0
    total_weight_intersection_left=0
    for i_location_left_down in range(min(i_list_left_down)+intersection_margin,max(i_list_left_down)):

        #the lowermost related pixel in left side
        vertical_pixels_left_down=j_list_left_down[i_list_left_down==i_location_left_down]
        for j in range(len(vertical_pixels_left_down)):
            if max(vertical_pixels_left_down)-j not in vertical_pixels_left_down:
                j=j-1
                break

        try: #Because of some vacant point in left-down side of the drop
            down_pix=max(vertical_pixels_left_down)-j
        except:
            pass

        #the uppermost related pixel in left side 
        vertical_pixels_left_up=j_list_left_up[i_list_left_up==i_location_left_down]
        for j in range(len(vertical_pixels_left_up)):
            if min(vertical_pixels_left_up)+j not in vertical_pixels_left_up:
                j=j-1
                break
        try:
            up_pix=min(vertical_pixels_left_up)+j
        except:
            pass

        weight=abs(up_pix-down_pix)
        mean=np.mean([up_pix,down_pix])

        mean_list_intersection_left=mean_list_intersection_left+[mean]
        i_location_list_intersection_left=i_location_list_intersection_left+[i_location_left_down]

        sum_all_intersection_left=sum_all_intersection_left+weight*mean
        total_weight_intersection_left=total_weight_intersection_left+weight

    #left simple calculation
    mean_list_simple_left=[]
    i_location_list_simple_left=[]
    sum_all_simple_left=0
    total_weight_simple_left=0
    for i_location_left_up in range(max(i_list_left_down),max(i_list_left_up)):

        #the uppermost related pixel in left side
        vertical_pixels_left_up=j_list_left_up[i_list_left_up==i_location_left_up]
        for j in range(len(vertical_pixels_left_up)):
            if min(vertical_pixels_left_up)+j not in vertical_pixels_left_up:
                j=j-1
                break
        try:
            up_pix=min(vertical_pixels_left_up)+j
        except:
            pass

        weight=abs(up_pix)
        mean=np.mean([up_pix,0])

        mean_list_simple_left=mean_list_simple_left+[mean]
        i_location_list_simple_left=i_location_list_simple_left+[i_location_left_up]

        sum_all_simple_left=sum_all_simple_left+weight*mean
        total_weight_simple_left=total_weight_simple_left+weight

    #right intersection calculation
    mean_list_intersection_right=[]
    i_location_list_intersection_right=[]
    sum_all_intersection_right=0
    total_weight_intersection_right=0

    for i_location_right_down in range(min(i_list_right_down),max(i_list_right_down)-intersection_margin):

        #the lowermost related pixel in right side
        vertical_pixels_right_down=j_list_right_down[i_list_right_down==i_location_right_down]
        for j in range(len(vertical_pixels_right_down)):
            if max(vertical_pixels_right_down)-j not in vertical_pixels_right_down:
                j=j-1
                break
        try:
            down_pix=max(vertical_pixels_right_down)-j
        except:
            pass

        #the uppermost related pixel in left side 
        vertical_pixels_right_up=j_list_right_up[i_list_right_up==i_location_right_down]
        for j in range(len(vertical_pixels_right_up)):
            if min(vertical_pixels_right_up)+j not in vertical_pixels_right_up:
                j=j-1
                break
        try:
            up_pix=min(vertical_pixels_right_up)+j
        except:
            pass

        weight=abs(up_pix-down_pix)
        mean=np.mean([up_pix,down_pix])

        mean_list_intersection_right=mean_list_intersection_right+[mean]
        i_location_list_intersection_right=i_location_list_intersection_right+[i_location_right_down]

        sum_all_intersection_right=sum_all_intersection_right+weight*mean
        total_weight_intersection_right=total_weight_intersection_right+weight

    #right simple calculation
    mean_list_simple_right=[]
    i_location_list_simple_right=[]
    sum_all_simple_right=0
    total_weight_simple_right=0
    for i_location_right_up in range(min(i_list_right_up),min(i_list_right_down)):

        #the uppermost related pixel in right side
        vertical_pixels_right_up=j_list_right_up[i_list_right_up==i_location_right_up]
        for j in range(len(vertical_pixels_right_up)):
            if min(vertical_pixels_right_up)+j not in vertical_pixels_right_up:
                j=j-1
                break

        try: #Because of some vacant point in left-down side of the drop
            up_pix=min(vertical_pixels_right_up)+j
        except:
            pass

        weight=abs(up_pix)
        mean=np.mean([up_pix,0])

        mean_list_simple_right=mean_list_simple_right+[mean]
        i_location_list_simple_right=i_location_list_simple_right+[i_location_right_up]

        sum_all_simple_right=sum_all_simple_right+weight*mean
        total_weight_simple_right=total_weight_simple_right+weight

    sum_all=sum_all_simple_right+sum_all_intersection_right+sum_all_simple_left+sum_all_intersection_left
    total_weight=total_weight_simple_right+total_weight_intersection_right+total_weight_simple_left+total_weight_intersection_left
    vertical_center=sum_all/total_weight

    i_location_list=i_location_list_simple_right+i_location_list_intersection_right+i_location_list_simple_left+i_location_list_intersection_left
    mean_list=mean_list_simple_right+mean_list_intersection_right+mean_list_simple_left+mean_list_intersection_left

    return(vertical_center,i_location_list,mean_list)

