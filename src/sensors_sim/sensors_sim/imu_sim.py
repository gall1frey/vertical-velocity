#! /bin/python3
"""
Simulate an IMU according to the equation: depth = 5 + 2 * sin(0.2 * t)
It is assumed that the ROV is moving forward with a constant velocity, 
while its depth is given by the above equation

Pitch is calculated using slope, yaw and roll are constant

Published as a sensor_msgs.msg.Imu message at 100 Hz


Author: Mallika Sirdeshpande
Date: 2026-04-28
"""

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
import math

from random import gauss

class DummyIMU(Node):

    def __init__(self):
        super().__init__('imu')
        self.start_time = self.get_clock().now()

        # Declare parameters
        self.declare_parameter('frequency', 100.0)
        self.declare_parameter('noise_stddev', 0.0)
        
        # Get parameters
        frequency = float(self.get_parameter('frequency').value)
        self.noise_stddev = float(self.get_parameter('noise_stddev').value)
        
        self.publisher_ = self.create_publisher(Imu, '/imu/data', 10)

        timer_period = 1 / frequency
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.v = 1.0  # forward velocity (m/s)

    def timer_callback(self):
        msg = Imu()

        # Time
        t_elapsed = self.get_clock().now() - self.start_time
        t = t_elapsed.nanoseconds / 1e9

        # Depth dynamics - obtained by differentiating the sine eqtn.
        dz = 0.4 * math.cos(0.2 * t)
        ddz = -0.08 * math.sin(0.2 * t)

        # Pitch angle with noise
        theta = math.atan2(dz, self.v) + gauss(0,self.noise_stddev)

        # Pitch rate with noise
        theta_dot = (-0.08 * math.sin(0.2 * t) * self.v) / (self.v**2 + dz**2) + gauss(0,self.noise_stddev)

        # Header
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        # Orientation
        msg.orientation.w = math.cos(theta / 2)
        msg.orientation.x = 0.0
        msg.orientation.y = math.sin(theta / 2)
        msg.orientation.z = 0.0

        # Angular velocity (gyro)
        msg.angular_velocity.x = 0.0
        msg.angular_velocity.y = theta_dot
        msg.angular_velocity.z = 0.0

        # Linear acceleration (with gravity projection)
        g = 9.81
        msg.linear_acceleration.x = -g * math.sin(theta)
        msg.linear_acceleration.y = 0.0
        msg.linear_acceleration.z = ddz + g * math.cos(theta)

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    imu = DummyIMU()
    rclpy.spin(imu)
    imu.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()