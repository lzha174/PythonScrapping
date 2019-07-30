""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""
import copy

class Route:
    def __init__(self, capacity, index):
        self.index = index
        self.capacity = capacity
        self.tour = [] #contin a list of nodes

    def __str__(self):
        return 'route index is ' + str(self.index) + ' capcaity is ' + str(self.capacity) + ' tour is ' + str([node for node in self.tour])

    def add_city(self, node):
        self.tour.append(node)

    def meet_capacity(self):
        return len(self.tour) - 2 == self.capacity

    def len(self):
        return  len(self.tour)

    def __getitem__(self, index):
        return self.tour[index]

    def set_tour(self, tour):
        self.tour = tour;

    def get_tour(self):

        return self.tour

class Vertex:
    def __init__(self, node, index):
        self.id = node
        self.index = index
        self.adjacent = {}
        self.start_window = 0
        self.end_window = 0
        self.start_service = 0;
        self.service_time = 0;

    def add_time_attributes(self, start_window, end_window, service_time):
        self.start_window = start_window
        self.end_window = end_window
        self.service_time = service_time

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def remove_neighbor(self, neighbor):
        del self.adjacent[neighbor];

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_index(self):
        return self.index

    def get_weight(self, neighbor):

        return self.adjacent[neighbor]

    def get_closest_neighbor(self, tour, totalWeight):
        print(tour)
        minimum_wieght = 100000;
        closest_neightbor = None;
        for key in self.adjacent.keys():
            if key.get_id() in tour:
                continue;
            weight = self.adjacent[key]
            if weight < minimum_wieght:
                minimum_wieght = weight;
                closest_neightbor = key;
        totalWeight += minimum_wieght;
        return totalWeight, closest_neightbor;

    def get_neighbors(self):
        return self.adjacent.keys();

    def populate_edges(self, edges):
        for x in self.adjacent.keys():
            x_in = False
            for edge in edges:
                if x.get_id() == edge[0]:
                    x_in = True;
                    break;
            if (not x_in):
                edges.append((self.get_id(), x.get_id(), self.adjacent[x]))

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0
        self.num_edges = 0;

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        new_vertex = Vertex(node, self.num_vertices)
        self.num_vertices = self.num_vertices + 1
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def remove_edge(self, frm, to):
        self.vert_dict[frm].remove_neighbor(self.vert_dict[to])
        self.vert_dict[to].remove_neighbor(self.vert_dict[frm])


    def add_edge(self, frm, to, cost = 0, add_reverse = True):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def is_connected(self,
                     vertices_encountered = None,
                     start_vertex=None):
        """ determines if the graph is connected """
        if vertices_encountered is None:
            vertices_encountered = set()
        gdict = self.vert_dict;
        vertices = list(gdict.keys()) # "list" necessary in Python 3
        if not start_vertex:
            # chosse a vertex from graph as a starting point
            start_vertex = vertices[0]
        vertices_encountered.add(start_vertex)
        if len(vertices_encountered) != len(vertices):
            for vertex in gdict[start_vertex].get_neighbors():
                if vertex.get_id() not in vertices_encountered:
                    if self.is_connected(vertices_encountered, vertex.get_id()):
                        return True
        else:
            return True
        return False


    def find_path(self, start, end, path=None):
        """ find a path from start_vertex to end_vertex
            in graph """
        if path == None:
            path = []
        graph = self.vert_dict
        path = path + [start]
        if start == end:
            return path
        if start not in graph:
            return None
        for vertex in graph[start].get_neighbors():
            if vertex.get_id() not in path:
                extended_path = self.find_path(vertex.get_id(),
                                               end,
                                               path)
                if extended_path:
                    return extended_path
        return None

    def find_all_paths(self, start_node, end_node, path=[]):
        """ find all paths from start_vertex to
            end_vertex in graph """
        graph = self.vert_dict
        path = path + [start_node]
        if start_node == end_node:
            return [path]
        if start_node not in graph.keys():
            return []
        paths = []
        for vertex in graph[start_node].get_neighbors():
            if vertex.get_id() not in path:
                extended_paths = self.find_all_paths(vertex.get_id(),
                                                     end_node,
                                                     path)
                for p in extended_paths:
                    paths.append(p)
        return paths

    def randome_tsp(self):
        tour = [];
        total_weight = 0;
        vertices = list(self.vert_dict.keys());
        for x in vertices:
            tour.append(x);
        tour.append(vertices[0])
        for i in range(0, len(tour) - 1):
            total_weight += self.vert_dict[tour[i]].get_weight(self.vert_dict[tour[i+1]]);
        print(tour)
        print(total_weight)

    def neareast_neighbor_tsp(self, start=None):
        # construct a tour using nearest neighbor method
        # start from a, find the closet vertix
        tour = [];
        if not start:
            start = 'a';
        tour.append(start);
        node: str = start;
        total_weight = 0;
        while len(tour) < self.num_vertices:
            print('find nearest negghbor for ' + node);
            total_weight, closest_node = self.get_vertex(node).get_closest_neighbor(tour, total_weight);
            node = closest_node.get_id();
            tour.append(node);
            print(node);
        # return to the first city
        tour.append(start);
        print('node is ' + node);
        total_weight += self.get_vertex(start).get_weight(self.get_vertex(node));
        print('tour length is ' + str(total_weight))
        print('best tour is')
        print(tour)

    def greedy_tsp(self):
        tour = Graph();
        sorted_edges = self.sort_edges();
        #print(sorted_edges)
        for i in range(0, len(sorted_edges)):
            # using deepcopy to deep copy
            new_tour = copy.deepcopy(tour)
            #print('current tour is ');
            #for k in tour:
            #    print(k);
            #print('check edge ' + sorted_edges[i][0] + ' ' + sorted_edges[i][1] + ' ' + str(sorted_edges[i][2]))
            new_tour.add_edge(sorted_edges[i][0], sorted_edges[i][1], sorted_edges[i][2], False);
            new_tour.add_time_attributes(sorted_edges[i][0], self.vert_dict[sorted_edges[i][0]].start_window, self.vert_dict[sorted_edges[i][0]].end_window, self.vert_dict[sorted_edges[i][0]].service_time)
            new_tour.add_time_attributes(sorted_edges[i][1], self.vert_dict[sorted_edges[i][1]].start_window, self.vert_dict[sorted_edges[i][1]].end_window, self.vert_dict[sorted_edges[i][1]].service_time)

            #print('new tour is ');
            #for k in new_tour:
            #    print(k);
            if (len(new_tour.sort_edges()) < self.num_vertices and  (new_tour.is_degree_2() or new_tour.isCyclic())):
                continue;

            tour = copy.deepcopy(new_tour);

            if len(tour.sort_edges()) == self.num_vertices:
                print('oh yeah');
                break;
        #self.local_2_opt(new_tour);
        #print('tour is')
        #tour.print_edges()

        #print('value is ')
        #print(tour.total_weight(tour.sort_edges()))
        best_value, optimal_tour = self.tabu_v2(tour.dfs('a', 'a'))
        print('tabu on greedy is ', best_value)
        return tour

    def total_weight(self, edges):
        total_weight = 0;
        for e in edges:
            total_weight += e[2];
        return total_weight;
    def print_edges(self):
        print(self.sort_edges())

    def get_weight_sum(self, edges):
        total_weight = 0
        for i in range(0, len(edges) - 1):
            total_weight += self.get_vertex(edges[i]).get_weight(self.get_vertex(edges[i+1]))
        return total_weight

    def tabu_v2(self, edges: list, best_value=2000):
        tabu_list = []
        best_value = self.get_weight_sum(edges)
        best_edges = edges

        used_tabu = False;
        counter = 0;
        while counter < 1000:
            for i in range(0, len(edges) - 2):
                for j in range(i + 2, len(edges) - 1):
                    counter += 1
                    if counter == 1000:
                        print('best edge is ', best_edges, best_value)
                        return best_value, best_edges
                    city1 = edges[i]
                    city2 = edges[i + 1]
                    city3 = edges[j]
                    city4 = edges[j + 1]
                    new_edge1_weight = self.vert_dict[city1].get_weight(self.vert_dict[city3])
                    new_edge2_weight = self.vert_dict[city2].get_weight(self.vert_dict[city4])
                    dif = self.vert_dict[city1].get_weight(self.vert_dict[city2]) + self.vert_dict[city3].get_weight(self.vert_dict[city4])  - new_edge1_weight - new_edge2_weight
                    copy_edges = copy.deepcopy(edges)
                    if (city1, city2, city3, city4) in tabu_list and dif <= 0:
                        continue;
                    if (city1, city3, city2, city4) in tabu_list:
                        used_tabu = True;
                    if not (city1, city3, city2, city4) in tabu_list:
                        tabu_list.append((city1, city3, city2, city4));
                    #swap edges
                    copy_edges = copy.deepcopy(edges)
                    subedges = copy_edges[i+1 : j+1]
                    reverse_subedges = subedges[::-1]
                    new_edges = copy_edges[0: i+1]
                    new_edges.extend(reverse_subedges)
                    new_edges.extend(copy_edges[j+1:])
                    total_weight = self.get_weight_sum(new_edges)
                    if total_weight < best_value:
                        best_value = total_weight
                        best_edges = new_edges
                        edges = new_edges


        return best_value, best_edges

    def loop_2_opt(self, tour):
        local_improve = False;
        sorted_edges = tour.sort_edges()
        print('edges are ')
        print(sorted_edges)
        for i in range(0, len(sorted_edges) - 1):
            for j in range(i+1, len(sorted_edges)):
                copy_edges = copy.deepcopy(sorted_edges)
                city1 = sorted_edges[i][0];
                city2 = sorted_edges[i][1];
                city3 = sorted_edges[j][0];
                city4 = sorted_edges[j][1];
                if city1 != city3 and city1 != city4 and city2 != city3 and city2 != city4:
                    #swap edge
                    new_edge1_weight = self.vert_dict[city1].get_weight(self.vert_dict[city3])
                    new_edge2_weight = self.vert_dict[city2].get_weight(self.vert_dict[city4])
                    if sorted_edges[i][2] + sorted_edges[j][2] - new_edge1_weight - new_edge2_weight <= 0:
                        continue;
                    local_improve = True

                    print('remove edge ', sorted_edges[i], sorted_edges[j])
                    new_tour = copy.deepcopy(tour);
                    path1 = tour.dfs(city1, city1);
                    print(path1)
                    if path1.index(city2) > path1.index(city3) and path1.index(city3) < path1.index(city4):
                        city = city4;
                        city4 = city3;
                        city3 = city
                    if path1.index(city2) < path1.index(city3) and path1.index(city3) > path1.index(city4):
                        city = city4;
                        city4 = city3;
                        city3 = city
                    del copy_edges[copy_edges.index(sorted_edges[i])]
                    del copy_edges[copy_edges.index(sorted_edges[j])]

                    copy_edges.append((city1, city3, new_edge1_weight))
                    copy_edges.append((city2, city4, new_edge2_weight))
                    new_tour.remove_edge(city1, city2);
                    new_tour.remove_edge(city3, city4);

                    new_tour.add_edge(city1, city3, new_edge1_weight);
                    new_tour.add_edge(city2, city4, new_edge2_weight);
                    tour = copy.deepcopy(new_tour)
                    sorted_edges = copy.deepcopy(copy_edges);
                    print('2pt total weight is ', tour.total_weight(sorted_edges))
                    #for k in new_tour:
                    #    print(k);
        return local_improve, tour

    def local_2_opt(self, tour):
        # tour is a graph
        print('hahaha')
        sorted_edges = tour.sort_edges();
        total_weight = 0;
        for e in sorted_edges:
            total_weight += e[2];
        print('total weight is ', total_weight);
        print(sorted_edges);
        local_improve = True;
        while local_improve:
            local_improve, tour = self.loop_2_opt(tour)


        sorted_edges = tour.sort_edges();
        total_weight = 0;
        print(sorted_edges)
        for e in sorted_edges:
            total_weight += e[2];
        print('total weight is ', total_weight);
        path = tour.dfs('b', 'b');
        print(path)

    # A utility function to find the subset of an element i
    def find_parent(self, parent,i):
        if parent[i] == -1:
            return i
        return self.find_parent(parent,parent[i])

    # A utility function to do union of two subsets
    def union(self,parent,x,y):
        x_set = self.find_parent(parent, x)
        y_set = self.find_parent(parent, y)
        parent[x_set] = y_set

    def is_degree_2(self):
        for i in self.vert_dict.keys():
            if len(self.vert_dict[i].get_neighbors()) > 2:
                return True;
        return False;

    def sort_edges(self):
        edges = [];
        for i in self.vert_dict.keys():
            self.vert_dict[i].populate_edges(edges);
        edges.sort(key=lambda tup: tup[2])  # sorts in place
        return edges;

    def dfs(self, start, end, path=None, visited=False, parent=None):
        """ find a path from start_vertex to end_vertex
            in graph """
        if path == None:
            path = []
        graph = self.vert_dict
        path = path + [start]

        if start not in graph:
            return None
        for vertex in graph[start].get_neighbors():
            if vertex.get_id() not in path:
                extended_path = self.dfs(vertex.get_id(),
                                               end,
                                               path, visited, start)
                if extended_path:
                    return extended_path
            if vertex.get_id() == parent:
                # should not go back to its parent
                continue;
            if len(path) > 1 and vertex.get_id() == path[0]:
                #found a cycle
                return path + [path[0]]

        return None



    # The main function to check whether a given graph
    # contains cycle or not
    def isCyclic(self):

        # Allocate memory for creating V subsets and
        # Initialize all subsets as single element sets
        parent = [-1] * (self.num_vertices)

        # Iterate through all edges of graph, find subset of both
        # vertices of every edge, if both subsets are same, then
        # there is cycle in graph.
        sorted_edges = self.sort_edges();
        for edge in sorted_edges:
            x = self.find_parent(parent, self.get_vertex(edge[0]).get_index())
            y = self.find_parent(parent, self.get_vertex(edge[1]).get_index())
            if x == y:
                return True
            self.union(parent, x, y)
        print('pass')
        return False

    def add_time_attributes(self, node, start_window, end_window, service_time):
        self.vert_dict[node].add_time_attributes(start_window, end_window, service_time)

