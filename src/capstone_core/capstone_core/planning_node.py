import rclpy
from rclpy.node import Node
from capstone_msgs.msg import VehicleState, ControlCmd
import numpy as np

WAYPOINTS = [
    (0.0, 0.0),
    (1.0, 0.0),
    (2.0, 0.5),
    (3.0, 0.0),
]
LOOKAHEAD_DIST = 0.5  # m
WHEELBASE = 0.25      # m, 실측값으로 교체

class PlanningNode(Node):
    def __init__(self):
        super().__init__('planning_node')
        self.sub = self.create_subscription(VehicleState, '/vehicle_state', self.callback, 10)
        self.pub = self.create_publisher(ControlCmd, '/cmd_control', 10)

    def find_target_point(self, x, y):
        for wx, wy in WAYPOINTS:
            if np.hypot(wx - x, wy - y) >= LOOKAHEAD_DIST:
                return wx, wy
        return WAYPOINTS[-1]

    def pure_pursuit(self, x, y, heading, tx, ty):
        alpha = np.arctan2(ty - y, tx - x) - heading
        ld = np.hypot(tx - x, ty - y)
        steering = np.arctan2(2 * WHEELBASE * np.sin(alpha), ld)
        return float(np.clip(steering / np.radians(30), -1.0, 1.0))

    def callback(self, msg):
        tx, ty = self.find_target_point(msg.x, msg.y)
        cmd = ControlCmd()
        cmd.steering = self.pure_pursuit(msg.x, msg.y, msg.heading, tx, ty)
        cmd.throttle = 0.4
        self.pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = PlanningNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
