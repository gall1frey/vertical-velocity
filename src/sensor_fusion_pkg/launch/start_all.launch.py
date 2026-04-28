#! /bin/python3
"""
Launch file to start the following:
1. Dummy Sensors - depth and IMU
2. Sensor fusion node
3. Rosbridge server

TODO:
1. Add parameters for gaussian noise in simulated sensors
2. Move sensor nodes to another launch file
3. Add sensor fusion node

Author: Mallika Sirdeshpande
Date: 2026-04-28
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # Dummy depth sensor
        Node(
            package='sensors_sim',
            executable='depth_sensor',
        ),

        # Dummy IMU
        Node(
            package='sensors_sim',
            executable='imu_sensor',
        ),

        # Rosbridge server
        Node(
            package='rosbridge_server',
            executable='rosbridge_websocket',
            name='rosbridge_websocket',
            output='screen',
            parameters=[{'port': 9090}]
        )
    ])