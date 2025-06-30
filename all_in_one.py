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
        if u >= self.current_size or v >= self.current_size:
            print("\nVertex does not exist !!!")
            return

        if u == v:
            print("Self-loop !!")
            return

        # حذف یال قبلی در صورت وجود
        self.adj_list[u] = [edge for edge in self.adj_list[u] if edge.vertex != v]
        self.adj_list[v] = [edge for edge in self.adj_list[v] if edge.vertex != u]

        self.adj_list[u].append(Node(v, cost, capacity, start_time, end_time))
        self.adj_list[v].append(Node(u, cost, capacity, start_time, end_time))

        self.G.add_edge(f"{u}", f"{v}")
        # self.G.add_edge(f"{v}", f"{u}")

        print(f"\nEdge added between {u} and {v}.")

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
            print(f"V{u} :", end=" ")
            for edge in self.adj_list[u]:
                print(edge, end=" -> ")
            print("None")

    def shortest_path(self, src, dest):
        print(f"Shortest path from {src} to {dest} not implemented yet.")

    def display_graph(self):
        if self.current_size == 0:
            print("\nEMPTY\n")
            return
        nx.draw(self.G, with_labels=True, node_color='skyblue', node_size=1500, font_size=16)
        plt.title("Simple Triangle Graph")
        plt.show()


def main():
    g = Graph()

    while True:
        print("\n[0]: Exit"
              "\n[1]: Add Vertex"
              "\n[2]: Add Edge"
              "\n[3]: Display Vertices"
              "\n[4]: Print"
              "\n[5]: Shortest Path"
              "\n[6]: Display Graph")

        command = input("Enter command: ")

        if command == '0':
            break

        elif command == '1':
            g.add_vertex()

        elif command == '2':
            if g.current_size < 2:
                print("\nAdd Vertex first !!")
                continue

            try:
                src = int(input("\nSource vertex: "))
                dest = int(input("Destination vertex: "))

                if src >= g.current_size:
                    print("\nSource Vertex does not exist !!!")
                    continue

                if dest >= g.current_size:
                    print("\nDestination Vertex does not exist !!!")
                    continue

                if src == dest:
                    print("Self-loop !!")
                    continue

                cost = int(input("\nCost: "))
                start_time = int(input("Start Time: "))
                end_time = int(input("End Time: "))
                capacity = int(input("Capacity: "))

                g.add_edge(src, dest, cost, capacity, start_time, end_time)

            except ValueError:
                print("Invalid input! Please enter numbers only.")

        elif command == '3':
            g.display_vertices()

        elif command == '4':
            g.print_graph()

        elif command == '5':
            if g.current_size < 2:
                print("Add Vertex first!")
                continue
            try:
                src = int(input("Source vertex: "))
                dest = int(input("Destination vertex: "))
                g.shortest_path(src, dest)
            except ValueError:
                print("Invalid input.")

        elif command == '6':
            g.display_graph()

        else:
            print("\nInvalid choice!")


if __name__ == '__main__':
    main()
