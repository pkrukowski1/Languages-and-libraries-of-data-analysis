from collections import defaultdict
# 1/3 pliku to komentarze
# Funkcja przyjmująca jako argument listę wzorców, na bazie których tworzy automat Aho-Corasicka
def build(patterns):
    j = len(patterns)

    # Bez utraty ogólności załóżmy, że poszukujemy jednie małych liter
    for k in range(j):
        patterns[k] = patterns[k].lower()   # właśnie Pan utracił ogólność

    # Wprowadzamy górne ograniczenie na maksymalną liczbę stanów. Jest to supremum zbioru
    # wszystkich możliwych wzorców, ponieważ w pesymistycznych danych wejściowych wszystkie litery
    # mogą być różne. Wtedy stanów będzie dokładnie tyle, co max_states.
    max_states = sum([len(pattern) for pattern in patterns])

    # Zakładamy, że symbole pochodzą ze zbioru {a,b,c,d,e,...,z}. Odrzucamy wszelkie pozostałe symbole.
    # Przedstawiona implementacja nie pozwala na załączenie innych symboli.
    max_char = 26   # a to czemu?

    # Tworzymy wektor pełniący rolę odwzorowania s -> wartość_stanu, gdzie s jest stanem, do którego
    # przechodzimy po wczytaniu z taśmy ostatniej litery badanego wzorca. Natomiast wartość_stanu to
    # liczba w systemie dziesiętnym, której postać binarna ma długość równą liczbie wzorców z listy
    # wzorców (w razie potrzeby można dorobić zera przed liczbą, bo np. w systemie binarnym, i nie tylko w systemie binarnym,
    # 0010 = 10). Ponadto pomiędzy bitami tej liczby, a indeksami wzorców z listy wzorców istnieje jednoznaczna
    # odpowiedniość. W liczbie tej wstawiamy bit równy 1 na i-tym miejscu, jeżeli do stanu s doprowadziło
    # nas wczytanie z taśmy ostatniej litery i-tego wzorca z listy wzorców. Inicjalizujemy zerami.
    # W ten sposób gromadzimy informacje na temat słów, które kończą się w stanie s i wiemy, które dokładnie
    # są to słowa!
    out = [0]*(max_states + 1)

    # Wektor pełniący rolę odwzorowania s1 -> s2, gdzie s1 oraz s2 są stanami oraz
    # s2 jest stanem, do którego prowadzi wczytanie z taśmy ostatniej litery najdłuższego sufiksu wzorca, którego
    # wczytanie ostatniej litery prowadzi do stanu s1. Uwzględniamy root, dodając jedynkę. Inicjalizujemy minus jedynkami.
    # Tak naprawdę mogłaby być to inna wartość, byleby nie zero. Chodzi o to, by posiadać informację o tym, w
    # których miejscach nasza struktura danych się "kończy".
    failLink = [-1] * (max_states + 1)  # przeszedł Pan ze snake_case na camelCase

    # Definiujemy macierz przejścia (tak naprawdę listę dwuwymiarową), która pełni rolę odwzorowania
    # (s1, l) -> s2, gdzie s1 i s2 są stanami, a l to litera z alfabetu. Interpretacja: po odczytaniu litery l z taśmy
    # przechodzimy ze stanu s1 do stanu s2. Podobnie inicjalizujemy "-1" i uwaga taka, jak w powyższym komentarzu.
    transitionMatrix = [[-1] * max_char for _ in range(max_states+1)]

    # Inicjalizacja, zakładamy, że mamy tylko stan 0.
    states = 1

    # Budujemy strukturę Trie - wypełniamy transistionMatrix. Iterujemy się po każdym słowie, a następnie iterujemy
    # po każdej literze z tego słowa. Potem przechodzimy do kolejnego słowa i kolejnych liter etc.
    for k in range(j):  # czy j jest czytelną nazwą?
        pattern = patterns[k]
        current_state = 0
        for symbol in pattern:

            # ch pełni rolę indeksu kolumny transitionMatrix, odejmujemy 97, ponieważ litera 'a' ma w ASCII kod 97.
            # Dzięki temy liczymy indeksy od zera.
            ch = ord(symbol) - 97

            # Jeżeli nie istnieje taki stan, to go tworzymy i przypisujemy wartość ze states, którą to
            # później inkrementujemy.
            if transitionMatrix[current_state][ch] == -1:
                transitionMatrix[current_state][ch] = states
                states += 1
            current_state = transitionMatrix[current_state][ch]

        # Dodajemy wzorzec do wektora out, korzystając z operatorów binarnych. W systemie dziesiętnym 1 << k ma
        # warość równą 2^k, a w systemie binarnym jest to równe liczbie 100...0, gdzie zer jest dokładnie k-1.
        # Operator | to operator binarny OR. Jeżeli w dwóch składowych wyrażenia poniżej po prawej stronie
        # bit 0 natrafi na bit 1 (czyli na informację o tym, że jakieś słowo kończy się w danym stanie), to zero
        # takie zostanie zamienione na 1, dzięki czemu stale gromadzimy informacje, nie nadpisując jej i
        # jednocześnie zachowując jednoznaczność rozkodowania i zakodowania takiej informacji.
        out[current_state] = out[current_state] | (1 << k)

    # Dla wszystkich liter z alfabetu dodajemy krawędzie łączące z rootem.
    for ch in range(max_char):
        if transitionMatrix[0][ch] == -1:
            transitionMatrix[0][ch] = 0

    # Deklarujemy kolejkę, która posłuży nam do wypełnienia failLink.
    que = []
    for ch in range(max_char):
        if transitionMatrix[0][ch] != 0:
            failLink[transitionMatrix[0][ch]] = 0
            que.append(transitionMatrix[0][ch])
    while que:
        state = que.pop(0)

        # Tworzymy failure linki dla stanu zdjętego z kolejki stanów.
        for ch in range(max_char):

            # Jeżeli dla tego stanu i litery macierz przejścia JEST zdefiniowana, to tworzymy failure link oraz...
            if transitionMatrix[state][ch] != -1:

                # ... znajdujemy failure state dla usuwanego stanu.
                failure = failLink[state]

                # Znajdujemy stan, do którego prowadzi nas wczytanie z taśmy
                # litery najdłuższego sufiksu badanego wzorca.
                while transitionMatrix[failure][ch] == -1:
                    failure = failLink[failure]

                failure = transitionMatrix[failure][ch]
                failLink[transitionMatrix[state][ch]] = failure

                # Patrzymy, czy któryś wzorzec nie jest zagnieżdżony w innym wzorcu. Jeśli tak zmieniamy
                # bit z reprezentacji dwójkowej z zera na jedynkę w odpowiednim miejscu.
                out[transitionMatrix[state][ch]] |= out[failure]

                # Dołączamy kolejny stan do kolejki, dla której ponawiamy cały proces.
                que.append(transitionMatrix[state][ch])

    return [transitionMatrix, failLink, out, states]

