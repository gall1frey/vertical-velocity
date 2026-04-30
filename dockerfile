FROM ros:jazzy-ros-core-noble

# Install dependencies and initialize rosdep
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    python3 \
    python3-pip \
    python3-colcon-common-extensions \
    python3-rosdep \
    ros-jazzy-rosbridge-server \
    python3-scipy\
    python3-numpy\
    && rm -rf /var/lib/apt/lists/*

RUN rosdep init || true && \
    rosdep update --rosdistro jazzy


# Setup environment
SHELL ["/bin/bash", "-c"]

RUN echo "source /opt/ros/jazzy/setup.bash" >> /root/.bashrc
ENV ROS_DISTRO=jazzy

# Create workspace
WORKDIR /root/ros2_ws
RUN mkdir -p src
COPY src/ ./src/
COPY --chmod=755 entrypoint.sh /root/ros2_ws/
RUN chmod +x /root/ros2_ws/entrypoint.sh

# Install dependencies of packages
RUN source /opt/ros/jazzy/setup.bash && \
    rosdep install --from-paths src --ignore-src -r -y

# Build workspace
RUN source /opt/ros/jazzy/setup.bash && \
    colcon build

# Runtime setup
RUN echo "source /root/ros2_ws/install/setup.bash" >> /root/.bashrc

WORKDIR /root/ros2_ws

CMD ["bash", "-c", "source /opt/ros/jazzy/setup.bash && source install/setup.bash && ros2 launch sensor_fusion_pkg start_all.launch.py imu_noise_stddev:=0.2 depth_noise_stddev:=0.1"]