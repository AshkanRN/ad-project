from node_edge_classes import Graph
from passenger_class import *
from collections import deque
import copy

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



def main():

    g = Graph()

    while True:
        print("\n[0]: Exit"
              "\n[1]: Add Vertex"
              "\n[2]: Add Edge"
              "\n[3]: Print"
              "\n[4]: Shortest Path"
              "\n[5]: Display Graph"
              "\n[6]: MST"
              "\n[7]: Release The Capacity"
              "\n[8]: Passenger List")

        command = input("--> ")

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

                if src not in g.adj_list:
                    print("\nSource Vertex does not exist !!!")
                    continue

                dest = int(input("Destination vertex: "))

                if dest not in g.adj_list:
                    print("\nDestination Vertex does not exist !!!")
                    continue

                if src == dest:
                    print("Self-loop !!")
                    continue

                try:
                    cost, capacity, start_time, end_time = map(int, input("cost, Capacity, Start Time, End Time: ").split())
                except ValueError:
                    print("\nINVALID !, Should Enter 4 Number")
                    continue
                if g.current_size < 5:
                    g.add_edge(src, dest, cost, capacity, start_time, end_time)
                    print(f"\nThe Edge {src} <--> {dest} added.")

                else:
                    temp_graph = copy.deepcopy(g)
                    temp_graph.add_edge(src, dest, cost, capacity, start_time, end_time)

                    if check_distance_bfs(temp_graph, 3):
                        g.add_edge(src, dest, cost, capacity, start_time, end_time)
                        print(f"\nThe Edge {src} <--> {dest} added.")
                    else:
                        print("\nThe Edge Can not be Added, (RADIUS LIMIT)")

            except ValueError:
                print("\nInvalid input! Please enter numbers only.")

        elif command == '3':
            g.print_graph()


        elif command == '4':
            if g.current_size < 2:
                print("\nAdd Vertex first!")
                continue
            try:
                src = int(input("Source vertex: "))
                dest = int(input("Destination vertex: "))

                shortest_path_edges = g.shortest_path(src, dest)

                cmd = input("Wanna Reserve The Route? [y/n]: ")

                if cmd == "y" or cmd.lower() == "yes":
                    name = input("\nEnter Name: ")
                    reserve_route(g, name, shortest_path_edges)

            except ValueError:
                print("\nInvalid Input")

        elif command == '5':
            g.display_graph()

        elif command == '6':
            g.mst_prim()

        elif command == '7':
            name = input("Passenger Name:")
            release_route_capacity(g, name)

        elif command == '8':
            g.display_passengers()

        else:
            print("\nInvalid choice!")


if __name__ == '__main__':
    main()
