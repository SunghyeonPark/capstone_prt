from setuptools import setup

package_name = 'capstone_core'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/full_system.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    entry_points={
        'console_scripts': [
            'camera_node = capstone_core.camera_node:main',
            'detection_node = capstone_core.detection_node:main',
            'localization_node = capstone_core.localization_node:main',
            'planning_node = capstone_core.planning_node:main',
            'comm_node = capstone_core.comm_node:main',
        ],
    },
)
