#!/usr/bin/env python
# coding: utf-8

# In[92]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import criteria_definition
plt.rcParams["figure.figsize"] = (20,15)


# In[94]:


def visualize(save_address ,i_list,j_list,i_left,j_left,i_right,j_right,
             j_poly_left,i_poly_left,j_poly_right,i_poly_right,x_cropped,
             i_poly_left_rotated, j_poly_left_rotated, i_poly_right_rotated, j_poly_right_rotated, middle_line_switch=0):

    plt.cla()
    font_size=14

    #conversion_factor
    cm_on_pixel=5/1280
    upscale_factor=3
    conversion_factor=cm_on_pixel/upscale_factor

    #DropShape
    plt.plot(i_list, j_list,'.',color='black')

    #Contact angle edge
    plt.plot(i_left, j_left,'.',color='red',markersize=12)
    plt.plot(i_right, j_right,'.',color='red',markersize=12)

    #Poly fit
    plt.plot(i_poly_left, j_poly_left,'--',color='yellow',linewidth=4)
    plt.plot(i_poly_right, j_poly_right,'--',color='yellow',linewidth=4)

    #left angle
    left_angle_degree,left_angle_point=criteria_definition.left_angle(i_poly_left_rotated, j_poly_left_rotated,1)
    adv=left_angle_degree
    plt.plot([i_poly_left[0]+20,i_poly_left[0]],[j_poly_left[0],j_poly_left[0]],linewidth=3, color='blue')
    m=np.tan(left_angle_degree*(np.pi/180))
    plt.plot([i_poly_left[0],i_poly_left[0]+(1/m)*j_poly_left[5]],[j_poly_left[0],j_poly_left[5]],linewidth=3, color='blue')
    plt.text(i_poly_left[0], j_poly_left[0]-12, 'Advancing='+str(round(adv, 2)), color="blue", fontsize=font_size)

    #right angle
    right_angle_degree,right_angle_point=criteria_definition.right_angle(i_poly_right_rotated, j_poly_right_rotated,1)
    rec=right_angle_degree
    plt.plot([i_poly_right[0]-20,i_poly_right[0]],[j_poly_right[0],j_poly_right[0]],linewidth=3, color='blue')
    m=np.tan(right_angle_degree*(np.pi/180))
    plt.plot([i_poly_right[0],i_poly_right[0]-(1/m)*j_poly_right[10]],[j_poly_right[0],j_poly_right[10]],linewidth=3, color='blue')
    plt.text(i_poly_right[0]-65, j_poly_right[0]-12, 'Receding='+str(round(rec, 2)), color="blue", fontsize=font_size)

    #Contact line
    contact_line_length=(right_angle_point-left_angle_point)*conversion_factor
    plt.plot([(x_cropped*3)+np.array(left_angle_point),(x_cropped*3)+np.array(right_angle_point)],[0,0],'--',linewidth=1, color='red')
    plt.text(((x_cropped*3)+np.array(right_angle_point)+(x_cropped*3)+np.array(left_angle_point))/2-60, j_poly_right[0]-12, 'Contact line length='+str(round(contact_line_length,3))+' cm', color="red", fontsize=font_size)
    right_angle_point=((1280)*3-right_angle_point-(x_cropped)*3)*conversion_factor
    left_angle_point=((1280)*3-left_angle_point+-(x_cropped)*3)*conversion_factor

    #horizontal center
    i_list, j_list = np.array(i_list), np.array(j_list)
    v_center,*v=criteria_definition.vertical_center(i_list,j_list)
    h_center,i_mean,j_mean=criteria_definition.horizontal_center(i_list,j_list)
    plt.plot([h_center,h_center],[min(j_list),j_list[i_list==int(h_center)][0]],'--',color='green')
    drop_height=abs(min(j_list)-j_list[i_list==int(h_center)][0])*conversion_factor
    i_text_horizontal=(j_list[i_list==int(h_center)][0]+v_center)/2
    plt.text(h_center+5, i_text_horizontal, str(round(drop_height,3))+' cm', color="green", fontsize=font_size)

    #middle line
    i_middle_line,j_middle_line=criteria_definition.poly_fitting(i_mean,j_mean,polynomial_degree=1,line_space=100)
    middle_angle_degree=criteria_definition.middle_angle(i_middle_line, j_middle_line)
    if middle_line_switch !=0:
        i_middle_line,j_middle_line=criteria_definition.poly_fitting(i_mean,j_mean,polynomial_degree=1,line_space=100)
        middle_angle_degree=criteria_definition.middle_angle(i_middle_line, j_middle_line)
        i2_middle_line=min(i_middle_line[j_middle_line<=j_list[i_list==int(h_center)][0]])
        plt.plot([i_middle_line[-1],i2_middle_line], [0,j_middle_line[i_middle_line==i2_middle_line][0]],'-',color='black')
        plt.text(i2_middle_line-35, j_middle_line[i_middle_line==i2_middle_line][0]-20, 'Angle='+str(round(middle_angle_degree[0],2)), color="black", fontsize=font_size)

    #vertical center
    v_center,i_mean,j_mean=criteria_definition.vertical_center(i_list,j_list)
    plt.plot([min(i_list[j_list==int(v_center)]),max(i_list[j_list==int(v_center)])],[v_center,v_center],'--',color='green')
    i_text_vertical=(min(i_list)+h_center)/2
    drop_length=abs(min(i_list[j_list==int(v_center)])-max(i_list[j_list==int(v_center)]))*conversion_factor
    plt.text(i_text_vertical, v_center+5, str(round(drop_length,3))+' cm', color="green", fontsize=font_size)

    #Center
    v_center,i_mean,j_mean=criteria_definition.vertical_center(i_list,j_list)
    x_center=((1280)*3-h_center)*conversion_factor
    y_center=v_center*conversion_factor
    plt.plot(h_center,v_center,'.',color='blue',markersize=14)
    plt.text(h_center+5, v_center+5, 'Center= [x='+str(round(x_center,3))+' cm, y='+str(round(y_center,3))+' cm]', color="blue", fontsize=font_size)

    #Save
    plt.axis('equal')
    plt.rc('xtick', labelsize=20) 
    plt.rc('ytick', labelsize=20) 
    font = {'weight' : 'normal'}
    plt.rc('font', **font)
    plt.savefig(save_address.replace('.tif','.png'))

    return(adv, rec,right_angle_point, left_angle_point, contact_line_length, x_center, y_center, middle_angle_degree[0])

