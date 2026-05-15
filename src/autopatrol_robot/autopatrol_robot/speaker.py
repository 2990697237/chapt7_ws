import rclpy
from rclpy.node import Node
from autopatrol_interfaces.srv import SpeachText
import espeakng

class Speaker(Node):
    def __init__(self, node_name):
        super().__init__(node_name)
        self.speech_service = self.create_service(
            SpeachText, 'speech_text', self.speak_text_callback)
        self.speaker = espeakng.Speaker()
        self.speaker.voice = 'zh'

    def speak_text_callback(self, request, response):
        self.get_logger().info('正在朗读 %s' % request.text)
        try:
            self.speaker.say(request.text)
            self.speaker.wait()
            response.result = True
        except FileNotFoundError as exc:
            self.get_logger().error(f'缺少语音引擎 espeak-ng，无法朗读: {exc}')
            response.result = False
        return response


def main(args=None):
    rclpy.init(args=args)
    node = Speaker('speaker')
    rclpy.spin(node)
    rclpy.shutdown()