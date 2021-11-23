from collections import deque, Counter, OrderedDict
import regex

# Zadanie nr 1

class Aho_Corasick:
    def __init__(self, patterns, text_to_search):
        self.patterns = patterns
        self.text_to_search = text_to_search
        self.automaton = []

        # Inicjalizacja roota
        self.automaton.append({'parent_node':'', 'children':[], 'failure_link':0, 'output':[]})

    def find_next_state(self, current_state, symbol):
        """ Funkcja zwracająca kolejny stan po wczytaniu danego symbolu lub zwracająca None, gdy lista
         dzieci jest pusta """
        for state in self.automaton[current_state]['children']:
            if self.automaton[state]["parent_node"] == symbol:
                return state
        return None

    def build_trie_with_failure_links(self):
        """ Funkcja buduje drzewo trie """

        # Budujemy strukturę trie
        for pattern in self.patterns:
            current_state = 0
            position_of_symbol = 0
            child = Aho_Corasick.find_next_state(self, current_state, pattern[position_of_symbol])
            while child != None:
                current_state = child
                position_of_symbol = position_of_symbol + 1
                if position_of_symbol < len(pattern):
                    child = Aho_Corasick.find_next_state(self, current_state, pattern[position_of_symbol])
                else:
                    break
            for i in range(position_of_symbol, len(pattern)):
                node = {'parent_node': pattern[i], 'children': [], 'failure_link': 0, 'output': []}
                self.automaton.append(node)
                self.automaton[current_state]["children"].append(len(self.automaton) - 1)
                current_state = len(self.automaton) - 1
            self.automaton[current_state]["output"].append(pattern)

        # Dodajemy failure linki
        q = deque()
        child = 0
        for node in self.automaton[0]["children"]:
            q.append(node)
            self.automaton[node]["failure_link"] = 0
        while q:
            r = q.popleft()
            for child in self.automaton[r]["children"]:
                q.append(child)
                state = self.automaton[r]["failure_link"]
                while Aho_Corasick.find_next_state(self, state, self.automaton[child]["parent_node"]) == None and state != 0:
                    state = self.automaton[state]["failure_link"]
                self.automaton[child]["failure_link"] = Aho_Corasick.find_next_state(self, state,
                                                               self.automaton[child]["parent_node"])
                if self.automaton[child]["failure_link"] is None:
                    self.automaton[child]["failure_link"] = 0
                    self.automaton[child]["output"] = self.automaton[child]["output"] +\
                                                      self.automaton[self.automaton[child]["failure_link"]]["output"]


    def search(self):
        """ Funkcja zwracająca indeksy wzorców występująych we wprowadzonym tekście """
        current_state = 0
        patterns_found = []
        for i in range(len(self.text_to_search)):
            while Aho_Corasick.find_next_state(self, current_state, self.text_to_search[i]) is None and current_state != 0:
                current_state = self.automaton[current_state]["failure_link"]
            current_state = Aho_Corasick.find_next_state(self, current_state, self.text_to_search[i])
            if current_state is None:
                current_state = 0
            else:
                for pattern in self.automaton[current_state]["output"]:
                    # index liczymy od 0
                    patterns_found.append({"index range": str(i - len(pattern) + 1) + " - " + str(i),
                                           "pattern": pattern})
        return patterns_found

    # Argument result to wynik poszukiwania wzorców w tekście
    def __repr__(self, result):
        """ Metoda __repr__ """
        return f"Results = {result}"


# Zadanie nr 2
# filename to wczytywany plik, a n to liczba najczęściej wyświetlanych słów wraz z ich ilością
def count_words(filename, n):
    """ Funkcja zliczająca słowa z pliku"""
    sentences = []
    try:
        with open(filename) as infile:
            WORD_RE = regex.compile(r'\w+')
            for line in infile:
                for token in WORD_RE.findall(line):
                    sentences.append(token)
        wordcount = Counter(sentences)
        count = 0
        for item in wordcount.most_common(n):
            print("{}\t{}".format(*item))
            count += 1
            # wyświetlanie remisów
            if count == n:
                reverse_sorted_values = sorted(list(wordcount.values()), reverse=True)
                while reverse_sorted_values[count] == reverse_sorted_values[count+1]:
                    print("{}\t{}".format(*item))
                    count += 1

    except IOError:
        print("Could not read file")


if __name__ == '__main__':
    aho_corasick = Aho_Corasick(['abc', 'aab', 'cba'], 'aaabcaab')
    aho_corasick.build_trie_with_failure_links()
    result = aho_corasick.search()
    print(aho_corasick.__repr__(result))

    count_words('potop.txt', 10)

