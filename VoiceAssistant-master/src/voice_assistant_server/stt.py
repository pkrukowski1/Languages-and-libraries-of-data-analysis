import string
import speech_recognition as sr


class STT:
    LISTENING_ANNOUNCEMENT = "Słucham..."
    SPEECH_UNRECOGNIZED_ANNOUNCEMENT = "Nie rozumiem, spróbuj powtórzyć"

    def recognize(self) -> string:
        r = sr.Recognizer()

        while True:
            with sr.Microphone() as source:
                print(STT.LISTENING_ANNOUNCEMENT)
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
                try:
                    text = r.recognize_google(audio, language='pl_PL')
                    print(text)
                    return text
                except sr.UnknownValueError:
                    print(STT.SPEECH_UNRECOGNIZED_ANNOUNCEMENT)
                except sr.RequestError as e:
                    print('error:', e)

    @staticmethod
    def main():
        stt = STT()
        print(stt.recognize())


if __name__ == "__main__":

    STT.main()
