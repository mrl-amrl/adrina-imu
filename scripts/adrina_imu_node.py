import rospy

if __name__ == "__main__":
    rospy.init_node('adrina_img', anonymous=True)

    name = rospy.get_name()

    rospy.loginfo("Starting adrina_imu as " + name)