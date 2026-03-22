import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from capstone_msgs.msg import Detection
from cv_bridge import CvBridge
import cv2

class DetectionNode(Node):
    def __init__(self):
        super().__init__('detection_node')
        self.sub = self.create_subscription(Image, '/image_raw', self.callback, 10)
        self.pub = self.create_publisher(Detection, '/detections', 10)
        self.bridge = CvBridge()
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.aruco_params = cv2.aruco.DetectorParameters()

    def callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        corners, ids, _ = cv2.aruco.detectMarkers(frame, self.aruco_dict, parameters=self.aruco_params)

        if ids is not None:
            for i, corner in enumerate(corners):
                det = Detection()
                det.id = int(ids[i][0])
                det.px = float(corner[0][:, 0].mean())
                det.py = float(corner[0][:, 1].mean())
                det.width = 0.0
                det.height = 0.0
                self.pub.publish(det)

def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
