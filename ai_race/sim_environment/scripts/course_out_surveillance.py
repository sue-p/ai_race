#!/usr/bin/env python
import rospy
import dynamic_reconfigure.client
import time

from gazebo_msgs.msg import ModelStates
from std_msgs.msg import Bool

#max speed param
MAX_SPEED_W = 0.5

#Level1 Parameters
Ly = 1
Lx = 1.1
r  = 0.5
Ly_out = 3.0
Lx_out = 2.5

x = 1.6
y = 0.0

dynamic_client = None
curr_max_speed_coeff = 1.0

#for debug
def print_pose(data):
    pos = data.name.index('wheel_robot')
    print "position:" + '\n' + '\tx:' + str(data.pose[pos].position.x) + '\n' + '\ty:' + str(data.pose[pos].position.y) + '\n' + '\tz:' + str(data.pose[pos].position.z) + '\n' + " orientation:" + '\n' + '\tx:' + str(data.pose[pos].orientation.x) + '\n' + '\ty:' + str(data.pose[pos].orientation.y) + '\n' + '\tz:' + str(data.pose[pos].orientation.z) + '\n' + "\033[8A",

def dynamic_recon_callback(config):
    rospy.loginfo("Config set to {max_speed_coeff}".format(**config))
    global curr_max_speed_coeff
    curr_max_speed_coeff = config.max_speed_coeff

def xy_update(data):
    global x
    global y

    pos = data.name.index('wheel_robot')
    x = data.pose[pos].position.x
    y = data.pose[pos].position.y


def judge_course_l1():
    global dynamic_client
    global x
    global y
    #print data
    #pos = data.name.index('wheel_robot')
    #x = data.pose[pos].position.x
    #y = data.pose[pos].position.y
    #print pos
    #print x
    #print y

    course_out_flag = False

    if abs(x) >= Lx_out or abs(y) >= Ly_out:
        course_out_flag = True
    elif abs(y) <= Ly:
        if abs(x) <= Lx:
            course_out_flag = True
    elif y > Ly:
        if   (abs(x) <  (Lx - r)) and (y < (Ly + r)):
            course_out_flag = True
        elif (x >=  (Lx - r)) and ((x - (Lx - r))**2 + (y - Ly)**2 < r**2):
            course_out_flag = True
        elif (x <= -(Lx - r)) and ((x + (Lx - r))**2 + (y - Ly)**2 < r**2):
            course_out_flag = True
    elif y < -Ly:
        if   (abs(x) <  (Lx - r)) and (y > -(Ly + r)):
            course_out_flag = True
        elif (x >=  (Lx - r)) and ((x - (Lx - r))**2 + (y + Ly)**2 < r**2):
            course_out_flag = True
        elif (x <= -(Lx - r)) and ((x + (Lx - r))**2 + (y + Ly)**2 < r**2):
            course_out_flag = True

    if   (course_out_flag == True)  and (curr_max_speed_coeff != MAX_SPEED_W):
        print "OK -> wwww"
        dynamic_client.update_configuration({"max_speed_coeff":MAX_SPEED_W})
    elif (course_out_flag == False) and (curr_max_speed_coeff == MAX_SPEED_W):
        print "wwww -> OK"
        dynamic_client.update_configuration({"max_speed_coeff":1.0})


def course_out_surveillance():
    global dynamic_client
    rospy.init_node('course_out_surveillance', anonymous=True)
    dynamic_client = dynamic_reconfigure.client.Client("dynamic_recon_server_node", timeout=30, config_callback=dynamic_recon_callback)
    rospy.Subscriber("/gazebo/model_states", ModelStates, xy_update, queue_size = 10)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        judge_course_l1()
        rate.sleep()
"""
    # spin() simply keeps python from exiting until this node is stopped
      rospy.spin()
"""

if __name__ == '__main__':
    try:
        course_out_surveillance()
    except rospy.ROSInterruptException:
        pass

