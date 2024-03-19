#!/usr/bin/env python3

import rospy
import brandon_turtlebot
import numpy as np
from math import pi, radians

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan





if __name__== '__main__':
    try:
        tb=brandon_turtlebot.TurtleBot()
        print("trying")
        tb.stop()
        rospy.spin()
    except rospy.ROSInterruptException:
        tb_stop=brandon_turtlebot.TurtleBot()
        tb_stop.stop()