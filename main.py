from node_edge_classes import Graph
from collections import deque

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
              "\n[5]: Display Graph")

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
                    cost, start_time, end_time, capacity = map(int, input("cots, Start Time, End Time, Capacity: ").split())
                except ValueError:
                    print("\nINVALID !, Should Enter 4 Number")
                    continue

                g.add_edge(src, dest, cost, capacity, start_time, end_time)

                print(f"\nThe Edge {src} -> {dest} added.")

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
                g.shortest_path(src, dest)
            except ValueError:
                print("Invalid input.")


        elif command == '5':
            g.display_graph()

        elif command == '6':
            x = int(input("enter a vertex: "))
            if x in g.adj_list:
                print(get_neighbours(g,x))
            else:
                print("the vertex does not exists")

        else:
            print("\nInvalid choice!")


if __name__ == '__main__':
    main()
