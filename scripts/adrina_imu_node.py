#!/usr/bin/env python
import rospy
import socket
from adrina_imu.msg import IMU
from adrina_imu.srv import SetZero


class Controller:
    def __init__(self):
        self.publisher = rospy.Publisher(
            '/adrina_imu/data', IMU, queue_size=10)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', 8888))

        self.offsets = [0, 0, 0]
        self.current = [0, 0, 0]       
        self.started = False 

    def set_zero(self):
        self.offsets[0] = self.current[0]
        self.offsets[1] = self.current[1]
        self.offsets[2] = self.current[2]

    def process(self):        
        output = IMU()

        message = ""
        
        try:
            message, _ = self.socket.recvfrom(1024)
        except socket.error as err:
            rospy.logerr(err)
            
        if not (message.startswith('$BEGIN') and message.endswith(';')):
            return
        
        message = message[7:-1]
        parts = message.split(',')

        output.yaw = int(parts[0]) - self.offsets[0]
        output.pitch = int(parts[1]) - self.offsets[1]
        output.roll = int(parts[2]) - self.offsets[2]

        self.current = [output.yaw, output.pitch, output.roll]
        if not self.started:
            self.started = True
            self.set_zero()

        self.publisher.publish(output)

    def close(self):
        self.socket.close()


if __name__ == "__main__":
    rospy.init_node('adrina_img', anonymous=True)

    name = rospy.get_name()
    rospy.loginfo("Starting adrina_imu as " + name)

    controller = Controller()
    try:
        while not rospy.is_shutdown():
            controller.process()
    except KeyboardInterrupt:
        rospy.logerr("Keyboard exception")
        controller.close()
    except rospy.ROSException:
        rospy.logerr("ROS exception")
        controller.close()
