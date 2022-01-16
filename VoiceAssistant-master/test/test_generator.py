from src.voice_assistant_server.stt import STT
import json
import argparse
from os import path
from pathlib import Path


class TestGenerator:
    TESTCASES_DIR = "testcases"

    def __init__(self, filepath):
        self.filepath = path.join(TestGenerator.TESTCASES_DIR, filepath + ".json")
        Path(Path(self.filepath).parent).mkdir(parents=True, exist_ok=True)
        self.stt = STT()

    def generate_testcase(self):
        try:
            with open(self.filepath, "r") as file:
                phrases = json.load(file)
        except FileNotFoundError:
            phrases = []

        while True:
            should_continue = input("Input next phrase?[yn]")
            if should_continue.lower() == "n":
                break
            else:
                phrases.append({
                    "phrase": str(self.stt.recognize()),
                                "expected_answer": None})

        with open(self.filepath,"w") as file:
            json.dump(phrases,file)

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(description="Generates a json file given voice inputs")
        parser.add_argument('--path', type=str, help='The filepath')
        args = parser.parse_args()

        test_generator = TestGenerator(args.path)
        test_generator.generate_testcase()


if __name__ == '__main__':
    TestGenerator.main()
