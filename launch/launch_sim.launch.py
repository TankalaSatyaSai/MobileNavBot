#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from ament_index_python.packages import get_package_share_directory
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
import os

def generate_launch_description():

    pkg_name="mobile_robot_ros"


    rsp= IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(pkg_name), 'launch', 'rsp.launch.py'
        )]), launch_arguments={"use_sim_time": "true", "use_ros2_control": "true"}.items()
    )

    # teleop_kbd = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource([os.path.join(
    #         get_package_share_directory(pkg_name), 'launch', 'teleop_kbd.launch.py'
    #     )]), launch_arguments={"use_sim_time": "true"}.items()
    # )

    twist_mux_params = os.path.join(get_package_share_directory(pkg_name), 'config', 'twist_mux.yaml')
    twist_mux = Node(
        package='twist_mux',
        executable='twist_mux',
        parameters=[twist_mux_params, {'use_sim_time': True}],
        remappings=[('cmd_vel_out', 'diff_cont/cmd_vel/unstamped')]
    )

    default_world=os.path.join(
        get_package_share_directory(pkg_name),
        'worlds',
        'empty.world'
    ) 

    world = LaunchConfiguration('world')

    world_arg=DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description="world to load"
    ) 

    gazebo = IncludeLaunchDescription(  
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'
        )]), launch_arguments={'gz_args': ['-r -v4 ', world], 'on_exit_shutdown': 'true'}.items()
    )

    spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=['-topic', 'robot_description', 
                   '-name', 'my_robot', 
                   '-z', '0.1'],
        output='screen'
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["diff_cont"]
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"]
    )

    gz_bridge_params = os.path.join(get_package_share_directory(pkg_name), 'config', 'gz_bridge.yaml')

    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={gz_bridge_params}',
        ]
    )

    ros_gz_image_bridge=Node(
        package='ros_gz_image',
        executable='image_bridge',
        arguments=["/camera/image_raw"]
    )


    return LaunchDescription([
        rsp, 
        # teleop_kbd,
        twist_mux,
        world_arg,
        gazebo, 
        spawn_entity,
        diff_drive_spawner,
        joint_broad_spawner,
        ros_gz_bridge,
        ros_gz_image_bridge
    ])
