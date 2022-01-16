class TTS:
    def __init__(self):
        import pyttsx3 as tts
        self.engine = tts.init()

        self.engine.setProperty('volume', 0.7)
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('voice', 'polish')


    def say(self, text) -> None:
        self.engine.say(text)
        self.engine.runAndWait()

    @staticmethod
    def main():
        tts = TTS()
        tts.say("To jest test serwera mowy.")


if __name__ == "__main__":
    TTS.main()
