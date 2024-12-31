#!/usr/bin/env python3

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os 
import xacro

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    pkg_name="mobile_robot_ros"
    xacro_file = os.path.join(get_package_share_directory(pkg_name), "description", "robot.urdf.xacro")

    robot_description_raw = xacro.process_file(xacro_file).toxml()

    params = {"robot_description": robot_description_raw, "use_sim_time": use_sim_time}

    rsp_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[params]
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'), 

        rsp_node
    ])
