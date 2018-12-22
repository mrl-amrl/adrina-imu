cmake_minimum_required(VERSION 2.8.3)
project(adrina_imu)

find_package(catkin REQUIRED
    rospy
    std_msgs
    message_generation
)

add_message_files(
  FILES
  IMU.msg
)

generate_messages()

catkin_package(

)

include_directories(

)
