from node_edge_classes import Graph

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


        else:
            print("\nInvalid choice!")


if __name__ == '__main__':
    main()
