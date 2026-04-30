#!/bin/bash
set -e

source /opt/ros/jazzy/setup.bash
source /root/ros2_ws/install/setup.bash

exec ros2 launch sensor_fusion_pkg start_all.launch.py \
    imu_noise_stddev:=0.2 \
    depth_noise_stddev:=0.1