def vehicle_routing(tour: Graph, base_graph: Graph):
    tour_array = tour.dfs('a', 'a')
    tour_array = ['a', 'b', 'c', 'd', 'e', 'f', 'a']
    print('tour array is ', tour_array)
    vehicle_capacity = 3;
    routes = []
    vehicle_instance = Route(vehicle_capacity, len(routes))
    vehicle_instance.add_city('a')
    routes.append(vehicle_instance)
    initilisation_done = False
    counter = 1;
    sub_tours = []
    sub_tour = []
    sub_tours.append(sub_tour)
    while not initilisation_done:

        if len(sub_tour) < vehicle_capacity:
            sub_tour.append(tour_array[counter])
        else:

            sub_tour = list()
            sub_tours.append(sub_tour)
            sub_tour.append(tour_array[counter])
        counter +=1
        if tour_array[counter] == 'a':
            initilisation_done = True

    routes = []
    for path in sub_tours:
        route = Route(vehicle_capacity, len(routes))
        route.add_city('a')
        for city in path:
            route.add_city(city)
        route.add_city('a')
        routes.append(route)

    for r in routes:
        print(r)
        best_value, best_edges = base_graph.tabu_v2(r.get_tour())
        print('tabu v2 is ', best_value)





if __name__ == '__main__':
    g = Graph()

    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    g.add_vertex('f')
    g.add_time_attributes('a', 0, 10, 2)
    g.add_time_attributes('b', 0, 10, 3)
    g.add_time_attributes('c', 0, 20, 4)
    g.add_time_attributes('d', 0, 20, 6)
    g.add_time_attributes('e', 0, 14, 5)
    g.add_time_attributes('f', 4, 12, 3)

    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'd', 23)
    g.add_edge('a', 'f', 14)
    g.add_edge('a', 'e', 9)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('b', 'e', 15)
    g.add_edge('b', 'f', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('c', 'e', 1)
    g.add_edge('d', 'e', 6)
    g.add_edge('d', 'f', 6)
    g.add_edge('e', 'f', 9)




    #g.neareast_neighbor_tsp();
    #g.randome_tsp();
    big_tour =  g.greedy_tsp();

    vehicle_routing(big_tour, g)
