from graph import *
from passenger_class import *
import copy


def main():

    graph = Graph()
    passenger_queue = PassengerQueue()

    while True:
        print("\n[0]: Exit"
              "\n[1]: Add Vertex"
              "\n[2]: Add Edge"
              "\n[3]: Print"
              "\n[4]: Shortest Path"
              "\n[5]: Display Graph"
              "\n[6]: MST"
              "\n[7]: Release The Capacity"
              "\n[8]: Passenger List"
              "\n[9]: Print Passenger Queue"
              "\n[10]: Check first Passenger Route in Queue")

        command = input("--> ")

        if command == '0':
            break

        elif command == '1':
            graph.add_vertex()

        elif command == '2':
            if graph.current_size < 2:
                print("\nAdd Vertex first !!")
                continue

            try:
                src, dest = map(int, input("Source and Destination: ").split())

                if src not in graph.adj_list:
                    print("\nSource Vertex does not exist !!!")
                    continue

                if dest not in graph.adj_list:
                    print("\nDestination Vertex does not exist !!!")
                    continue

                if src == dest:
                    print("Self-loop !!")
                    continue

                try:
                    cost, capacity, start_time, end_time = (
                        map(int, input("Cost, Capacity, Start Time, End Time: ").split()))

                except ValueError:
                    print("\nINVALID !, Should Enter 4 Number")
                    continue

                if cost <= 0:
                    print("Edge's Cost Can not be <= 0")

                if graph.current_size < 5:
                    graph.add_edge(src, dest, cost, capacity, start_time, end_time)
                    print(f"\nThe Edge {src} <--> {dest} added.")

                else:
                    temp_graph = copy.deepcopy(graph)
                    temp_graph.add_edge(src, dest, cost, capacity, start_time, end_time)

                    if check_radius_bfs(temp_graph, 3):
                        graph.add_edge(src, dest, cost, capacity, start_time, end_time)
                        print(f"\nThe Edge {src} <--> {dest} added.")
                    else:
                        print("\nThe Edge Can not be Added, (RADIUS LIMIT)")

            except ValueError:
                print("\nInvalid input! Please enter numbers only.")

        elif command == '3':
            graph.print_graph()


        elif command == '4':
            if graph.current_size < 2:
                print("\nAdd Vertex first!")
                continue

            try:
                src = int(input("Source vertex: "))
                dest = int(input("Destination vertex: "))

                shortest_path_edges = graph.shortest_path(src, dest)

                if shortest_path_edges:
                    cmd = input("Wanna Reserve The Route? [y/n]: ")

                    if cmd == "y" or cmd.lower() == "yes":
                        name = input("Enter Name: ")
                        flg = reserve_route(graph, name, shortest_path_edges, passenger_queue)
                        if flg:
                            graph.highlight_edges(shortest_path_edges)

            except ValueError:
                print("\nInvalid Input")


        elif command == '5':
            graph.display_graph()

        elif command == '6':
            graph.mst_prim()

        elif command == '7':
            if not graph.passenger_info:
                print("No Passenger Yet.")
                continue

            name = input("Passenger Name:")
            release_route_capacity(graph, name)

        elif command == '8':
            graph.display_passengers()

        elif command == '9':
            passenger_queue.print_queue()

        elif command == '10':
            first_passenger = passenger_queue_process(graph, passenger_queue)

            if first_passenger:
                graph.highlight_edges(first_passenger.edges)


        else:
            print("\nInvalid choice!")



if __name__ == '__main__':
    main()
