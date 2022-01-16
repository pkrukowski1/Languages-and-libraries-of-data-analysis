import wikipedia

class Query:
    def __init__(self, query, df):
        self.query = query
        self.df = df

    def search_for_events(self):
        index = -1
        for event in self.df['EVENT']:
            index += 1
            if self.query in event.lower():
                return self.df['DATE_TIME'].loc[index]

    def search_for_people_and_statements(self):
        wikipedia.set_lang("pl")
        result_from_wikipedia = wikipedia.summary(self.query, sentences=1)
        return result_from_wikipedia


if __name__ == '__main__':
    pass
