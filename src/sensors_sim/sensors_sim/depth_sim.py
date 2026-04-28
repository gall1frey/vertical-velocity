#! /bin/python3
"""
Simulate a depth sensor according to the equation: depth = 5 + 2 * sin(0.2 * t)


TODO:
1. Add gaussian noise 
2. Move depth calculation to a new function?

Author: Mallika Sirdeshpande
Date: 2026-04-28
"""

import rclpy
from rclpy.node import Node

from std_msgs.msg import Float32
from math import sin

class DummyDepthSensor(Node):

    def __init__(self):
        super().__init__('depth_sensor')
        self.start_time = self.get_clock().now()
        self.publisher_ = self.create_publisher(Float32, '/depth', 10)
        frequency = 10 #Hz
        timer_period = 1/frequency
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Float32()

        t_elapsed = self.get_clock().now() - self.start_time
        t = t_elapsed.nanoseconds/1e9
        depth = 5 + 2 * sin(0.2 * t)
        msg.data = depth
        self.publisher_.publish(msg)
        # self.get_logger().info('Depth: "%f"' % msg.data)


def main(args=None):
    rclpy.init(args=args)
    depth_sensor = DummyDepthSensor()
    rclpy.spin(depth_sensor)
    depth_sensor.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

