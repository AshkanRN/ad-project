import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout

from collections import deque

from priority_queue import PriorityQueue
from passenger_class import *


class Node:
    def __init__(self, vertex, cost, capacity, start_time, end_time):
        self.vertex = vertex
        self.cost = cost
        self.capacity = capacity
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return f"(to: {self.vertex}, cost: {self.cost}, cap: {self.capacity}, time: {self.start_time}-{self.end_time})"


class Graph:
    def __init__(self):
        self.adj_list = {}
        self.passenger_info = {}
        self.current_size = 0
        self.G = nx.Graph()
        self.passenger_queue = PassengerQueue()
        # self.edges = set()

    def add_vertex(self):
        self.adj_list[self.current_size] = []
        print(f"\nVertex {self.current_size} Created.")
        self.G.add_node(self.current_size)
        self.current_size += 1

    def add_edge(self, u, v, cost, capacity, start_time, end_time):

        if any(edge.vertex == v for edge in self.adj_list[u]):
            self.adj_list[u] = [edge for edge in self.adj_list[u] if edge.vertex != v]
            self.adj_list[v] = [edge for edge in self.adj_list[v] if edge.vertex != u]

        self.adj_list[u].append(Node(v, cost, capacity, start_time, end_time))
        self.adj_list[v].append(Node(u, cost, capacity, start_time, end_time))

        self.G.add_edge(min(u, v), max(u, v), weight = cost, capacity = capacity,
                        start_time = start_time, end_time = end_time)

        # self.edges.add((min(u, v), max(u, v), cost, capacity, start_time, end_time))


    def display_vertices(self):
        if self.current_size == 0:
            print("\nEMPTY\n")
            return
        print()
        for i in range(self.current_size):
            print(f"Vertex: {i}")


    def print_graph(self):
        if self.current_size == 0:
            print("\nEMPTY\n")
            return

        for u in range(self.current_size):
            i = 0
            print(f"V{u} :", end=" ")

            for edge in self.adj_list[u]:
                if i == len(self.adj_list[u]) - 1 :
                    print(edge, end=" ")
                else:
                    print(edge, end=" -> ")
                i += 1

            print("")


    def display_passengers(self):
        if not self.passenger_info:
            print("\nNO Passenger Yet.")
            return

        # print(self.passenger_info)
        for name,edge in self.passenger_info.items():
            print(f"{name}: {edge} ")

    def display_mst_edges(self, mst_edges):

        pos = graphviz_layout(self.G, prog='sfdp')
        plt.figure(figsize=(14, 12))

        edge_colors = []
        for u, v in self.G.edges:
            if (u, v) in mst_edges or (v, u) in mst_edges:
                edge_colors.append('red')
            else:
                edge_colors.append('gray')

        plt.figure(figsize=(10, 8))
        nx.draw(
            self.G, pos,
            with_labels=True,
            node_color='skyblue',
            node_size=900,
            font_size=14,
            edge_color=edge_colors,
            width=2,
        )

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels=edge_labels,
            font_size=12,
            label_pos=0.5,
            rotate=False
        )

        plt.title("MST Result")
        plt.show()

    def mst_prim(self):
        if self.current_size == 0:
            print("Graph is Empty")
            return

        visited = [False] * self.current_size
        all_components = []
        total_cost = 0

        for start_vertex in range(self.current_size):
            if visited[start_vertex]:
                continue

            pq = PriorityQueue()
            component_edge = []
            component_cost = 0

            visited[start_vertex] = True

            for edge in self.adj_list[start_vertex]:
                pq.enqueue(edge.vertex, edge.cost, start_vertex)

            while not pq.is_empty():
                node = pq.dequeue()
                u = node.parent
                v = node.vertex
                cost = node.weight

                if visited[v]:
                    continue

                visited[v] = True
                component_edge.append((u, v, cost))
                component_cost += cost

                for edge in self.adj_list[v]:
                    if not visited[edge.vertex]:
                      pq.enqueue(edge.vertex, edge.cost, v)

            all_components.append((component_edge, component_cost))
            total_cost += component_cost

        # print(all_components)

        mst_edges = set()
        component_num = 1
        # all_component: [ ([(0, 3, 4), (3, 4, 6)], 10), ([(1, 5, 2), (5, 2, 5)], 7) ]
        for component in all_components:
            # component: ( [(0, 3, 4), (3, 4, 6)], 10)
            edges, cost = component
            # edges: [ (0, 3, 4), (3, 4, 6) ]  , cost: 10

            print(f"\nComponent {component_num} MST:")
            for u, v, c in edges:
                print(f"{u} -- {v} (cost: {c})")
                mst_edges.add((min(u, v), max(u, v)))

            print(f"Total cost of component {component_num}: {cost}")
            component_num += 1

        print(mst_edges)
        self.display_mst_edges(mst_edges)


    def shortest_path(self, src, dest=None):
        if src not in self.adj_list:
            print("\nsrc vertex does not exist")
            return None

        if dest not in self.adj_list:
            print("\ndest vertex does not exist")
            return None

        visited = [False] * self.current_size
        distance = [float('inf')] * self.current_size
        parent = [-1] * self.current_size

        distance[src] = 0
        pq = PriorityQueue()
        pq.enqueue(src, 0, None)

        while not pq.is_empty():
            node = pq.dequeue()
            u = node.vertex

            if visited[u]:
                continue

            visited[u] = True

            if dest is not None and u == dest:
                break

            for edge in self.adj_list[u]:
                v = edge.vertex
                cost = edge.cost

                if not visited[v] and distance[u] + cost < distance[v]:
                    distance[v] = distance[u] + cost
                    parent[v] = u
                    pq.enqueue(v, distance[v], u)

        if dest is not None:
            if distance[dest] == float('inf'):
                print(f"\nNo Path from {src} to {dest}")
                return None

            path = []
            curr = dest
            shortest_path_edges = []

            while curr != -1:
                path.append(curr)
                curr = parent[curr]

            path.reverse()

            for i in range(len(path)-1):
                shortest_path_edges.append((min(path[i], path[i+1]), max(path[i], path[i+1])))
            # print("\npath: ",path)
            print("edges: ",shortest_path_edges)
            print(f"Shortest path from {src} to {dest}: {' -> '.join(map(str, path))}")
            print(f"Total cost: {distance[dest]}")
            return shortest_path_edges
        else:
            print(f"Shortest distances from node {src}:")
            for i in range(self.current_size):
                print(f"to {i}: {distance[i]}")
            return None


    def display_graph(self):
        if self.current_size == 0:
            print("\nEMPTY\n")
            return

        pos = graphviz_layout(self.G, prog='sfdp')

        plt.figure(figsize=(14, 12))

        nx.draw(
            self.G, pos,
            with_labels=True,
            node_color='skyblue',
            node_size=900,
            font_size=14,
            edge_color='gray',
            width=2
        )

        # edge_labels = nx.get_edge_attributes(self.G, 'weight')
        edge_labels = {
            (u, v): f"{d['weight']}, {d['capacity']}"
            for u, v, d in self.G.edges(data=True)
        }
        nx.draw_networkx_edge_labels(
            self.G, pos,
            edge_labels=edge_labels,
            font_size=12,
            label_pos=0.5,
            rotate=False
        )

        plt.title("Graph Display", fontsize=16)
        plt.axis('off')
        plt.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
        plt.show()





def get_neighbours(graph, vertex):
    neighbours = [edge.vertex for edge in graph.adj_list[vertex]]
    return neighbours


def check_distance_bfs(graph, radius):
    for start in range(graph.current_size):
        visited = [False] * graph.current_size
        distance = [-1] * graph.current_size
        queue = deque()

        visited[start] = True
        distance[start] = 0
        queue.append(start)

        while queue:
            u = queue.popleft()
            for neighbour in get_neighbours(graph, u):
                if not visited[neighbour]:
                    visited[neighbour] = True
                    distance[neighbour] = distance[u] + 1

                    if distance[neighbour] > radius:
                        return False

                    queue.append(neighbour)

    return True