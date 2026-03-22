from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(package='capstone_core', executable='camera_node'),
        Node(package='capstone_core', executable='detection_node'),
        Node(package='capstone_core', executable='localization_node'),
        Node(package='capstone_core', executable='planning_node'),
        Node(package='capstone_core', executable='comm_node'),
    ])
