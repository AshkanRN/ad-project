import networkx as nx
import matplotlib.pyplot as plt

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
        self.current_size = 0
        self.G = nx.Graph()

    def add_vertex(self):
        self.adj_list[self.current_size] = []
        print(f"\nVertex {self.current_size} Created.")
        self.G.add_node(f"{self.current_size}")
        self.current_size += 1

    def add_edge(self, u, v, cost, capacity, start_time, end_time):

        self.adj_list[u] = [edge for edge in self.adj_list[u] if edge.vertex != v]
        self.adj_list[v] = [edge for edge in self.adj_list[v] if edge.vertex != u]

        self.adj_list[u].append(Node(v, cost, capacity, start_time, end_time))
        self.adj_list[v].append(Node(u, cost, capacity, start_time, end_time))

        self.G.add_edge(f"{u}", f"{v}")


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
                if i == len(self.adj_list[u]) -1 :
                    print(edge, end=" ")
                else:
                    print(edge, end=" -> ")
                i += 1

            print("")

    def shortest_path(self, src, dest):
        print(f"Shortest path from {src} to {dest} not implemented yet.")

    def display_graph(self):
        if self.current_size == 0:
            print("\nEMPTY\n")
            return

        nx.draw(self.G, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)
        plt.title("Simple Triangle Graph")
        plt.show()


