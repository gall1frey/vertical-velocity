#! /bin/python3
"""
Subscribe to data from IMU (/imu/data) and depth sensor (/depth)
And fuse the sensor readings to obtain vertical velocity

The way this works:
1. Compute downward linear velocity from IMU data
    - Use quaternion to find the orientation (which way is down)
    - Use linear acceleration vector projections to get 
        downward/upward linear acceleration
    - Integrate to get vertical speed
3. Use a kalman filter to fuse vertical speeds from IMU with measurements
    from depth sensor

TODO:
1. Add topics as parameters 
2. Complete this script

Author: Mallika Sirdeshpande
Date: 2026-04-29
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from sensor_msgs.msg import Imu

from .kalman_filter import KalmanFilter

class FusedData(Node):

    def __init__(self):
        super().__init__('fused_data')

        self.depth_sub = self.create_subscription(Float32,'/depth',self.depth_sensor_callback,10)
        self.depth_sub

        self.imu_sub = self.create_subscription(Imu,'/imu/data',self.imu_callback,10)
        self.imu_sub

        self.publisher_ = self.create_publisher(Float32, '/vertical_velocity', 10)
        frequency = 100  # Hz
        timer_period = 1 / frequency
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.depth_sensor_reading = None
        self.imu_reading = None

        self.ds_vel = None
        self.imu_vel = None

        self.kalman = KalmanFilter()

    def timer_callback(self):
        msg = Float32()
        # TODO: kalman stuff here
        self.publisher_.publish(msg)

    def depth_sensor_callback(self, msg):
        new_depth = msg.data
        self.ds_vel = new_depth - self.depth_sensor_reading
        self.depth_sensor_reading = new_depth

    def imu_callback(self,msg):
        self.imu_reading = msg.data

def main(args=None):
    rclpy.init(args=args)

    v_speed_node = FusedData()

    rclpy.spin(v_speed_node)

    v_speed_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()