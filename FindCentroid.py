#!/usr/bin/env python3


from telnetlib import TN3270E
from traceback import print_list
from turtle import width
import rospy
from std_msgs.msg import Int16MultiArray 
import rospy
import cv2 as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np

def callback_cam(msg):
    global image, imgExist
    imgExist=True
    bridge = CvBridge()
    image = bridge.imgmsg_to_cv2(msg, "bgr8")   
   
    return 

def main():
    rospy.init_node("ejercicio01")
    rospy.Subscriber("/hsrb/head_rgbd_sensor/rgb/image_raw", Image, callback_cam)
    pub_centroid = rospy.Publisher(
        "/centroide", Int16MultiArray, queue_size = 10) 
        
    global image,  imgExist
    image = 2
    loop = rospy.Rate(10)
   
    imgExist=False
    myArray=Int16MultiArray()
    #Funcionan
    upperYellow = np.array([50, 255, 255])
    lowerYellow = np.array([10, 70, 0])

    print(lowerYellow)
    while not rospy.is_shutdown():
        if imgExist==True:
            yellowPixelsImg = cv.inRange(image,lowerYellow, upperYellow)
            erosion_size = 5
            erosion_shape = cv.MORPH_RECT
            element = cv.getStructuringElement(erosion_shape, (2 * erosion_size + 1, 2 * erosion_size + 1),
                                            (erosion_size, erosion_size))
    
            imgDila = cv.dilate(yellowPixelsImg, element)
            yellowPixelsDetected= cv.dilate( imgDila, element)
           
            xCount = 0
            yCount=0
            colorPixelsCount=0
            for  x in range(yellowPixelsDetected.shape[0]):
                for y in range(yellowPixelsDetected.shape[1]):  
                    if yellowPixelsDetected[x,y] == 255:
                        yCount+=x
                        xCount+=y
                        colorPixelsCount+=1
            if colorPixelsCount>20:              
                centerX= int(xCount/colorPixelsCount)
                centerY= int (yCount/colorPixelsCount)
                centroid = [centerX, centerY, colorPixelsCount]
                cv.circle(image,(centerX, centerY), 4, (255, 66, 0),1)
                print("Pixeles:{} ".format(colorPixelsCount))
            else:
                centroid = [0, 0,0]
                print("No hay pixeles amarillos")
            cv.imshow("Vista amarillos", yellowPixelsDetected)
            cv.imshow("Vista normal", image)
            cv.waitKey(1)
            myArray.data = centroid
            pub_centroid.publish(myArray)
            print (centroid)


        loop.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass