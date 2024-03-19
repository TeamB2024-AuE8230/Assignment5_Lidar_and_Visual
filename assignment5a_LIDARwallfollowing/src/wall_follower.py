#!/usr/bin/env python3

import rospy
import numpy as np
from math import pi, radians

from geometry_msgs.msg import Twist
from sensor_msgs import LaserScan
move = Twist
class TurtleBot:
    def __init__(self):#Initialization script
        rospy.init_node('wall_follower',anonymous=True)#Starts node called 'wall_follower'
        self.lidar_data = rospy.Subscriber("/scan", LaserScan,callback=self.percieve)#Subsrciber object that listens for LaserScan type messages from "/scan". It will then use the percieve method to process the message
        self.turtle_bot_move = rospy.Publisher("/cmd_vel",Twist,queue_size=10)#Publisher object that publishes a Twist type message to "/cmd_vel" and has a queue buffer with size of 10
    def percieve(self, lidarData):
        self.left_wall = Wall(15,165,30,lidarData)
        self.right_wall = Wall(195,345,30,lidarData)

class Wall:
    def __init__(self,minAngle,maxAngle,samples,data):
        self.minAngle = minAngle#Defines the starting angle of a sweep
        self.maxAngle = maxAngle#Defines the end angle of a sweep for walls
        self.samples = samples#Defines how many data points to capture in each sweep
        self.datapoints = []
        iterator=(self.maxAngle-self.minAngle)/self.samples
        for x in iterator:
            self.datapoints.append(data.ranges[self.minAngle+x])
        self.average = np.mean(self.datapoints)
        self.variance = np.var(self.datapoints)