def search(text, patterns, automaton):
    AhoCorasik = automaton(patterns)    # czy jest potrzeba przebudowywać automat co wyszukiwanie?
    transitionMatrix = AhoCorasik[0]
    failLink = AhoCorasik[1]
    out = AhoCorasik[2]

    # Funkcja zwracająca kolejny stan po wczytaniu litery next_input ze stanu current_state
    def next_state(current_state, next_input):
        answer = current_state
        ch = ord(next_input) - 97  # Ascii value of 'a' is 97
        while transitionMatrix[answer][ch] == -1:
            answer = failLink[answer]

        return transitionMatrix[answer][ch]

    text = text.lower()

    # Przeszukiwanie zrealizujemy używając BFS (przeszukiwanie wszerz). Zaczynamy od roota.
    current_state = 0
    result = defaultdict(list)


    for i in range(len(text)):
        current_state = next_state(current_state, text[i])

        # Jeżeli wczytanie litery ze słowa text w i-tej iteracji prowadzi nas do błędnego stanu,
        # to przechodzimy do i+1 iteracji
        if out[current_state] == 0:
            continue
        for j in range(len(patterns)):
            if (out[current_state] & (1 << j)) > 0:
                pattern = patterns[j]
                result[pattern].append(i - len(pattern) + 1)
    return result


if __name__ == "__main__":
    patterns = ['abaa', 'baa', 'baccaa', 'ca']
    text = 'abaabaaaabbababaccacaaa'

    for word in search(text, patterns, build):
        for i in search(text, patterns, build)[word]:   # wielokrotne przeszukanie
            print("Wzorzec", word, "pojawia się od", i, "do", i + len(word) - 1)
            
