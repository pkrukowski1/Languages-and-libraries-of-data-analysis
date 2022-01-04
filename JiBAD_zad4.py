import csv
from datetime import datetime, date
from datetime import timedelta
# Plik books to plik csv, którego budowa jest linijkowa, tzn. każda linijka opisuje jedną książkę w formacie
# id,tytuł_książki,imię_autora,nazwisko_autora,rok_wydania,czy_wypożyczona - czy wypożyczona przyjmuje wartości 0 (nie jest)
# lub 1 (jest wypożyczona)

# Plik books_to_be_returned to plik csv o budowie takiej samej, jak plik books.csv. Zawiera książki gotowe do zwrotu.

# Plik readers.csv to plik csv, którego budowa jest następująca: username_czytelnika,hasło (username musi być unikalny),
# konto czytelnika jest tworzone przez bibliotekarza wraz z hasłem, w związku z czym czytelnik musi zmienić hasło zaraz
# po pierwszym zalogowaniu

# Plik librarians.csv to plik, którego budowa jest następująca: username_bibliotekarza,hasło (username musi być unikalny)

# Plik reserved_books.csv to plik, którego budowa jest następująca: id_zarezerwowanej_książki,od_kiedy,do_kiedy,przez_kogo
# Daty mają format dd-mm-yyyy, przez_kogo to username odpowiedniego użytkownika.

