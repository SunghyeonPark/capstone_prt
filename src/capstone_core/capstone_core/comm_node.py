import rclpy
from rclpy.node import Node
from capstone_msgs.msg import ControlCmd
import paho.mqtt.client as mqtt
import json

MQTT_BROKER = '192.168.0.xxx'  # 실제 브로커 IP로 교체
MQTT_PORT = 1883
MQTT_TOPIC = 'rc/control'

class CommNode(Node):
    def __init__(self):
        super().__init__('comm_node')
        self.sub = self.create_subscription(ControlCmd, '/cmd_control', self.callback, 10)
        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT)
        self.client.loop_start()

    def callback(self, msg):
        payload = json.dumps({
            'steering': msg.steering,
            'throttle': msg.throttle
        })
        self.client.publish(MQTT_TOPIC, payload)

def main(args=None):
    rclpy.init(args=args)
    node = CommNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
