import cv2 # importing OpenCV. use pip install opencv-python to install it
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob


MY = [28,29, 30, 31] # the list of MY numbers
# Going through each MY
for jj in range(len(MY)):
    # Looking through each MY
    image_list = sorted(glob.glob('/Users/pruthviacharya/Library/CloudStorage/OneDrive-YorkUniversity/MARCI_VIDEOS/South_Pole/MY'+str(MY[jj])+'_South_Projected/*.jpg')) # Getting a list of images for that particular MY
    date = pd.read_excel('/Users/pruthviacharya/Library/CloudStorage/OneDrive-YorkUniversity/MARCI_VIDEOS/South_Pole/MY'+str(MY[jj])+'date.xlsx') # This excel file contains the dates that were manually created
    dateLs = date['LS']/10 # Convert the excel numbers to Ls values
    cv2.namedWindow('test',cv2.WINDOW_NORMAL) # Setting up the main window to display the images
    
    # Empericaly determined best upper and lower bound for the HSV values (got super lazy and just use upper and lower bounds)
    low_H = [0,0, 0, 0]
    low_S = [0,0, 0, 0]
    low_V = [93,93, 93, 93]

    high_H = [180,180, 180,180]
    high_S = [181,181, 181, 181]
    high_V = [192,192, 192, 192]

    
    for ii in range(len(image_list)):
        if dateLs[ii] >= 205 and dateLs[ii] < 229: # Eyeballed the date when the edge of the SPSC reaches the Cryptic Terrain.
            print(dateLs[ii])
            img = cv2.imread(image_list[ii])
            img = img[344:789, 386:735] # Cropping around the Cryptic Terrain region, eyeballed it and needs to be refined more. 
            img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # Converting the image to HSV

            # Applying the in-built cv2.inRange function to filter out the desired color range
            frame_threshold = cv2.inRange(img_hsv, (low_H[jj], low_S[jj], low_V[jj]), (high_H[jj], high_S[jj], high_V[jj]))

            # Drawing contours
            contours, hierarchy = cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Extracting the contours (values between the HSV bounds))
            
            cv2.drawContours(img, contours, -1, (255, 255, 150), 5) # Drawing the contours on the image
            # Displaying the image and the mask
            cv2.imshow('test', img)
            cv2.waitKey(1)
            #cv2.imwrite(str(dateLs[ii])+'.png', img) # Saving the image
        