#! /bin/python3
"""
Launch file to start the following:
1. Dummy Sensors - depth and IMU

Author: Mallika Sirdeshpande
Date: 2026-04-28
"""

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
     
    # Declare launch arguments
    depth_noise_stddev = LaunchConfiguration('depth_noise_stddev', default=0.0)
    imu_noise_stddev = LaunchConfiguration('imu_noise_stddev', default=0.0)
    depth_freq = LaunchConfiguration('depth_freq', default=10.0)
    imu_freq = LaunchConfiguration('imu_freq', default=100.0)

    declare_depth_noise_stddev = DeclareLaunchArgument(
        'depth_noise_stddev',
        default_value='0.0',
        description='Std. dev. of noise added to simulated depth sensor measurements',
    )

    declare_imu_noise_stddev = DeclareLaunchArgument(
        'imu_noise_stddev',
        default_value='0.0',
        description='Std. dev. of noise added to simulated IMU measurements',
    )

    declare_depth_freq = DeclareLaunchArgument(
        'depth_freq',
        default_value='10.0',
        description='Frequency of publishing depth sensor measurements',
    )

    declare_imu_freq = DeclareLaunchArgument(
        'imu_freq',
        default_value='100.0',
        description='Frequency of publishing IMU measurements',
    )

    return LaunchDescription([
        
        declare_depth_noise_stddev,
        declare_imu_noise_stddev,
        declare_depth_freq,
        declare_imu_freq,

        # Dummy depth sensor
        Node(
            package='sensors_sim',
            executable='depth_sensor',
            parameters=[{
                'frequency':depth_freq,
                'noise_stddev':depth_noise_stddev
            }]
        ),

        # Dummy IMU
        Node(
            package='sensors_sim',
            executable='imu_sensor',
            parameters=[{
                'frequency':imu_freq,
                'noise_stddev':imu_noise_stddev
            }]
        ),
    ])