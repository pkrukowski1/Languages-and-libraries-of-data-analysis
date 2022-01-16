class Exchange:
    '''
    Represents a single exchange of phrases, so query and answer
    '''
    def __init__(self, query, answer, time_received=None, time_answered=None):
        self.query = query
        self.answer = answer
        self.time_received = time_received
        self.time_answered = time_answered

    def to_dict(self):
        return {
            "query": self.query,
            "answer": self.answer,
            "time_received": self.time_received,
            "time_answered": self.time_answered
        }