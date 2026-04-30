#! /bin/python3
"""
Simulate a depth sensor according to the equation: depth = 5 + 2 * sin(0.2 * t)


Author: Mallika Sirdeshpande
Date: 2026-04-28
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from math import sin
from random import gauss

class DummyDepthSensor(Node):

    def __init__(self):
        super().__init__('depth_sensor')
        self.start_time = self.get_clock().now()
        
        # Declare parameters
        self.declare_parameter('frequency', 10.0)
        self.declare_parameter('noise_stddev', 0.0)
        
        # Get parameters
        frequency = float(self.get_parameter('frequency').value)
        self.noise_stddev = float(self.get_parameter('noise_stddev').value)

        self.publisher_ = self.create_publisher(Float32, '/depth', 10)
        
        timer_period = 1/frequency
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Float32()

        t_elapsed = self.get_clock().now() - self.start_time
        t = t_elapsed.nanoseconds/1e9
        depth = self.get_depth_from_timestamp(t)
        msg.data = depth
        
        # add noise
        msg.data += gauss(0, self.noise_stddev)

        self.publisher_.publish(msg)
        # self.get_logger().info('Depth: "%f"' % msg.data)

    def get_depth_from_timestamp(self,t:float) -> float:
        """
        Calculates and returns current depth by computing
        it by plugging in current timestamp in the depth equation
        """
        return 5 + 2 * sin(0.2 * t)

def main(args=None):
    rclpy.init(args=args)
    depth_sensor = DummyDepthSensor()
    rclpy.spin(depth_sensor)
    depth_sensor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

