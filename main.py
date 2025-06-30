from node_edge_classes import Graph

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