# Plik borrowed_books.csv to plik, którego budowa jest następująca: id_wypożyczonej_książki,do_kiedy,przez_kogo -
# książki wypożyczamy na okres jednego miesiąca z możliwością prolongaty o jeden miesiąc (tylko jedna prolongata)
# zmieszczenie tego projektu w jednym pliku to zły znak
class files:    # nazwy klas raczej PascalCasem i w liczbie pojedynczej
    def __init__(self, file):
        self.file = file

    def read_csv_file(self):
        """Funkcja czytająca plik csv"""    # nazwa to mówi
        with open(self.file, 'r',encoding='UTF8', newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                yield row

    # Argument line_to_write to linia tekstu dopisywana do pliku
    def write_to_csv_file(self, line_to_write):
        """Funkcja dopisująca linię tekstu do pliku csv"""  # a tego nie mówi
        with open(self.file, 'a+', encoding='UTF8', newline='') as csv_file:
            writer_object = csv.writer(csv_file)
            writer_object.writerow(line_to_write)

    # Argument unique_value_to_delete to pierwsza wartość danego wiersza z pliku csv (która zawsze jest unikalna)
    def delete_row(self, unique_value_to_delete):
        """Funkcja usuwająca wiersz wartości z pliku csv"""
        lines = list()
        with open(self.file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                lines.append(row)
                for field in row:
                    if field == unique_value_to_delete:
                        lines.remove(row)
        with open(self.file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
    # taka obsługa pliku jest mało wydajna, może lepiej go napisać od nowa raz na jakiś czas (w tym przy zamknięciu programu?), a w czasie działania trzymać dane w pamięci?

    def clear_csv_file(self):
        """Funkcja usuwająca zawartość pliku"""
        f = open(self.file, "w")
        f.truncate()
        f.close()

class library:

    def __init__(self):
        self.log_menu_options = {"1":"Bibliotekarz", "2":"Czytelnik", "3":"Wyjście"}    # czy lista by nie była lepsza?
        self.log_as_librarian = ["Podaj login: ", "Podaj hasło: "]
        self.librarian_options = {"1":"Przyjmij zwrot książki", "2":"Dodaj nową książkę", "3":"Usuń książkę z systemu",
                                  "4":"Dodaj czytelnika", "5":"Dodaj bibliotekarza", "6":"Przeglądaj katalog",
                                  "7":"Powrót"}
        self.reader_options = {"1":"Wypożycz książkę", "2":"Zarezerwuj książkę", "3":"Prolonguj", "4":"Przeglądaj katalog",
                               "5":"Zwróć książkę", "6":"Powrót"}
        self.browsing_options = {"1":"Id", "2":"Tytuł", "3":"Imię autora", "4":"Nazwisko autora", "5":"Rok wydania"}

    def display_log_menu(self):
        """Funkcja wyświetlająca menu z opcjami logowania dla czytelnika oraz dla bibliotekarza"""
        print("Zaloguj się jako:")
        for k in range(1, len(self.log_menu_options)+1):
            print(f"{k}. {self.log_menu_options.get(str(k))}")

    def log_in_as_librarian(self, username, password):
        """Funkcja umożliwiająca zalogowanie się dla bibliotekarza"""
        lib = library()
        if lib.check_password_librarian(username, password):
            return True
        else:
            return False

    def log_in_as_reader(self, username, password):
        """Funkcja umożliwiająca zalogowanie się dla bibliotekarza"""
        lib = library()
        if lib.check_password_reader(username, password):
            return True
        else:
            return False

    def check_password_librarian(self, username, password):
        """Funkcja sprawdzająca hasło i username bibliotekarza"""
        file = files("librarians.csv").read_csv_file()
        for line in file:
            if line[0] == username and line[1] == password:
                return True
        else:
            print("Sprawdź, czy na pewno założyłeś konto, a jeśli tak, to upewnij się, że wprowadzone dane są prawidłowe")
            return False

    def check_password_reader(self, username, password):
        """Funkcja sprawdzająca hasło i username czytelnika"""
        file = files("readers.csv").read_csv_file()
        for line in file:
            if line[0] == username and line[1] == password:
                return True
        else:
            print("Sprawdź, czy na pewno założyłeś konto, a jeśli tak, to upewnij się, że wprowadzone dane są prawidłowe")
            return False

    def display_options_for_librarian(self):
        """Funkcja wyświetlająca menu z opcjami dla bibliotekarza"""
        for k in range(1, len(self.librarian_options)+1):
            print(f"{k}. {self.librarian_options.get(str(k))}")

    def display_options_for_reader(self):
        """Funkcja wyświetlająca menu z opcjami dla bibliotekarza"""
        for k in range(1, len(self.reader_options)+1):
            print(f"{k}. {self.reader_options.get(str(k))}")

    def display_browsing_options(self):
        """Funkcja wyświetlająca menu z opcjami przeszukwiania katalogu"""
        for k in range(1, len(self.browsing_options)):
            print(f"{k}. {self.browsing_options.get(str(k))}")

    def handle_menu_for_librarian(self):    # ta metoda robi za dużo, trzeba to rozbić na mniejsze, łatwiejsze do zarządzania metody
        """Funkcja zarządzająca menu dla bibliotekarza"""
        lib= librarian()
        while True:
            library.display_options_for_librarian(self) # <=> self.display_options_for_librarian()
            librarian_decision = int(input("> "))
            try:
                if librarian_decision in range(1, len(self.librarian_options) + 1):
                    librarian_decision = str(librarian_decision)
                    if self.librarian_options.get(librarian_decision) == "Przyjmij zwrot książki":
                        lib.accept_returned_book()
                    elif self.librarian_options.get(librarian_decision) == "Dodaj nową książkę":
                        counter = 3
                        while counter > 0:
                            print("Podaj tytuł")
                            title = input("> ")
                            print("Podaj imię autora - jeśli autor ma dwa imiona to podaj je oddzielone spacją")
                            name = input("> ")
                            print("Podaj nazwisko autora")
                            surname = input("> ")
                            print("Podaj rok wydania")
                            year_of_release = input("> ")
                            lib.add_book(title, name, surname, year_of_release)
                            print("Czy to wszystkie książki? Napisz T (tak) lub N (nie).")
                            end = input("> ")
                            if end == "T":
                                break
                            elif end == "N":
                                continue
                            elif end != "N" and end != "T": # czy ten warunek jest tu potrzebny, skoro dwa poprzednie były fałszywe?
                                print(f"Nieprawidłowa odpowiedź. Masz jeszcze {str(counter)} prób") # czy ta pętla działa tak jak Pan chciał?
                                counter = counter-1
                    elif self.librarian_options.get(librarian_decision) == "Usuń książkę z systemu":
                        counter = 3
                        while counter > 0:
                            print("Jaką książkę chciałbyś usunąć? Podaj jej identyfikator")
                            id_book = input("> ")
                            lib.remove_book(id_book)
                            print("Czy to wszystkie książki? Napisz T (tak) lub N (nie).")
                            end = input("> ")
                            if end == "T":
                                break
                            elif end == "N":
                                continue
                            elif end != "N" and end != "T": # mam deja vu
                                print(f"Nieprawidłowa odpowiedź. Masz jeszcze {str(counter)} prób")
                                counter = counter - 1
                    elif self.librarian_options.get(librarian_decision) == "Dodaj czytelnika":
                        counter = 3
                        while counter > 0:
                            print("Podaj username (unikatowy) czytelnika, którego chcesz dodać")
                            username = input("> ")
                            lib.add_reader(username)
                            print("Czy to wszyscy czytelnicy? Napisz T (tak) lub N (nie).")
                            end = input("> ")
                            if end == "T":
                                break
                            elif end == "N":
                                continue
                            elif end != "N" and end != "T":
                                print(f"Nieprawidłowa odpowiedź. Masz jeszcze {str(counter)} prób")
                                counter = counter - 1
                    elif self.librarian_options.get(librarian_decision) == "Dodaj bibliotekarza":
                        counter = 3
                        while counter > 0:
                            print("Podaj username (unikatowy) bibliotekarza, którego chcesz dodać")
                            username = input("> ")
                            lib.add_librarian(username)
                            print("Czy to wszyscy bibliotekarze? Napisz T (tak) lub N (nie).")
                            end = input("> ")
                            if end == "T":
                                break
                            elif end == "N":
                                continue
                            elif end != "N" and end != "T":
                                print(f"Nieprawidłowa odpowiedź. Masz jeszcze {str(counter)} prób")
                                counter = counter - 1
                    elif self.librarian_options.get(librarian_decision) == "Przeglądaj katalog":
                        library.display_browsing_options(self)
                        print("Podaj numer opcji, po której chcesz przeszukiwać katalog")
                        filter = input("> ")
                        print("Podaj frazę wyszukiwania")
                        searching = input("> ")
                        library.browse_catalog(self, filter, searching)
                    elif self.librarian_options.get(librarian_decision) == "Powrót":
                        library.run_system(self)
            except ValueError:
                print(f"Podaj liczbę od 1 do {len(self.librarian_options)}")

    def set_new_password_for_reader(self):
        """Funkcja ustawiająca hasło dla czytelnika"""
        print("Podaj username")
        username = input("> ")
        print("Podaj nowe hasło")
        password = input("> ")
        file = files("readers.csv")
        for line in file.read_csv_file():
            if line[0] == username:
                line[1] = password
                file.delete_row(username)
                file.write_to_csv_file([line[0], line[1]])
        print("Nowe hasło zostało zapisane")

    def set_new_password_for_librarian(self):
        """Funkcja ustawiająca hasło dla bibliotekarza"""
        print("Podaj username")
        username = input("> ")
        print("Podaj nowe hasło")
        password = input("> ")
        file = files("librarians.csv")
        for line in file.read_csv_file():
            if line[0] == username:
                line[1] = password
                file.delete_row(username)
                file.write_to_csv_file([line[0], line[1]])
        print("Nowe hasło zostało zapisane")

    def handle_menu_for_reader(self, username):
        """Funkcja zarządzająca menu dla czytelnika"""
        read = reader()
        while True:
            lib.display_options_for_reader()
            reader_decision = str(input("> "))
            try:
                if int(reader_decision) in range(1, len(self.reader_options)+1):
                    if self.reader_options.get(reader_decision) == "Wypożycz książkę":
                        while True:
                            print("Podaj id książki, którą chcesz wypożyczyć")
                            book_id = input("> ")
                            read.borrow_book(book_id, username)
                            print("Czy chcesz wypożyczyć jeszcze jakąś książkę? Odpowiedz T (tak) lub N (nie)")
                            answer = input("> ")
                            if answer == "T":
                                continue
                            elif answer == "N":
                                break
                            elif answer != "N" and answer != "T":
                                print("Sprawdź odpowiedzi")
                    elif self.reader_options.get(reader_decision) == "Zarezerwuj książkę":
                        while True:
                            print("Podaj id książki, którą chcesz zarezerwować")
                            book_id = input("> ")
                            read.reserve_book(book_id, username)
                            print("Czy chcesz zarezerwować jeszcze jakąś książkę? Odpowiedz T (tak) lub N (nie)")
                            answer = input("> ")
                            if answer == "T":
                                continue
                            elif answer == "N":
                                break
                            elif answer != "N" and answer != "T":
                                print("Sprawdź odpowiedzi")
                    elif self.reader_options.get(reader_decision) == "Prolonguj":
                        while True:
                            print("Podaj id książki, którą chcesz prolongować")
                            book_id = input("> ")
                            read.prolong_book(book_id, username)
                            print("Czy chcesz prolongować jeszcze jakąś książkę? Napisz T (tak) lub N (nie)")
                            answer = input("> ")
                            if answer == "T":
                                continue
                            elif answer=="N":
                                break
                            elif answer != "T" and answer != "N":
                                print("Sprawdź poprawność udzielonych odpowiedzi")
                    elif self.reader_options.get(reader_decision) == "Zwróć książkę":
                        while True:
                            print("Podaj id książki, którą zwrócić")
                            book_id = input("> ")
                            read.get_back_book(book_id)
                            print("Czy chcesz zwrócić jeszcze jakąś książkę? Odpowiedz T (tak) lub N (nie)")
                            answer = input("> ")
                            if answer == "T":
                                continue
                            elif answer == "N":
                                break
                            elif answer != "N" and answer != "T":
                                print("Sprawdź odpowiedzi")
                    elif self.reader_options.get(reader_decision) == "Przeglądaj katalog":
                        library.display_browsing_options(self)
                        print("Podaj numer opcji, po której chcesz przeszukiwać katalog")
                        filter = input("> ")
                        print("Podaj frazę wyszukiwania")
                        searching = input("> ")
                        library.browse_catalog(self, filter, searching)
                    elif self.reader_options.get(reader_decision) == "Powrót":
                        library.run_system(self)
            except ValueError:
                print(f"Podaj liczbę od 1 do {len(self.reader_options)}")

    # Filter to numer opcji, po której chcemy przefiltrować, a searching to wyszukiwana fraza
    def browse_catalog(self, filter, searching):
        """Funkcja przeszukująca katalog"""
        lib = library()
        number_of_trial = 3
        while number_of_trial>0:
            try:
                filter = int(filter)
                searching = str(searching)
                if filter in range(1, len(lib.browsing_options)+1):
                    file = files("books.csv").read_csv_file()
                    for line in file:
                        if searching in line[filter-1]:
                            print(f"Id: {line[0]}, Tytuł: {line[1]}, Imię autora: {line[2]}, Nazwisko autora: {line[3]},"
                                  f"Data wydania: {line[4]}, Dostępność: {line[5]}")
                print("Czy chcesz przestać przeglądać katalog? Odpowiedz T (tak) lub N (nie).")
                end = input("> ")
                if end == "T":
                    break
                elif end == "N":
                    continue
                elif end != "T" and end != "N":
                    print(f"Nieprawidłowa odpowiedź. Masz jeszcze {str(number_of_trial)} prób")
                    number_of_trial = number_of_trial-1
            except ValueError:
                print("Sprawdź poprawność wybranej opcji")


    def run_system(self):
        """Funkcja obsługująca system biblioteczny"""
        lib = library()
        lib.display_log_menu()
        while True:
            try:
                decision = int(input("> "))
                if decision in range(1, len(self.log_menu_options) + 1):
                    decision = str(decision)
                    if self.log_menu_options.get(decision) == "Bibliotekarz":
                        number_of_trial = 3
                        while number_of_trial>0:
                            print("Czy to Twoje pierwsze logowanie? Podaj odpowiedź T (tak) lub N (nie).")
                            first_log = input("> ")
                            if first_log == "N":
                                username = str(input("Podaj username: "))
                                password = str(input("Podaj hasło: "))
                                is_correctly_logged = lib.log_in_as_librarian(username, password)
                                if is_correctly_logged == True:
                                    lib.handle_menu_for_librarian()
                                else:
                                    number_of_trial = number_of_trial-1
                                    if number_of_trial == 0:
                                        break
                            elif first_log == "T":
                                lib.set_new_password_for_librarian()
                            elif first_log != "T" and first_log != "N":
                                print("Nieprawidłowa odpowiedź")
                    elif self.log_menu_options.get(decision) == "Czytelnik":
                        number_of_trial = 3
                        while number_of_trial > 0:
                            print("Czy to Twoje pierwsze logowanie? Podaj odpowiedź T (tak) lub N (nie).")
                            first_log = input("> ")
                            if first_log == "N":
                                username = str(input("Podaj username: "))
                                password = str(input("Podaj hasło: "))
                                is_correctly_logged = lib.log_in_as_reader(username, password)
                                if is_correctly_logged == True:
                                    lib.handle_menu_for_reader(username)
                                else:
                                    number_of_trial = number_of_trial - 1
                                    if number_of_trial == 0:
                                        break
                            elif first_log == "T":
                                lib.set_new_password_for_reader()
                    elif self.log_menu_options.get(decision) == "Wyjście":
                        exit()
            except ValueError:
                print(f"Podaj liczbę od 1 do {len(self.log_menu_options)}")

class librarian:

    def __init__(self):
        pass

    def accept_returned_book(self):
        """Funkcja przyjmująca zwroty książek"""
        file_to_open = files("books_to_be_returned.csv")
        file_to_write = files("books.csv")
        for line in file_to_open.read_csv_file():
            file_to_write.write_to_csv_file(line)
        file_to_open.clear_csv_file()

    # Argumentami są dane na temat książki
    def add_book(self, title, first_name_of_author, surname_of_author, year_of_release):
        """Funkcja dodająca nową książkę do zbioru bibliotecznego"""
        file = files("books.csv")
        new_id = str(max([int(line[0])+1 for line in file.read_csv_file()]))
        L = [new_id, title, first_name_of_author, surname_of_author, str(year_of_release), str(1)]
        if new_id not in [line[0] for line in file.read_csv_file() if len(line) > 0]:
            file.write_to_csv_file(L)
        else:
            print("Taka książka widnieje już w zbiorze bibliotecznym")

    # Argumentem jest unikalny identyfikator książki
    def remove_book(self, id_book):
        """Funkcja usuwa książkę ze zbioru bibliotecznego"""
        id_book = str(id_book)
        file = files("books.csv")
        if id_book in [line[0] for line in file.read_csv_file()]:
            file.delete_row(id_book)
        else:
            print("Taka książka nie istnieje w zbiorze bibliotecznym")

    # Argumentem jest username czytelnika
    def add_reader(self, username):
        """Funkcja dodająca czytelnika do systemu"""
        file = files("readers.csv")
        if username not in [line[0] for line in file.read_csv_file() if len(line)>0]:
            file.write_to_csv_file([username])
        else:
            print("Czytelnik o takim id widnieje już w systemie")

    # Argumentem jest username dodawanego bibliotekarza
    def add_librarian(self, username):
        """Funkcja dodająca bibliotekarza do systemu"""
        file = files("librarians.csv")  # przesłonięcie nazwy wbudowanej
        if username not in [user[0] for user in file.read_csv_file() if len(user) > 0]:
            file.write_to_csv_file([username,None])
        else:
            print("Czytelnik o takim id widnieje już w systemie")


class reader:

    def __init__(self):
        pass

    def borrow_book(self, book_id, username):
        """Funkcja umożliwia wypożyczenie książki o danym id"""
        file_1 = files("books.csv")
        file_2 = files("borrowed_books.csv")
        for line in file_1.read_csv_file():
            if line[0] == book_id and line[5] == "0":
                line[5] = "1"
                file_1.delete_row(book_id)
                file_1.write_to_csv_file(line)
                date_after_month = datetime.today() + timedelta(days=30)
                line_to_write = [line[0],date_after_month.strftime('%Y-%m-%d'), username]
                file_2.write_to_csv_file(line_to_write)
            else:
                print("Książka jest wypożyczona")

    def reserve_book(self, book_id, username):
        """Funkcja realizuje zarezerwowanie wypożyczonej książki o danym id z miesięcznym wyprzedzeniem"""
        file_1 = files("books.csv")
        file_2 = files("reserved_books.csv")
        for line in file_1.read_csv_file():
            if line[0] == book_id and line[5] == "1":
                date_after_month = datetime.today() + timedelta(days=30)
                line_to_write = [book_id,date_after_month.strftime('%Y-%m-%d'),username]
                file_2.write_to_csv_file(line_to_write)

    def prolong_book(self, book_id, username):
        """Funkcja przedłużająca wypożyczenie książki o miesiąc"""
        file = files("borrowed_books.csv")
        for line in file.read_csv_file():
            if line[2] == username and line[0] == book_id:
                date_to_write = datetime.strptime(line[2], '%Y-%m-%d') + timedelta(days=30)
                file.delete_row(book_id)
                file.write_to_csv_file([book_id, date_to_write.strftime('%Y-%m-%d'), username])
                break


    def get_back_book(self, book_id):
        """Funkcja umożliwiająca zwrot książki"""
        file_1 = files("books_to_be_returned.csv")  # czy gdyby ta metoda była dłuższa, to pod koniec by Pan wiedział co jest w file_1, a co w file_2?
        file_2 = files("borrowed_books.csv")
        file_3 = files("books.csv")
        for line in file_2.read_csv_file():
            if line[0] == book_id:
                file_2.delete_row(book_id)
                break
        for line_1 in file_3.read_csv_file():   # line, line_1 - łatwo pomylić
        # Chcemy uzyskać wszystkie informacje niezbędne do wpisania do pliku borrowed_books.csv
            if line_1[0] == book_id:
                file_1.write_to_csv_file([book_id, line_1[1], line_1[2],line_1[3], line_1[4], "0"])
                break

if __name__ == "__main__":
    lib = library()
    lib.run_system()

    # Wartości inicjalizujące bibliotekarza
    #files("librarians.csv").write_to_csv_file(["janek_kowalski", "password"])

# Operuje Pan na niskim poziomie - dużo jest myślenia o tym, gdzie co jest w pliku itp. Po to ma Pan listy, słowniki i tym podobne atrakcje, żeby takie rzeczy się robiło łatwiej i szybciej (mniej kodu).