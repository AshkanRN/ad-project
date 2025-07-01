import networkx as nx
import matplotlib.pyplot as plt
from priority_queue import PriorityQueue
from networkx.drawing.nx_agraph import graphviz_layout


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

        self.G.add_edge(f"{u}", f"{v}", weight = cost, capacity = capacity,start_time = start_time, end_time = end_time)


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


    def mst_prim(self):
        if self.current_size == 0:
            print("Graph is Empty")
            return

        visited = [False] * self.current_size
        mst_edge = []
        total_cost = 0

        pq = PriorityQueue()

        start_vertex = 0
        visited[start_vertex] = True

        for edge in self.adj_list[start_vertex]:
            pq.enqueue(edge.vertex, edge.cost, start_vertex)

        while not pq.is_empty() and len(mst_edge) < self.current_size - 1:
            node = pq.dequeue()
            u = node.parent
            v = node.vertex
            cost = node.weight

            if visited[v]:
                continue

            visited[v] = True
            mst_edge.append((u, v, cost))
            total_cost += cost

            for edge in self.adj_list[v]:
                if not visited[edge.vertex]:
                    pq.enqueue(edge.vertex, edge.cost, v)

        if len(mst_edge) != self.current_size - 1:
            print("\nGraph is Not Connected")
            return

        print("\nMST Edges:")
        for u, v, c in mst_edge:
            print(f"{u} -- {v} (cost: {c})")

        print(f"\nTotal cost of MST: {total_cost}")


    def shortest_path(self, src, dest):
        print(f"Shortest path from {src} to {dest} not implemented yet.")

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

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
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