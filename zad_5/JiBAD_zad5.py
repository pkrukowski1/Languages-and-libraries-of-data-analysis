from math import ceil
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from prettytable import PrettyTable

class kNN:

    def __init__(self, data, K, distance):
        self.data = data
        self.K = K
        self.distance = distance


    # Argumentami jest vector, czyli wektor wartości, na których będziemy operować oraz label, czyli klasa, do której
    # ten wektor należy
    def train(self, vector, label):
        """Funkcja rozbudowująca zbiór przypadków uczących"""
        data_frame = pd.read_csv(self.data, delim_whitespace=True, header=None)
        keys = [i for i in range(vector.shape[0]+1)]
        values = [vector[i] for i in range(vector.shape[0])] + [int(label)]
        new_row = {key:value for (key, value) in zip(keys, values)}
        data_frame = data_frame.append(new_row, ignore_index=True)
        data_frame.to_csv(self.data, index=False, sep = ' ', header=False)

    def calculate_euclidean_distance(self, vector_1, vector_2):
        """Funkcja licząca odległość Euklidesa pomiędzy dwoma wektorami"""
        sum_of_squares = np.sum(np.square(vector_1-vector_2))
        return np.sqrt(sum_of_squares)

    def calculate_taxicab_distance(self, vector_1, vector_2):
        """Funkcja licząca odległość taksówkową pomiędzy dwoma wektorami"""
        return np.sum(np.abs(vector_1-vector_2))

    def calculate_maximum_distance(self, vector_1, vector_2):
        """Funkcja licząca odległość maximum pomiędzy dwoma wektorami"""
        vector_of_difference = np.abs(vector_1-vector_2)
        return np.amax(vector_of_difference)

    def calculate_cosine_distance(self, vector_1, vector_2):
        """Funkcja licząca odległosć cosinusową pomiędzy dwoma wektorami"""
        return np.dot(vector_1, vector_2) / (np.sqrt(np.dot(vector_1, vector_1) * np.dot(vector_2, vector_2)))

    def predict(self, vector_to_predict_class):
        """Funkcja predykująca klasę dla wprowadzanego wektora"""
        X_train = kNN.split_data(self)["X_train"]
        y_train = kNN.split_data(self)["y_train"]

        # Distances to słownik, którego kluczami są id wierszy data frame'u, a wartościami odległości pomiędzy
        # wektorami z data frame'u (bez klas), a wektorem vector_to_predict_class
        distances = dict()
        for i in X_train.index:
            distances.update({i+1:self.distance(self, np.array(X_train.loc[i]), vector_to_predict_class)})

        sorted_distances = sorted(distances.items(), key=lambda kv: kv[1])
        sorted_distances = {key:value for (key, value) in sorted_distances[:self.K]}
        labels = dict()
        key_list = list(sorted_distances.keys())
        for i in range(self.K):
            labels.update({key_list[i]:y_train[key_list[i]-1]})
        #print(labels)
        if sum(labels.values()) >= ceil(self.K/2):
            #kNN.train(self, vector_to_predict_class, int(1))
            return 1
        else:
            #kNN.train(self, vector_to_predict_class, int(0))
            return 0

    def split_data(self):
        """Funkcja dzieląca dataset na zbiór testowy oraz treningowy"""
        data_frame = pd.read_csv(self.data, delim_whitespace=True, header=None)

        # Dzięki temu możemy obsłużyć w ten sam sposób wiele Data Frame'ów, pod warunkiem, że kolumna Class
        # będzie dołączona jako ostatnia kolumna z prawej strony
        df_without_classess = data_frame.iloc[:, 0:(data_frame.shape[1] - 1)]
        classess = data_frame.iloc[:, data_frame.shape[1] - 1]
        X_train, X_test, y_train, y_test = train_test_split(df_without_classess, classess,
                                                            test_size = 0.05, random_state = 42)
        return {"X_train":X_train, "X_test":X_test, "y_train":y_train, "y_test":y_test}

    def calculate_accuracy(self):
        """Funkcja licząca dokładność algorytmu kNN na zbiorze testowym"""
        X_test = kNN.split_data(self)["X_test"]
        y_test = np.array(kNN.split_data(self)["y_test"])
        y_pred = [kNN.predict(self, np.array(X_test.loc[i])) for i in X_test.index]
        y_pred = np.array(y_pred)
        TP = kNN.calculate_TP(self, y_test, y_pred)
        TN = kNN.calculate_TN(self, y_test, y_pred)
        FP = kNN.calculate_FP(self, y_test, y_pred)
        FN = kNN.calculate_FN(self, y_test, y_pred)
        return (TP+TN)/(TP+TN+FP+FN)


    def calculate_TP(self, array_of_true_classess, array_of_predicted_classess):
        """Funkcja zwracająca liczbę przypadków True Positive"""
        if len(array_of_predicted_classess) == len(array_of_true_classess):
            length = len(array_of_true_classess)
            TP = 0
            for i in range(length):
                if array_of_true_classess[i] == 1 and array_of_predicted_classess[i] == 1:
                    TP += 1
            return TP
        else:
            print("Proszę sprawdzić wymiary wektorów")

    def calculate_TN(self, array_of_true_classess, array_of_predicted_classess):
        """Funkcja zwracająca liczbę przypadków True Negative"""
        if len(array_of_predicted_classess) == len(array_of_true_classess):
            length = len(array_of_true_classess)
            TN = 0
            for i in range(length):
                if array_of_true_classess[i] == 0 and array_of_predicted_classess[i] == 0:
                    TN += 1
            return TN
        else:
            print("Proszę sprawdzić wymiary wektorów")

    def calculate_FP(self, array_of_true_classess, array_of_predicted_classess):
        """Funkcja zwracająca liczbę przypadków False Positive"""
        if len(array_of_predicted_classess) == len(array_of_true_classess):
            length = len(array_of_true_classess)
            FP = 0
            for i in range(length):
                if array_of_true_classess[i] == 0 and array_of_predicted_classess[i] == 1:
                    FP += 1
            return FP
        else:
            print("Proszę sprawdzić wymiary wektorów")

    def calculate_FN(self, array_of_true_classess, array_of_predicted_classess):
        """Funkcja zwracająca liczbę przypadków False Negative"""
        if len(array_of_predicted_classess) == len(array_of_true_classess):
            length = len(array_of_true_classess)
            FN = 0
            for i in range(length):
                if array_of_true_classess[i] == 1 and array_of_predicted_classess[i] == 0:
                    FN += 1
            return FN
        else:
            print("Proszę sprawdzić wymiary wektorów")

