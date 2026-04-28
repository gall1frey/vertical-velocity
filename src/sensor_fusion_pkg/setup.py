from setuptools import find_packages, setup

package_name = 'sensor_fusion_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', [
            'launch/start_all.launch.py'
        ])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Mallika',
    maintainer_email='sirdeshpande.m@northeastern.edu',
    description='Fusing IMU and Depth Sensor to get vertical velocity',
    license='MIT',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'fused_data = sensor_fusion_pkg.fused_data:main'
        ],
    },
)
