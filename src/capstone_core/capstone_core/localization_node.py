import rclpy
from rclpy.node import Node
from capstone_msgs.msg import Detection, VehicleState
import numpy as np
import cv2

# 캘리브레이션 후 실측값으로 교체
H = np.eye(3, dtype=np.float32)

class LocalizationNode(Node):
    def __init__(self):
        super().__init__('localization_node')
        self.sub = self.create_subscription(Detection, '/detections', self.callback, 10)
        self.pub = self.create_publisher(VehicleState, '/vehicle_state', 10)
        self.prev_x, self.prev_y = 0.0, 0.0

    def pixel_to_world(self, px, py):
        pt = np.array([[[px, py]]], dtype=np.float32)
        world = cv2.perspectiveTransform(pt, H)
        return float(world[0][0][0]), float(world[0][0][1])

    def callback(self, msg):
        wx, wy = self.pixel_to_world(msg.px, msg.py)
        dx = wx - self.prev_x
        dy = wy - self.prev_y

        state = VehicleState()
        state.x = wx
        state.y = wy
        state.heading = float(np.arctan2(dy, dx))
        state.velocity = float(np.hypot(dx, dy))
        self.pub.publish(state)

        self.prev_x, self.prev_y = wx, wy

def main(args=None):
    rclpy.init(args=args)
    node = LocalizationNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
