class PassengerQueueNode:
    def __init__(self, name, edges):
        self.name = name
        self.edges = edges
        self.next = None

    def __str__(self):
        return f"{self.name}: {self.edges}"

class PassengerQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, name, edges):
        new_node = PassengerQueueNode(name, edges)

        if self.is_empty():
            self.rear = self.front = new_node

        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.is_empty():
            print("Passengers Queue is Empty")
            return None

        temp = self.front
        self.front = self.front.next

        if self.is_empty():
            self.rear = None

        return temp

    def get_front(self):
        return self.front

    def print_queue(self):
        if self.is_empty():
            print("empty")
            return

        curr = self.front
        print("\n")
        while curr:
            print(curr)
            curr = curr.next



def reserve_route(graph, name, edge_list, passenger_queue):
    norm_edges = [normalize_edge(u, v) for u, v in edge_list]

    if name in graph.passenger_info:
        print("\nThis passenger is Already on a Route")
        return

    if not check_capacity(graph, norm_edges):
        print("\nThe route does not have enough capacity.")

        cmd = input("Wanna Enter the Queue Route? [y/n]: ")
        if cmd == 'y' or cmd.lower() == "yes":
            passenger_queue.enqueue(name , norm_edges)
            print("\nEnqueued")
        return

    for u, v in norm_edges:
        decrease_capacity(graph, u, v,graph.G)

    graph.passenger_info[name.lower()] = norm_edges
    print("\nReserved successfully.")


def release_route_capacity(graph, name):
    if not graph.passenger_info:
        print("NO Passenger Yet.")
        return

    name = name.lower()
    if name not in graph.passenger_info:
        print("\nPassenger not found.")
        return

    for u, v in graph.passenger_info[name]:
        increase_capacity(graph, u, v, graph.G)

    del graph.passenger_info[name]
    print("\nCapacity released.")


def passenger_queue_process(graph, passenger_queue):

    first_passenger = passenger_queue.get_front()
    if not first_passenger:
        print("passengers Queue is Empty")
        return

    norm_edges = [normalize_edge(u, v) for u, v in first_passenger.edges]

    if not check_capacity(graph, norm_edges):
        print("The Route of first passenger has not enough Capacity Yet")
        return

    else:
        for u, v in norm_edges:
            decrease_capacity(graph, u, v,graph.G)

        graph.passenger_info[first_passenger.name.lower()] = norm_edges
        print("\nReserved successfully.")
        passenger_queue.dequeue()



def decrease_capacity(graph, u, v, networkx_g):

    networkx_g[u][v]['capacity'] -= 1

    for edge in graph.adj_list[v]:
        if edge.vertex == u:
            if edge.capacity > 0:
                edge.capacity -= 1
            break
    for edge in graph.adj_list[u]:
        if edge.vertex == v:
            if edge.capacity > 0:
                edge.capacity -= 1
            break

def increase_capacity(graph, u, v, networkx_g):
    networkx_g[u][v]['capacity'] += 1
    for edge in graph.adj_list[v]:
        if edge.vertex == u:
            if edge.capacity >= 0:
                edge.capacity += 1
            break
    for edge in graph.adj_list[u]:
        if edge.vertex == v:
            if edge.capacity >= 0:
                edge.capacity += 1
            break


def check_capacity(graph, passenger_edge):
    for u, v in passenger_edge:
        for edge in graph.adj_list[u]:
            if edge.vertex == v:
                if edge.capacity <= 0:
                    return False
    return True

def normalize_edge(u, v):
    return min(u, v), max(u, v)
