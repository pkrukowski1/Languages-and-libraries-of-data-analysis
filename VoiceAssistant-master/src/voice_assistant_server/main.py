from src.voice_assistant_server.stt import STT
from src.voice_assistant_server.tts import TTS
from src.voice_assistant_server.va_server import VAServer
from src.config.network_config import DEFAULT_BROKER

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Server for the voice assistant')
    parser.add_argument('--broker', type=str, help='The IP to use as the MQTT broker', default=DEFAULT_BROKER)
    args = parser.parse_args()
    broker = args.broker
    print(broker)
    stt = STT()
    tts = TTS()
    va_server = VAServer(tts_client=tts, broker=broker)
    while True:
        va_server.pub(stt.recognize())


if __name__ == "__main__":
    main()
