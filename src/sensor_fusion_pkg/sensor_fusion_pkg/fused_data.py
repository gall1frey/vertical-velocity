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
2. Use a kalman filter to fuse vertical speeds from IMU with measurements
    from depth sensor

TODO:
1. Add topics as parameters (optional)

Author: Mallika Sirdeshpande
Date: 2026-04-29
Updated: 2026-04-30
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from sensor_msgs.msg import Imu

from .kalman_filter import KalmanFilter

import numpy as np
from scipy.spatial.transform import Rotation as R

class FusedData(Node):

    def __init__(self):
        super().__init__('fused_data')

        self.depth_sub = self.create_subscription(Float32,'/depth',self.depth_sensor_callback,10)
        self.depth_sub

        # For timing and integration purposes
        self.depth_last_time = self.get_clock().now()

        self.imu_sub = self.create_subscription(Imu,'/imu/data',self.imu_callback,10)
        self.imu_sub

        # For timing and integration purposes
        self.imu_last_time = self.get_clock().now()

        self.publisher_ = self.create_publisher(Float32, '/vertical_velocity', 10)
        frequency = 10 # Hz -> this works best as the slower of the two inputs (depth and velocity)
        
        # for callback 
        self.dt = 1 / frequency
        self.timer = self.create_timer(self.dt, self.timer_callback)

        # variables to hold most current values
        self.depth_sensor_reading = None
        self.imu_reading = None
        self.ds_vel = 0.0
        self.imu_vel = 0.0

        # Kalman filter variables
        F = np.array([[1, self.dt],
            [0, 1]])

        B = np.array([[0.5 * self.dt**2],
                    [self.dt]])

        H = np.array([[1, 0],
                    [0, 1]])

        Q = np.array([[0.01, 0],
                    [0, 0.1]])   # tune later

        R = np.array([[10, 0],
                    [0,  100]])

        P = np.eye(2)

        x0 = np.zeros((2, 1))

        self.kalman = KalmanFilter(F, B, H, Q, R, P, x0)

    def timer_callback(self):
        """
        Publisher callback
        """
        msg = Float32()
        self.kalman._prediction_step(u=self.imu_vel)
        msg.data = float(self.kalman.x[1][0])  # velocity
        self.publisher_.publish(msg)

    def depth_sensor_callback(self, msg):
        """
        Depth sensor subscriber callback

        Computes vertical velocity based on depth
        Stores current depth and current vertical velocity in
        self.depth_sensor_reading and self.ds_vel
        """
        if self.depth_sensor_reading is None:
            self.depth_sensor_reading = msg.data
            return
        
        now = self.get_clock().now()
        dt = (now - self.depth_last_time).nanoseconds / 1e9
        self.depth_last_time = now
        
        new_depth = msg.data
        self.ds_vel = (self.depth_sensor_reading - new_depth)/dt
        self.depth_sensor_reading = new_depth
        z = np.array([[self.depth_sensor_reading],
              [self.ds_vel]])
        self.kalman._update_step(z)

    def imu_callback(self,msg):
        """
        IMU subscriber callback

        Converts body frame acceleration to world frame acceleration (assume z up)
        Integrates acceleration to get vertical velocity in world frame
        Stores current reading and computed vertical velocity in
        self.imu_reading and self.imu_vel
        """
        if self.imu_reading is None:
            self.imu_reading = msg
            self.imu_last_time = self.get_clock().now()
            return
        
        now = self.get_clock().now()
        dt = (now - self.imu_last_time).nanoseconds / 1e9
        self.imu_last_time = now

        self.imu_reading = msg
        linear_accel = self.get_world_accel(self.imu_reading.orientation,self.imu_reading.linear_acceleration)

        self.imu_vel += (linear_accel[-1] - 9.81)*dt

    def get_world_accel(self,orientation,linear_accel):
        """
        Use quaternion's transform to get linear acceleration 
        in world frame
        """
        quaternion = [
            orientation.x,
            orientation.y,
            orientation.z,
            orientation.w,
        ]
        
        a_body = [
            linear_accel.x,
            linear_accel.y,
            linear_accel.z
        ]

        r = R.from_quat(quaternion)
        linear_accel_world = r.apply(a_body)
        return linear_accel_world
    

def main(args=None):
    rclpy.init(args=args)

    v_speed_node = FusedData()

    rclpy.spin(v_speed_node)

    v_speed_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()