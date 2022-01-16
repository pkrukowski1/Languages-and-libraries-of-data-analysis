import paho.mqtt.client as mqtt
from ..config.network_config import QUERY_CHANNEL, ANSWER_CHANNEL, DEFAULT_BROKER
from .tts import TTS


class VAServer:
    ID = "pc"
    def __init__(self, broadcast_channel=QUERY_CHANNEL, listen_channel=ANSWER_CHANNEL, broker=DEFAULT_BROKER, tts_client=None):
        self.broadcast_channel = broadcast_channel
        self.listen_channel = listen_channel
        self.broker = broker
        self.tts_client = tts_client
        if self.tts_client is None:
            self.tts_client = TTS()

        self.client = mqtt.Client(VAServer.ID)
        self.init_client()

    def init_client(self):
        self.client.on_message = self.on_message
        connect_res = self.client.connect(self.broker)
        print(connect_res)

        self.client.subscribe(self.listen_channel+"#")
        self.client.loop_start()

    def pub(self, msg):
        print("Publishing:", msg)
        self.client.publish(self.broadcast_channel+VAServer.ID, msg)

    def on_message(self, _, __, message):
        message = str(message.payload.decode("utf-8"))
        print("Got answer:", message)
        self.tts_client.say(message)
