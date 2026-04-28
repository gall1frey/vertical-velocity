from setuptools import find_packages, setup

package_name = 'sensors_sim'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mallika',
    maintainer_email='sirdeshpande.m@northeastern.edu',
    description='Dummy depth sensor and IMU',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'depth_sensor = sensors_sim.depth_sim:main',
            'imu_sensor = sensors_sim.imu_sim:main',
        ],
    },
)
