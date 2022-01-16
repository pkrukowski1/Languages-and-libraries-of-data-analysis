from src.voice_assistant_modules.va_module import VAModule


class EchoModule(VAModule):
    @classmethod
    def get_id(cls):
        return "echo"

    def process_query(self, query: str) -> str:
        return query


if __name__ == '__main__':
    EchoModule.main()
