#!/usr/bin/env python3

import rospy
import numpy as np
from math import pi, radians

from geometry_msgs.msg import Twist
from sensor_msgs import LaserScan

class TurtleBot:
    errorSignal_2 = 0
    errorSignal_1 = 0
    errorSignal = 0
    def __init__(self):#Initialization script
        rospy.init_node('wall_follower',anonymous=True)#Starts node called 'wall_follower'
        self.lidar_data = rospy.Subscriber("/scan", LaserScan,callback=self.percieve)#Subsrciber object that listens for LaserScan type messages from "/scan". It will then use the percieve method to process the message
        self.turtle_bot_move = rospy.Publisher("/cmd_vel",Twist,queue_size=10)#Publisher object that publishes a Twist type message to "/cmd_vel" and has a queue buffer with size of 10
        self.move_msg=Twist
    def percieve(self, lidarData):
        self.left_wall = Wall(15,165,30,lidarData)
        self.right_wall = Wall(195,345,30,lidarData)
    def controller(self):
        TARGET=0
        ## PID GAINS ##
        P_GAIN = 1
        I_GAIN = 0
        D_GAIN = 0
        K_ONE = P_GAIN + I_GAIN + D_GAIN#Gains for discrete PID
        K_TWO = -P_GAIN + -2 * D_GAIN
        K_THREE = D_GAIN
        ## Error Signals##
        errorSignal_2 = errorSignal_1#Errors for discrete PID
        errorSignal_1 = errorSignal
        errorSignal = TARGET - self.left_wall-self.right_wall
        ##Output Signal##
        output=errorSignal * K_ONE + errorSignal_1 * K_TWO + errorSignal_2 * K_THREE#output signal for discrete PID
        return output
    def forward(self):
        #Twist message for linear velocity components so turtlebot only drives forward
        self.move_msg.linear.x=0.15
        self.move_msg.linear.y=0.0
        self.move_msg.linear.z=0.0
    def steer(self):
        self.move_msg.angular.x=0.0
        self.move_msg.angular.y=0.0
        self.move_msg.angular.z= self.controller
    def drive(self)
        self.forward
        self.steer

class Wall:
    def __init__(self,minAngle,maxAngle,samples,data):
        self.minAngle = minAngle#Defines the starting angle of a sweep
        self.maxAngle = maxAngle#Defines the end angle of a sweep for walls
        self.samples = samples#Defines how many data points to capture in each sweep
        self.datapoints = []#Creates empty list to store datapoints
        iterator=(self.maxAngle-self.minAngle)/self.samples#Determines size of iterator to go through entire angle sweep
        for x in iterator:
            self.datapoints.append(data.ranges[self.minAngle+x])#Appends range data to end of list
        self.average = np.mean(self.datapoints)#Calculates mean of datapoints
        self.variance = np.var(self.datapoints)#Calculates variance of datapoints