
class Passenger:
    def __init__(self, name, edges):
        self.passenger_num = 0
        self.name = name.lower()
        self.edges = edges

    # def __repr__(self):
    #     return f"{self.name} : {self.edges}"


def reserve_route(graph, name, edge_list):
    norm_edges = [normalize_edge(u, v) for u, v in edge_list]

    if name in graph.passenger_info:
        print("\nThis passenger is Already on a Route")
        return

    if not check_capacity(graph, norm_edges):
        print("\nThe route does not have enough capacity.")
        return

    for u, v in norm_edges:
        decrease_capacity(graph, u, v,graph.G)

    graph.passenger_info[name.lower()] = edge_list
    print("\nReserved successfully.")

def release_route_capacity(graph, name):
    name = name.lower()
    if name not in graph.passenger_info:
        print("\nPassenger not found.")
        return

    for u, v in graph.passenger_info[name].edges:
        increase_capacity(graph, u, v, graph.G)

    del graph.passenger_info[name]
    print("\nCapacity released.")

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
