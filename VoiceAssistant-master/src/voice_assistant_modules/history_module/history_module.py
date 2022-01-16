from src.voice_assistant_modules.va_module import VAModule
from src.voice_assistant_modules.history_module.query import Query
import pandas as pd

class HistoryModule(VAModule):

    @classmethod
    def get_id(cls):
        return "history"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.df = pd.read_csv("data.csv", sep=',')


    EVENT_QUESTIONS = (
        "w którym roku odbyła się",
        "w którym roku odbył się",
        "w którym roku odbyły się",
        "kiedy był",
        "kiedy było",
        "kiedy były",
        "kiedy była",
        "kiedy zdarzyło się",
        "kiedy zdarzył się",
        "kiedy zdarzyły się",
        "kiedy zdarzyła się",
        "kiedy miało miejsce",
        "kiedy miał miejsce",
        "kiedy miały miejsce",
        "kiedy nadany został",
        "kiedy odbyło się",
        "kiedy odbyły się",
        "kiedy odbyła się",
    )

    PEOPLE_STATEMENTS_QUESTIONS = (
        "kim był",
        "kim była",
        "kim były",
        "czym jest"
    )


    def normalize_query(self, query_text):
        return query_text.lower()

    def process_query(self, query_text: str) -> str:
        query_text = self.normalize_query(query_text)
        for question in HistoryModule.EVENT_QUESTIONS:
            if query_text.startswith(question):
                query_text = query_text[len(question) + 1:]
                query = Query(query_text, self.df)
                return "W " + str(query.search_for_events()) + " roku"
        for question in HistoryModule.PEOPLE_STATEMENTS_QUESTIONS:
            if query_text.startswith(question):
                query_text = query_text[len(question) + 1:]
                query = Query(query_text, self.df)
                return str(query.search_for_people_and_statements())
        else:
            return None  # if not a history question, we can't answer it

if __name__ == '__main__':
    HistoryModule.main()