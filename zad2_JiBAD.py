import queue

class Graph:

    # Konstruktor
    # vertexes to lista wierzchołków (stringów), a edges to lista krotek postaci (wierzchołek_1, wierzchołek_2)
    def __init__(self, vertexes, edges):
        self.vertexes = vertexes
        self.edges = edges

    # Funkcja ta dodaje wierzchołki do grafu, list_of_vertexes to lista wierzchołków do dodania
    def add_vertexes(self, list_of_vertexes):
        for ver in list_of_vertexes:
            ver = str(ver)
            if ver not in self.vertexes:
                self.vertexes.append(ver)

    # Funkcja ta dodaje krawędzie do grafu, jako argument podajemy listę krotek krawędzi.
    def add_edges(self, list_of_edges):
        k = len(list_of_edges)
        for j in range(k):
            edge_1 = list_of_edges[j][0]
            edge_2 = list_of_edges[j][1]
            edge = (edge_1, edge_2)
            edge_prim = (edge_2, edge_1)
            if edge not in self.edges and edge_prim not in self.edges and edge_1 in self.vertexes and\
                    edge_2 in self.vertexes:
                self.edges.append(edge)

    # Argument vertexes_to_remove to lista wierzchołków, które chcemy usunąć z grafu. Funkcja ta usuwa wierzchołek wraz
    # z przyległymi krawędziami
    def del_vertexes(self, vertexes_to_remove):
        k = len(vertexes_to_remove)
        for j in range(k):
            self.vertexes.remove(vertexes_to_remove[j])
        while k>=0:
            for ver in vertexes_to_remove:
                for edge in self.edges:
                    if ver in edge:
                        edge_1 = edge[0]
                        edge_2 = edge[1]
                        self.edges.remove(edge)
                        if edge_1 in self.vertexes:
                            self.vertexes.remove(edge_1)
                        elif edge_2 in self.vertexes:
                            self.vertexes.remove(edge_2)
                        k = k+1
            k = k-1
            if k<0:
                for edge in self.edges:
                    edge_1 = edge[0]
                    edge_2 = edge[1]
                    self.vertexes.extend([edge_1, edge_2])

        if len(self.edges) < len(self.vertexes)-1:
            raise Exception("Graph is not connected!")

    # Jeżeli usunięta krawędź pozostawia samotny wierzchołek, to automatycznie jest on także usuwany. Argument
    # list_of_edges w poniższej funkcji to lista krawędzi (krotek).
    def del_edges(self, list_of_egdes):
        A = [i[0] for i in list_of_egdes]
        B = [i[1] for i in list_of_egdes]
        for a in A:
            if a not in self.vertexes:
                A.remove(a)
        for b in B:
            if b not in self.vertexes:
                B.remove(b)

        for a in A:
            for b in B:
                if (a, b) in self.edges:
                    self.edges.remove((a, b))
                    first_vertex_list = [i[0] for i in self.edges]
                    second_vertex_list = [i[1] for i in self.edges]
                    if (a not in first_vertex_list and a not in second_vertex_list):
                        self.vertexes.remove(a)
                    if (b not in first_vertex_list and b not in second_vertex_list):
                        self.vertexes.remove(b)
                elif (b, a) in self.edges:
                    self.edges.remove((b, a))
                    first_vertex_list = [i[0] for i in self.edges]
                    second_vertex_list = [i[1] for i in self.edges]
                    if (b not in first_vertex_list and b not in second_vertex_list):
                        self.vertexes.remove(b)
                    if (a not in first_vertex_list and a not in second_vertex_list):
                        self.vertexes.remove(a)

        if len(self.edges) < len(self.vertexes)-1:
            raise Exception("Graph is not connected!")

    # Funkcja pobierająca sąsiadów wierzchołka vertex
    def get_neighbors(self, vertex):
        vertex = str(vertex)
        neighbors = set()
        if vertex in self.vertexes:
            edge_1 = [i[0] for i in self.edges]
            edge_2 = [i[1] for i in self.edges]
            for j in range(len(edge_1)):
                if vertex == edge_1[j]:
                    neighbors.add(edge_2[j])
            for j in range(len(edge_2)):
                if vertex == edge_2[j]:
                    neighbors.add(edge_1[j])
        else:
            print("Vertex is not included in the vertexes list")
        return neighbors

    def bfs(self, start_vertex):
        start_vertex = str(start_vertex)

        # Kolejka FIFO - First In First Out
        que = queue.Queue()
        visited_vertexes = [start_vertex]
        que.put(start_vertex)
        while que.empty() == False:
            actual_vertex = que.get()

            for vertex in self.get_neighbors(actual_vertex):
                if vertex not in visited_vertexes:
                    que.put(vertex)
                    visited_vertexes.append(vertex)
        return visited_vertexes.__iter__()

    def dfs(self, start_vertex):
        start_vertex = str(start_vertex)
        # Kolejka LIFO - Last In First Out
        que = queue.LifoQueue()
        visited_vertexes = []
        que.put(start_vertex)
        while que.empty() == False:
            vertex = que.get()
            if vertex not in visited_vertexes:
                visited_vertexes.append(vertex)
                L = [ver for ver in self.get_neighbors(vertex) if ver not in visited_vertexes]
                for ver in L:
                    que.put(ver)
        return visited_vertexes.__iter__()



if __name__ == '__main__':
    vertexes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']

    # Przykładowe drzewo do przeszukania
    edges = [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'e'), ('b', 'f'), ('c', 'g'), ('c', 'h'),
             ('d', 'i'), ('d', 'j'), ('e', 'k'), ('g', 'l')]
    graph = Graph(vertexes, edges)
    result_dfs = graph.dfs('a')
    result_bfs = graph.bfs('a')
    try:
        print("Visited vertexes in DFS: ")
        while True:
            a = result_dfs.__next__()
            print(a)
    except StopIteration:
        pass

    try:
        print("Visited vertexes in BFS: ")
        while True:
            a = result_bfs.__next__()
            print(a)
    except StopIteration:
        pass

