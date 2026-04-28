import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Imu
import math


class DummyIMU(Node):

    def __init__(self):
        super().__init__('imu')

        self.start_time = self.get_clock().now()
        self.publisher_ = self.create_publisher(Imu, '/imu/data', 10)

        frequency = 100  # Hz
        timer_period = 1 / frequency
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.v = 1.0  # forward velocity (m/s)

    def timer_callback(self):
        msg = Imu()

        # Time
        t_elapsed = self.get_clock().now() - self.start_time
        t = t_elapsed.nanoseconds / 1e9

        # Depth dynamics
        dz = 0.4 * math.cos(0.2 * t)
        ddz = -0.08 * math.sin(0.2 * t)

        # Pitch angle
        theta = math.atan2(dz, self.v)

        # Pitch rate
        theta_dot = (-0.08 * math.sin(0.2 * t) * self.v) / (self.v**2 + dz**2)

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