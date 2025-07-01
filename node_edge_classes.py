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

        self.G.add_edge(f"{u}", f"{v}", weight = cost, capacity = capacity,
                        start_time = start_time, end_time = end_time)


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
                mst_edges.add((str(min(u, v)), str(max(u, v))))

            print(f"Total cost of component {component_num}: {cost}")
            component_num += 1

        print(mst_edges)
        self.display_mst_edges(mst_edges)


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