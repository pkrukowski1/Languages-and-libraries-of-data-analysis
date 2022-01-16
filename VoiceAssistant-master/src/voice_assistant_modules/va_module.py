import abc
from abc import ABC

import traceback

import paho.mqtt.client as mqtt

from src.config.network_config import QUERY_CHANNEL, ANSWER_CHANNEL, DEFAULT_BROKER
from src.voice_assistant_modules.exchange import Exchange
from src.voice_assistant_modules.module_observer import ModuleObserver
from src.voice_assistant_modules.timer import Timer


class VAModule(ABC):
    def __init__(self, broadcast_channel=ANSWER_CHANNEL, listen_channel=QUERY_CHANNEL, broker=DEFAULT_BROKER, timer=None):
        self.broadcast_channel = broadcast_channel
        self.listen_channel = listen_channel
        self.broker = broker
        self.id = self.__class__.get_id()
        self.client = mqtt.Client(self.id)
        self.init_client()
        self.observers = []
        self.timer = timer
        if self.timer is None:
            self.timer = Timer()

    def init_client(self):
        self.client.on_message = self.on_message

        def on_connect(client, userdata, flags, rc):
            client.subscribe(self.listen_channel + "#")

        self.client.on_connect = on_connect

        self.client.connect(self.broker)

        self.client.loop_start()

    def on_message(self, client, userdata, message):
        time_received = self.timer.get_curr_time()
        query = str(message.payload.decode("utf-8"))
        try:
            answer = self.process_query(query)
        except Exception as e:
            traceback.print_exc()
            return  # not a question we can answer
        time_answered = self.timer.get_curr_time()

        exchange = Exchange(query, answer, time_received=time_received, time_answered=time_answered)
        for observer in self.observers:
            observer.notify(exchange)

        if answer is not None:
            self.client.publish(self.broadcast_channel + self.id, answer)

    @classmethod
    def get_name(cls):
        return cls.__name__

    @classmethod
    def class_description(cls):
        return cls.get_name() + ", a VA Module implementation."

    @abc.abstractmethod
    def process_query(self, query: str) -> str:
        pass

    @classmethod
    @abc.abstractmethod
    def get_id(cls):
        pass

    def observe(self, observer: ModuleObserver):
        self.observers.append(observer)

    @classmethod
    def add_arguments(cls, parser):
        pass

    @classmethod
    def main(cls):
        import argparse
        parser = argparse.ArgumentParser(description=cls.class_description())
        parser.add_argument('--broker', type=str, help='The IP to use as the MQTT broker', default=DEFAULT_BROKER)
        parser.add_argument('--log', type=bool, help='Whether or not to log the conversations', default=False)
        cls.add_arguments(parser)  # so that the implementation can define it's own arguments
        args = parser.parse_args()
        broker = args.broker
        module = cls(broker=broker)

        if args.log:
            from ..logging.module_logger import ModuleLogger
            module_logger = ModuleLogger(module)
            module.observe(module_logger)

        import time
        time.sleep(10000)  # TODO: better solution
