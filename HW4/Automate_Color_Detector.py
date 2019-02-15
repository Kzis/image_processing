#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  9 18:38:20 2019

@author: nutt
"""

import numpy as np
import cv2


def HSV(src_h,src_s,src_v,color) :   
    
    # Define RGB color and convert to HSV
    if color == 'Blue' :  
        Lower_H = 90
        Upper_H = 120       
    elif color == 'Green' : 
        Lower_H = 45
        Upper_H = 80
    elif color == 'Red' :
        Lower_H = 0
        Upper_H = 5
    elif color == 'Yellow' : 
        Lower_H = 20
        Upper_H = 32
    elif color == 'Orange' : 
        Lower_H = 6
        Upper_H = 20
    
    # Lower satuation 20% of maximum
    Sat = 0.2*255

    mask_h = cv2.inRange(src_h,Lower_H,Upper_H)
    mask_s = cv2.inRange(src_s,Sat,255)  
    #mask_v = cv2.inRange(src_v,0,255)  
    
    # For red there is 2 range have to be cater
    if color == 'Red' :
        Lower_H2 = 175
        Upper_H2 = 180 
        mask_h2 = cv2.inRange(src_h,Lower_H2,Upper_H2)
        mask_h = cv2.bitwise_or(mask_h,mask_h2)
    
    # Combine Hue and Satuation mask    
    mask_hsv = cv2.bitwise_and(mask_h,mask_s)
           
    return mask_hsv

capture = cv2.VideoCapture(0)
color = input('Please specify color to detect : ')

while True :
    
    # read video frame
    ret,frame = capture.read()
    if not ret :
        break
    
    #resize 
    frame = cv2.resize(frame,(640,480))
        
    # convert BGR frame to HSV and split image to 1-channel grayscale
    frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    src_h = frame_hsv[:,:,0]
    src_s = frame_hsv[:,:,1]
    src_v = frame_hsv[:,:,2]
    
    # Create mask HSV 
    mask_hsv = HSV(src_h,src_s,src_v,color)
    
    # Color segment between original frame and mask HSV
    segment = cv2.bitwise_and(frame,cv2.cvtColor(mask_hsv,cv2.COLOR_GRAY2BGR))
    
    # show frame
    segment_h = np.hstack([frame,segment])
    cv2.imshow('Automate detect='+color,segment_h)
    
    if cv2.waitKey(1) == 27 :  # Esc = exit 
        break 

cv2.destroyAllWindows()