class interface:

    def __init__(self):
        self.options = {1: "Metryka euklidesowa", 2: "Metryka taksówkowa", 3: "Metryka maximum",
                        4: "Metryka cosinusowa", 5: "Zakończ działanie programu"}

    def choose_distance(self):
        """Funkcja pozwalająca użytkownikowi wybrać metrykę do algorytmu kNN"""
        while True:
            print("Wybierz funkcję odległości")
            for k in range(1, len(self.options) + 1):
                print(f"{k}. {self.options.get(k)}")
            decision = int(input("> "))
            if decision == 1:
                distance = kNN.calculate_euclidean_distance
                return distance
            elif decision == 2:
                distance = kNN.calculate_taxicab_distance
                return distance
            elif decision == 3:
                distance = kNN.calculate_maximum_distance
                return distance
            elif decision == 4:
                distance = kNN.calculate_cosine_distance
                return distance
            elif decision == 5:
                exit(0)
            else:
                print("Podaj poprawną wartość")


if __name__ == '__main__':
    # distance = interface().choose_distance()
    # knn_1_3 = kNN("dataset1.csv", 3, distance)
    # knn_1_5 = kNN("dataset1.csv", 5, distance)
    # knn_1_10 = kNN("dataset1.csv", 10, distance)
    # knn_2_3 = kNN("dataset2.csv", 3, distance)
    # knn_2_5 = kNN("dataset2.csv", 5, distance)
    # knn_2_10 = kNN("dataset2.csv", 10, distance)
    #
    # print(knn_1_3.calculate_accuracy())
    # print(knn_1_5.calculate_accuracy())
    # print(knn_1_10.calculate_accuracy())
    # print(knn_2_3.calculate_accuracy())
    # print(knn_2_5.calculate_accuracy())
    # print(knn_2_10.calculate_accuracy())

    table = PrettyTable(["Dataset", "K", "Metric", "Accuracy"])
    table.add_row(["dataset1.csv", "3", "Euclidean", "0.98"])
    table.add_row(["dataset1.csv", "5", "Euclidean", "0.98"])
    table.add_row(["dataset1.csv", "10", "Euclidean", "0.98"])
    table.add_row(["dataset1.csv", "3", "Maximum", "0.98"])
    table.add_row(["dataset1.csv", "5", "Maximum", "0.98"])
    table.add_row(["dataset1.csv", "10", "Maximum", "1"])
    table.add_row(["dataset2.csv", "3", "Euclidean", "0.948"])
    table.add_row(["dataset2.csv", "5", "Euclidean", "0.962"])
    table.add_row(["dataset2.csv", "10", "Euclidean", "0.972"])
    table.add_row(["dataset2.csv", "3", "Maximum", "0.954"])
    table.add_row(["dataset2.csv", "5", "Maximum", "0.96"])
    table.add_row(["dataset2.csv", "10", "Maximum", "0.968"])

    print(table)

