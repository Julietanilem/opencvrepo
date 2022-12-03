#!/usr/bin/env python3


from telnetlib import TN3270E
from traceback import print_list
from turtle import width
import rospy
from geometry_msgs.msg import Twist
import rospy
from std_msgs.msg import Int16MultiArray as Array

def callback_centroide(msg):
    global centroide
    centroide = msg.data
    return 

def main():
    rospy.init_node("ejercicio02")
    rospy.Subscriber("/centroide", Array, callback_centroide)
    pub_cmd_vel = rospy.Publisher(
        "/cmd_vel", Twist, queue_size=10)
    global centroide
    loop = rospy.Rate(10)
    screenCenter= [640/2, 480/2]
    centroide=False
    myTwist = Twist()
    numPixels=0
    change =0
    while not rospy.is_shutdown():
        if centroide:
            
            if centroide[2] !=0 : 
                angular_vel  = screenCenter[0] - centroide[0] 
                if change-300>centroide[2] or change+300<centroide[2]:
                    myTwist.angular.z=angular_vel*0.001
                    print(centroide[2])
                    if int(centroide[2]/100) < 20:   
                        myTwist.linear.x = +1
                    elif int(centroide[2]/100) > 36: 
                        myTwist.linear.x = -1
                    else:
                        myTwist.linear.x = 0
                    change=centroide[2]
               
            else:
                myTwist.angular.z=0
                myTwist.linear.x = 0
            print("VEL:{}".format(myTwist.linear.x))
            pub_cmd_vel.publish(myTwist)

            loop.sleep()
    
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
