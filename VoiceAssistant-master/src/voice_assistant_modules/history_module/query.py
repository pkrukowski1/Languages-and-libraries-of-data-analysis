import re

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

    def search_for_dates(self):
        index = -1
        if "myślnik" in self.query:
            date = re.findall('[0-9]+', self.query)
            date = str(date[0]) + ' - ' + str(date[1])
        elif "przed naszą erą" in self.query:
            date = str(self.query.split()[-5]) + ' p.n.e.'
        else:
            date = self.query.split()[-2]
        for date_time in self.df['DATE_TIME']:
            index +=1
            if date == date_time:
                return self.df['EVENT'].loc[index]


if __name__ == '__main__':
    pass
