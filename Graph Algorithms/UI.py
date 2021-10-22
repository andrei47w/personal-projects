from Controller import Controller

INF = 999999999


class UI:
    def __init__(self):
        self.ctrl = Controller()
        pass

    def read_file_ui(self):
        print("Give file name: ", end='')
        cmd = input()
        self.ctrl.read_new_graph(cmd)

    def print_nr_vertices(self):
        self.ctrl.is_graph()

        nr = self.ctrl.get_nr_vertices()
        if not nr:
            return
        print(nr)

    def print_menu(self):
        print("--------------------------MENU---------------------------\n"
              "0 - exit\n"
              "1 - print nr of vertices\n"
              "2 - parse the set of vertices\n"
              "3 <vertex> <vertex> - check for edge\n"
              "4 <vertex> - get in degree and out degree\n"
              "5 <vertex> - get all outbound edges\n"
              "6 <vertex> - get all inbound edges\n"
              "7 <Edge_id> - get endpoints and cost\n"
              "8 <Edge_id> <cost> - modify cost\n"
              "9 <Edge_id> - remove edge\n"
              "10 <vertex> <vertex> <cost> - add edge\n"
              "11 <vertex> - remove vertex\n"
              "12 - add vertex\n"
              "13 - create copy and only modify the graph in memory\n"
              "14 <file name> - read file\n"
              "15 <file_name> - save as\n"
              "16 <file name> <vertices> <edges> - generate random graph\n"
              "17 - print connected components (DFS)\n"
              "18 <vertex> <vertex> - print lowest cost walk between the given vertices\n"
              "19 - display minimal spanning tree\n"
              "20 - display minimum cost Hamiltonian cycle")
        if self.ctrl.graph.nr_edges == 0:
            print("------------------------NO-GRAPH--------------------------\n")
        elif self.ctrl.is_copy:
            print("-------------------------COPY----------------------------\n")
        else:
            print("-----------------------ORIGINAL--------------------------\n")

    def print_all_vertices(self):
        self.ctrl.is_graph()

        pairs = self.ctrl.get_all_edges()
        if not pairs:
            return
        for i in range(int(self.ctrl.graph.nr_edges)):
            if not pairs[i][2] == 0:
                print(i, ": ", pairs[i][0], "->", pairs[i][1], " [", pairs[i][2], "]")

    def print_if_edge(self):
        self.ctrl.is_graph()

        print("Give 1st vertex: ", end='')
        x = input()
        print("Give 2nd vertex: ", end='')
        y = input()

        Edge_id = self.ctrl.edge_check(x, y)
        if Edge_id is not None:
            print("There is an edge between", x, "and", y, "with the Edge_id of", Edge_id)
        else:
            print("There is no such edge")

    def print_degree(self):
        self.ctrl.is_graph()

        print("Give vertex: ", end='')
        x = input()

        print("In degree:", self.ctrl.get_in_degree(int(x)), "\nOut degree:", self.ctrl.get_out_degree(int(x)))

    def print_outbound_edges(self):
        self.ctrl.is_graph()

        print("Give vertex: ", end='')
        x = input()
        id_list = self.ctrl.get_outbound_edges(x)

        if id_list:
            print('\n', x, "has the following outbound edges:")
            for id in id_list:
                print(x, "->", self.ctrl.graph.Edge_id(id)[1], "    Edge_id:", id)
        else:
            print("No edges found!")

    def print_inbound_edges(self):
        self.ctrl.is_graph()

        print("Give vertex: ", end='')
        x = input()
        id_list = self.ctrl.get_inbound_edges(x)

        if id_list:
            print('\n', x, "has the following inbound edges:")
            for id in id_list:
                print(self.ctrl.graph.Edge_id(id)[0], "->", x, "    Edge_id:", id)
        else:
            print("No edges found!")

    def print_endpoints(self):
        self.ctrl.is_graph()

        print("Give Edge_id: ", end='')
        id = input()
        endpoints = self.ctrl.get_endpoints(int(id))

        if endpoints:
            print("\nThe endpoints are: ", endpoints[0], '->', endpoints[1], "with the cost of", endpoints[2])

    def modify_cost(self):
        self.ctrl.is_graph()

        print("Give Edge_id: ", end='')
        id = input()
        print("Give new cost:", end='')
        new_cost = input()
        self.ctrl.modify_cost(int(id), int(new_cost))

        if not self.ctrl.is_copy:
            self.ctrl.save(None)

    def remove_edge(self):
        self.ctrl.is_graph()

        print("Give Edge_id: ", end='')
        id = input()
        self.ctrl.remove_edge(int(id))

        if not self.ctrl.is_copy:
            self.ctrl.save(None)

    def add_edge(self):
        self.ctrl.is_graph()

        print("Give 1st vertex: ", end='')
        x = input()
        print("Give 2nd vertex: ", end='')
        y = input()
        print("Give cost: ", end='')
        cost = input()
        self.ctrl.add_edge(int(x), int(y), int(cost))

        if not self.ctrl.is_copy:
            self.ctrl.save(None)

    def remove_vertex(self):
        self.ctrl.is_graph()

        print("Give vertex: ", end='')
        x = input()
        self.ctrl.remove_vertex(int(x))

        if not self.ctrl.is_copy:
            self.ctrl.save(None)

    def add_vertex(self):
        self.ctrl.is_graph()
        self.ctrl.add_vertex()

        if not self.ctrl.is_copy:
            self.ctrl.save(None)

        print("Vertex", self.ctrl.get_nr_vertices() - 1, "was added.")

    def save_as(self):
        print("Give file name: ", end='')
        file_name = input()
        self.ctrl.save(file_name)

    def create_copy(self):
        self.ctrl.is_copy = True

    def generate_random(self):
        print("Give file name: ", end='')
        file_name = input()
        print("Give nr of vertices: ", end='')
        vertices = input()
        print("Give nr of edges: ", end='')
        edges = input()

        self.ctrl.generate_random(file_name, int(vertices), int(edges))

    def connected_components(self):
        self.ctrl.is_graph()

        mega_list = self.ctrl.connected_components()
        count = 0
        for list in mega_list:
            print()
            for elem in list:
                for pair in self.ctrl.graph.pairs:
                    if pair[2] == 0:
                        break
                    if pair[0] == elem:
                        count += 1
                        print(pair[0], "->", pair[1], " [", pair[2], "]")
            if count == 0:
                print(list[0])
            print("edges:", count, "\tvertices:", len(list))
            count = 0

    def shortest_path(self):
        self.ctrl.is_graph()
        print("Give 1st vertex: ", end='')
        x = input()
        print("Give 2nd vertex: ", end='')
        y = input()

        matrix, path, w = self.ctrl.shortest_path(x, y)
        if matrix[int(x)][int(y)] == INF:
            print("There is no path between the 2 vertices")
        else:
            print("path:", w)
            print("cost:", matrix[int(x)][int(y)])
            print("length:", path[int(x)][int(y)])

    def Kruskal(self):
        self.ctrl.is_graph()
        result = self.ctrl.kruskal()
        for pair in result:
            print(pair[0], " - ", pair[1], " [", pair[2], "]", sep='')

    def TSP(self):
        self.ctrl.is_graph()
        cost, path = self.ctrl.TSP(0)

        if cost == 0:
            print("there is no such path!")
            return

        print("path: ", end='')
        for vertex in path[:-1]:
            print(vertex, end=' -> ')
        print(path[-1])
        print("cost:", cost)

    # def TSP(self):
    #     self.ctrl.hamCycle()

    def start(self):
        while True:
            try:
                self.print_menu()
                print("Give command: ", end='')
                cmd = input()
                if cmd == '0':
                    exit()
                elif cmd == '1':
                    self.print_nr_vertices()
                elif cmd == '2':
                    self.print_all_vertices()
                elif cmd == '3':
                    self.print_if_edge()
                elif cmd == '4':
                    self.print_degree()
                elif cmd == '5':
                    self.print_outbound_edges()
                elif cmd == '6':
                    self.print_inbound_edges()
                elif cmd == '7':
                    self.print_endpoints()
                elif cmd == '8':
                    self.modify_cost()
                elif cmd == '9':
                    self.remove_edge()
                elif cmd == '10':
                    self.add_edge()
                elif cmd == '11':
                    self.remove_vertex()
                elif cmd == '12':
                    self.add_vertex()
                elif cmd == '13':
                    self.create_copy()
                elif cmd == '14':
                    self.read_file_ui()
                elif cmd == '15':
                    self.save_as()
                elif cmd == '16':
                    self.generate_random()
                elif cmd == '17':
                    self.connected_components()
                elif cmd == '18':
                    self.shortest_path()
                elif cmd == '19':
                    self.Kruskal()
                elif cmd == '20':
                    self.TSP()
                else:
                    print("There is no such command!")
            except ValueError as ve:
                print(ve)
