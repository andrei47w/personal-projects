from random import randint
from sys import maxsize
from itertools import permutations

INF = 999999999


class Graph:
    def __init__(self):
        self.nr_vertices = 0
        self.nr_edges = 0
        self.pairs = []
        self.converted_pairs = []

    # creates new graph with specified nr_vertices, nr_edges and a matrix of pairs
    def create(self, nr_vertices, nr_edges, pairs):
        self.nr_vertices = nr_vertices
        self.nr_edges = nr_edges
        self.pairs = pairs

    # returns the pair with specified Edge_id
    def Edge_id(self, i):
        return self.pairs[i]

    # deletes the current graph in memory
    def destroy(self):
        self.nr_vertices = 0
        self.nr_edges = 0
        self.pairs = []


class Controller:
    def __init__(self):
        self.graph = Graph()
        self.file_name = ''
        self.is_copy = False

    # reads the contents of a specified file and stores it in memory
    # raises error if could not open file
    def read_new_graph(self, file_name):
        self.is_copy = False
        try:
            file = open(file_name, "r")
        except:
            raise ValueError("Could not open file!")
        self.file_name = file_name
        pairs = [[0 for x in range(3)] for y in range(sum(1 for line in file))]
        file.close()
        file = open(file_name, "r")
        i = 0
        j = 0
        nr_vertices = 0
        nr_edges = 0
        # print(file.read())

        for line in file:
            if i == int(nr_edges) + 1:
                break
            i += 1
            for number in line.split():
                j += 1
                if i == 1 and j == 1:
                    nr_vertices = number
                elif i == 1 and j == 2:
                    nr_edges = number
                else:
                    pairs[i - 2][j - 1] = int(number)
            j = 0
        file.close()
        self.graph.create(int(nr_vertices), int(nr_edges), pairs)

    # returns the number of vertices
    def get_nr_vertices(self):
        return self.graph.nr_vertices

    # returns all edges
    def get_all_edges(self):
        return self.graph.pairs

    # returns the in degree of the specified vertex
    def get_in_degree(self, x):
        count = 0
        for pair in self.graph.pairs:
            if int(pair[1]) == x:
                count += 1
        return count

    # returns the out degree of the specified vertex
    def get_out_degree(self, x):
        count = 0
        for pair in self.graph.pairs:
            if int(pair[0]) == x:
                count += 1
        return count

    # checks if there is an edge between the 2 specified vertices
    # returns its Edge_id if there is one, None otherwise
    def edge_check(self, x, y):
        for i in range(int(self.graph.nr_edges)):
            if int(self.graph.pairs[i][0]) == int(x) and int(self.graph.pairs[i][1]) == int(y):
                return i
        return None

    # checks if there is currently a graph stored in memory
    def is_graph(self):
        try:
            if self.graph.nr_vertices == 0:
                raise ValueError('')
        except:
            raise ValueError("There is no graph in memory!")

    # returns outbound edges of a specified vertex by their Edge_it, None otherwise
    def get_outbound_edges(self, x):
        id_list = []
        for i in range(int(self.graph.nr_edges)):
            if int(self.graph.pairs[i][0]) == int(x):
                id_list.append(i)
        if not id_list:
            return None
        return id_list

    # checks if the Edge_id is valid
    def validate_id(self, id):
        if id < 0 or id >= int(self.graph.nr_edges):
            raise ValueError("Invalid Edge_id!")

    # checks if the vertex is valid
    def validate_vertex(self, x):
        if x < 0 or x >= int(self.graph.nr_vertices):
            raise ValueError("Invalid vertex!")

    # returns inbound edges of a specified vertex by their Edge_it, None otherwise
    def get_inbound_edges(self, x):
        id_list = []
        for i in range(int(self.graph.nr_edges)):
            if int(self.graph.pairs[i][1]) == int(x):
                id_list.append(i)
        if not id_list:
            return None
        return id_list

    # returns the endpoints if an edge using its Edge_id
    def get_endpoints(self, id):
        self.validate_id(id)
        return self.graph.Edge_id(id)

    # modifies an edges cost after checking if it's valid
    def modify_cost(self, id, new_cost):
        self.validate_id(id)
        self.graph.pairs[id][2] = new_cost

    # removes an edge using its Edge_id only if it's valid, updating the other Edge_ids
    def remove_edge(self, id):
        self.validate_id(id)
        self.graph.nr_edges -= 1
        self.graph.pairs.remove(self.graph.Edge_id(id))

    # adds a new edge after checking if the new values are valid and increments the number of vertices
    def add_edge(self, x, y, cost):
        self.validate_vertex(x)
        self.validate_vertex(y)
        self.graph.nr_edges += 1
        self.graph.pairs.append([x, y, cost])

    # removes a vertex if possible and all its edges
    # updates the vertices with a larger id than the deleted one, decrementing them by 1
    # updates nr_vertices
    def remove_vertex(self, x):
        self.validate_vertex(x)
        count = 0
        ids = []
        self.graph.nr_vertices -= 1
        for i in range(self.graph.nr_edges):
            if int(self.graph.pairs[i][0]) == x or int(self.graph.pairs[i][1]) == x:
                ids.append(i)
                count += 1
            # if int(self.graph.pairs[i][0]) > x:
            #     self.graph.pairs[i][0] -= 1
            # if int(self.graph.pairs[i][1]) > x:
            #     self.graph.pairs[i][1] -= 1

        for i in range(len(ids)):
            self.graph.pairs.remove(self.graph.Edge_id(int(ids[i] - i)))
        self.graph.nr_edges -= count

    # adds a new vertex
    # the vertex's id will be nr_vertices
    def add_vertex(self):
        self.graph.nr_vertices += 1

    # saves any changes made in the memory to the file (file_name is a string)
    # or saves as new file (file_name is None)
    def save(self, file_name):
        if not file_name:
            file_name = self.file_name

        try:
            file = open(file_name, "x")
        except:
            file = open(file_name, "w")

        string = str(self.graph.nr_vertices) + ' ' + str(self.graph.nr_edges) + '\n'
        file.write(string)

        for i in range(self.graph.nr_edges - 1):
            string = str(self.graph.pairs[i][0]) + ' ' + str(self.graph.pairs[i][1]) + ' ' + str(
                self.graph.pairs[i][2]) + '\n'
            file.write(string)
        file.close()

    # generates a random graph using the given nr of vertices and edges and stores it in memory and the specified file
    def generate_random(self, file_name, vertices, edges):
        if vertices * vertices < edges:
            raise ValueError("too many edges!")

        self.is_copy = False
        try:
            file = open(file_name, "x")
        except:
            raise ValueError("File already exists!")

        string = str(vertices) + ' ' + str(edges) + '\n'
        file.write(string)

        self.graph.destroy()
        pairs = [[0 for x in range(3)] for y in range(edges)]
        vertices -= 1
        count = 0
        ok = 1
        while count != edges:
            vert1 = randint(0, vertices)
            vert2 = randint(0, vertices)
            cost = randint(-100, 100)
            for i in range(edges):
                ok = 1
                if pairs[i][0] == vert1 and pairs[i][1] == vert2:
                    ok = 0
                    break
            if ok:
                pairs[count][0] = vert1
                pairs[count][1] = vert2
                pairs[count][2] = cost
                count += 1

        self.graph.nr_edges = edges
        self.graph.nr_vertices = vertices + 1
        self.graph.create(vertices, edges, pairs)

        for i in range(self.graph.nr_edges):
            string = str(self.graph.pairs[i][0]) + ' ' + str(self.graph.pairs[i][1]) + ' ' + str(
                self.graph.pairs[i][2]) + '\n'
            file.write(string)

        file.close()

    def connected_components(self):
        viz = []  # list for not searching vertices already visited
        mega_viz = []  # list containing all subgraphs
        for vertex in range(self.graph.nr_vertices):
            temp_viz = []  # temporary subgraph
            if not vertex in viz:
                self.DFS(vertex, temp_viz)
                mega_viz.append(temp_viz)
                # print(temp_viz)
            viz.extend(temp_viz)

        return mega_viz

    def DFSUtil(self, v, visited, temp_viz):
        visited.add(v)
        temp_viz.append(v)

        # Recur for all the vertices
        for pair in self.graph.pairs:
            if pair[0] == v:
                neighbour = pair[1]
                if neighbour not in visited:
                    self.DFSUtil(neighbour, visited, temp_viz)

    def DFS(self, v, temp_viz):
        visited = set()

        self.DFSUtil(v, visited, temp_viz)

    def shortest_path(self, x, y):
        G = []
        for i in range(self.graph.nr_vertices):
            aux = []
            for j in range(self.graph.nr_vertices):
                if i == j:
                    aux.append(0)
                else:
                    aux.append(INF)
            G.append(aux)

        for i in range(self.graph.nr_edges):
            G[self.graph.pairs[i][0]][self.graph.pairs[i][1]] = self.graph.pairs[i][2]

        # self.print_solution(G)
        return self.floyd_warshall(G, int(x), int(y))

    def floyd_warshall(self, G, x, y):
        distance = list(map(lambda i: list(map(lambda j: j, i)), G))

        path = []
        for i in range(self.graph.nr_vertices):
            aux = []
            for j in range(self.graph.nr_vertices):
                if G[i][j] != INF:
                    aux.append(i)
                else:
                    aux.append(0)
            path.append(aux)

        # print(path)
        for k in range(self.graph.nr_vertices):
            for i in range(self.graph.nr_vertices):
                for j in range(self.graph.nr_vertices):
                    if distance[i][j] > distance[i][k] + distance[k][j]:
                        path[i][j] = path[k][j]
                        distance[i][j] = distance[i][k] + distance[k][j]
            # self.print_solution(distance)
            # print()
            # self.print_solution(path)
            # print()
            # print()

        # self.print_solution(path)
        # self.print_solution(distance)

        u = [0] * (self.graph.nr_vertices * self.graph.nr_vertices)
        w = []
        k = int(self.graph.nr_vertices)
        u[k] = y
        while u[k] != x:
            u[k - 1] = path[x][u[k]]
            k -= 1

        for i in range(k, k + self.graph.nr_vertices + 1):
            w.append(u[i])
            if u[i] == y:
                break

        return distance, path, w

    def print_solution(self, distance):
        for i in range(self.graph.nr_vertices):
            for j in range(self.graph.nr_vertices):
                if distance[i][j] == INF:
                    print("INF", end="   ")
                else:
                    print(distance[i][j], end="    ")
            print("   ")

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def apply_union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def kruskal(self):
        result = []
        i, e = 0, 0
        self.graph.pairs = sorted(self.graph.pairs, key=lambda item: item[2])
        parent = []
        rank = []

        for node in range(self.graph.nr_vertices):
            parent.append(node)
            rank.append(0)

        while e < self.graph.nr_vertices - 1:
            u, v, w = self.graph.pairs[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.apply_union(parent, rank, x, y)

        return result

    def converted_graph(self):
        new_graph = [[int(INF) for x in range(self.graph.nr_vertices - 1)] for y in range(self.graph.nr_vertices - 1)]
        for i in range(self.graph.nr_edges):
            new_graph[self.graph.pairs[i][0] - 1][self.graph.pairs[i][1] - 1] = self.graph.pairs[i][2]

        # print(new_graph)
        return new_graph

    def TSP(self, s):
        V = self.graph.nr_vertices - 1
        graph = self.converted_graph()
        # graph[1] = [0,5,3,0];
        path = [int(0) for x in range(self.graph.nr_vertices ** 2)]
        best_path = path
        vertex = []

        for i in range(V):
            if i != s:
                vertex.append(i)

        min_path = maxsize
        next_permutation = permutations(vertex)
        for i in next_permutation:
            path.clear()
            current_pathweight = 0

            k = s
            for j in i:
                current_pathweight += graph[k][j]
                path.append(k + 1)
                k = j
            current_pathweight += graph[k][s]
            path.append(k + 1)
            path.append(s + 1)

            if min_path > current_pathweight:
                min_path = current_pathweight
                best_path = path.copy()

        if min_path >= INF:
            return 0, 0
        return min_path, best_path

    # Kosaraju's algorithm to find strongly connected components in Python

    from collections import defaultdict

    class Graph:

        def __init__(self, vertex):
            self.V = vertex
            self.graph = defaultdict(list)

        # Add edge into the graph
        def add_edge(self, s, d):
            self.graph[s].append(d)

        # dfs
        def dfs(self, d, visited_vertex):
            visited_vertex[d] = True
            print(d, end='')
            for i in self.graph[d]:
                if not visited_vertex[i]:
                    self.dfs(i, visited_vertex)

        def fill_order(self, d, visited_vertex, stack):
            visited_vertex[d] = True
            for i in self.graph[d]:
                if not visited_vertex[i]:
                    self.fill_order(i, visited_vertex, stack)
            stack = stack.append(d)

        # transpose the matrix
        def transpose(self):
            g = Graph(self.V)

            for i in self.graph:
                for j in self.graph[i]:
                    g.add_edge(j, i)
            return g

        # Print stongly connected components
        def print_scc(self):
            stack = []
            visited_vertex = [False] * (self.V)

            for i in range(self.V):
                if not visited_vertex[i]:
                    self.fill_order(i, visited_vertex, stack)

            gr = self.transpose()

            visited_vertex = [False] * (self.V)

            while stack:
                i = stack.pop()
                if not visited_vertex[i]:
                    gr.dfs(i, visited_vertex)
                    print("")

    # Kosaraju's algorithm to find strongly connected components in Python

    from collections import defaultdict

    class Graph:

        def __init__(self, vertex):
            self.V = vertex
            self.graph = defaultdict(list)

        # Add edge into the graph
        def add_edge(self, s, d):
            self.graph[s].append(d)

        # dfs
        def dfs(self, d, visited_vertex):
            visited_vertex[d] = True
            print(d, end='')
            for i in self.graph[d]:
                if not visited_vertex[i]:
                    self.dfs(i, visited_vertex)

        def fill_order(self, d, visited_vertex, stack):
            visited_vertex[d] = True
            for i in self.graph[d]:
                if not visited_vertex[i]:
                    self.fill_order(i, visited_vertex, stack)
            stack = stack.append(d)

        # transpose the matrix
        def transpose(self):
            g = Graph(self.V)

            for i in self.graph:
                for j in self.graph[i]:
                    g.add_edge(j, i)
            return g

        # Print stongly connected components
        def print_scc(self):
            stack = []
            visited_vertex = [False] * (self.V)

            for i in range(self.V):
                if not visited_vertex[i]:
                    self.fill_order(i, visited_vertex, stack)

            gr = self.transpose()

            visited_vertex = [False] * (self.V)

            while stack:
                i = stack.pop()
                if not visited_vertex[i]:
                    gr.dfs(i, visited_vertex)
                    print("")

    from collections import defaultdict


    # dfs
    def dfs(self, d, visited_vertex):
        visited_vertex[d] = True
        print(d, end='')
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.dfs(i, visited_vertex)

    def fill_order(self, d, visited_vertex, stack):
        visited_vertex[d] = True
        for i in self.graph[d]:
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)
        stack = stack.append(d)

    # transpose the matrix
    def transpose(self):
        g = Graph(self.get_nr_vertices())

        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        return g

    # Print stongly connected components
    def print_scc(self):
        stack = []
        visited_vertex = [False] * (self.V)

        for i in range(self.V):
            if not visited_vertex[i]:
                self.fill_order(i, visited_vertex, stack)

        gr = self.transpose()

        visited_vertex = [False] * (self.V)

        while stack:
            i = stack.pop()
            if not visited_vertex[i]:
                gr.dfs(i, visited_vertex)
                print("")

    g = Graph(8)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(2, 4)
    g.add_edge(3, 0)
    g.add_edge(4, 5)
    g.add_edge(5, 6)
    g.add_edge(6, 4)
    g.add_edge(6, 7)

    print("Strongly Connected Components:")
    g.print_scc()

