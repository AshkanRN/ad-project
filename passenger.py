import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import animation
from networkx.drawing.nx_agraph import graphviz_layout


class PassengerQueueNode:
    def __init__(self, name, edges,vertices):
        self.name = name
        self.edges = edges
        self.vertices = vertices
        self.next = None

    def __str__(self):
        return f"{self.name}: {self.edges} , {self.vertices}"

class PassengerQueue:
    def __init__(self):
        self.front = None
        self.rear = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, name, edges, vertices):
        new_node = PassengerQueueNode(name, edges, vertices)

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



def reserve_route(graph, name, edges_vertices, passenger_queue):
    # edges_vertices is a tuple with 2 element, the first element is edges in SP and the second is Vertices
    norm_edges = [normalize_edge(u, v) for u, v in edges_vertices[0]]

    if name.lower() in graph.passenger_info:
        print("\nThis passenger is Already on a Route")
        return False

    if not check_capacity(graph, norm_edges):
        print("\nThe route does not have enough capacity.")

        cmd = input("Wanna Enter the Queue Route? [y/n]: ")
        if cmd == 'y' or cmd.lower() == "yes":
            passenger_queue.enqueue(name , norm_edges, edges_vertices[1])
            print("\nEnqueued")
        return False

    for u, v in norm_edges:
        decrease_capacity(graph, u, v,graph.G)

    graph.passenger_info[name.lower()] = (norm_edges,edges_vertices[1])
    # passenger_info is a dictionary, it's value is a tuple like edge_vertices
    print("\nReserved successfully.")
    return True





def animate_edge_traversal(g, vertex_list, steps_per_edge=10, interval=200):
    # ساخت موقعیت گره‌ها
    plt.ioff()
    pos = graphviz_layout(g, prog='sfdp')  # یا هر layout دلخواه
    fig, ax = plt.subplots(figsize=(12, 10))

    manager = plt.get_current_fig_manager()
    try:
        manager.window.wm_geometry("+500+100")  # X=500px, Y=100px
    except AttributeError:
        pass

    edge_list = [(vertex_list[i], vertex_list[i+1]) for i in range(len(vertex_list) - 1 )]

    # ایجاد نقاط مسیر: بین هر جفت رأس (u, v)، steps_per_edge نقطه
    path_points = []
    for u, v in edge_list:
        x_vals = np.linspace(pos[u][0], pos[v][0], steps_per_edge)
        y_vals = np.linspace(pos[u][1], pos[v][1], steps_per_edge)
        points = list(zip(x_vals, y_vals))
        path_points.extend(points)

    # تابع آپدیت فریم‌ها
    def update(i):
        ax.clear()

        # رنگ پیش‌فرض همه گره‌ها خاکستری
        node_colors = []
        for node in g.nodes():
            if node == vertex_list[0]:
                node_colors.append('lightskyblue')  # رنگ شروع
            elif node == vertex_list[-1]:
                node_colors.append('lightgreen')  # رنگ پایان
            else:
                node_colors.append('lightgray')

        nx.draw(
            g,
            pos,
            with_labels=True,
            node_color=node_colors,
            edge_color='gray',
            ax=ax
        )

        # نقطه جاری که در مسیر حرکت می‌کنه
        if i < len(path_points):
            x, y = path_points[i]
            ax.plot(x, y, 'ro', markersize=12)

        # مسیر طی‌شده تا اینجا
        if i > 0:
            ax.plot(*zip(*path_points[:i + 1]), color='red', linewidth=2)

    # ایجاد انیمیشن
    ani = animation.FuncAnimation(
        fig, update, frames=len(path_points), interval=interval, repeat=False)

    plt.show()


def release_route_capacity(graph, name):
    if not graph.passenger_info:
        print("NO Passenger Yet.")
        return

    name = name.lower()
    if name not in graph.passenger_info:
        print("\nPassenger not found.")
        return

    vertices_path = graph.passenger_info[name][1]
    animate_edge_traversal(graph.G, vertices_path,25,10)

    for u, v in graph.passenger_info[name][0]:
        increase_capacity(graph, u, v, graph.G)

    del graph.passenger_info[name]
    print("\nCapacity released.")



def passenger_queue_process(graph, passenger_queue):

    first_passenger = passenger_queue.get_front()
    if not first_passenger:
        print("passengers Queue is Empty")
        return False

    norm_edges = [normalize_edge(u, v) for u, v in first_passenger.edges]

    if not check_capacity(graph, norm_edges):
        print("The Route of first passenger has not enough Capacity Yet")
        return False

    else:
        for u, v in norm_edges:
            decrease_capacity(graph, u, v,graph.G)

        graph.passenger_info[first_passenger.name.lower()] = (norm_edges, first_passenger.vertices)
        print("\nReserved successfully.")
        passenger_queue.dequeue()
        return first_passenger



def decrease_capacity(graph, u, v, networkx_g):

    if networkx_g[u][v]['capacity'] > 0:
        networkx_g[u][v]['capacity'] -= 1

    networkx_g[u][v]['usage'] += 1

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

    if networkx_g[u][v]['usage'] > 0:
        networkx_g[u][v]['usage'] -= 1

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




# def animate_path_on_graph(G, path_edges, layout_prog='sfdp', interval=800):
#     """
#     گراف G و مسیر به صورت لیست یال‌ها (path_edges) دریافت می‌کند
#     و انیمیشن حرکت نقطه روی مسیر را نمایش می‌دهد.
#
#     پارامترها:
#     - G: گراف networkx (بدون جهت)
#     - path_edges: لیست یال‌ها به صورت [(u,v), (v,w), ...]
#     - layout_prog: نام الگوریتم layout برای graphviz_layout (مثل 'sfdp', 'dot', 'neato' و ...)
#     - interval: فاصله زمانی بین فریم‌ها به میلی‌ثانیه
#     """
#
#     # گرفتن موقعیت رئوس با graphviz_layout
#     pos = graphviz_layout(G, prog=layout_prog)
#
#     fig, ax = plt.subplots()
#
#     # رسم گراف ثابت
#     nx.draw(G, pos, ax=ax, node_color='lightblue', edge_color='gray', with_labels=True)
#
#     # استخراج نقاط مسیر پشت سر هم از یال‌ها
#     def path_points(edges):
#         points = []
#         for i, (u, v) in enumerate(edges):
#             if i == 0:
#                 points.append(pos[u])
#             points.append(pos[v])
#         return points
#
#     points = path_points(path_edges)
#     x_points = [p[0] for p in points]
#     y_points = [p[1] for p in points]
#
#     # ایجاد نقطه متحرک روی مسیر
#     point, = ax.plot(x_points[0], y_points[0], 'ro', markersize=10)
#
#     def update(num):
#         point.set_data(x_points[num], y_points[num])
#         ax.set_title(f'Step {num+1} / {len(points)}')
#
#     ani = FuncAnimation(fig, update, frames=len(points), interval=interval, repeat=False)
#     plt.show()


# def animate_path(pos, edge_list):
#     fig, ax = plt.subplots(figsize=(8, 6))
#
#     # رسم گراف پایه (اختیاری، اگر گراف رو هم بخوای نمایش بدی)
#     # می‌تونی اینجا گراف اصلی رو رسم کنی
#
#     # تبدیل یال‌ها به جفت مختصات نقاط ابتدا و انتها
#     path_coords = [(pos[u], pos[v]) for u, v in edge_list]
#
#     # نقطه متحرک (dot)
#     dot, = ax.plot([], [], 'ro', markersize=10)
#
#     steps_per_edge = 10  # تعداد فریم برای هر یال
#     frames_count = len(path_coords) * steps_per_edge
#
#     # تعیین محدوده‌ی نمودار با کمی حاشیه
#     all_x = [x for p in pos.values() for x in (p[0],)]
#     all_y = [y for p in pos.values() for y in (p[1],)]
#     ax.set_xlim(min(all_x)-0.1, max(all_x)+0.1)
#     ax.set_ylim(min(all_y)-0.1, max(all_y)+0.1)
#     ax.set_aspect('equal')
#     ax.axis('off')
#
#     def update(frame):
#         edge_index = frame // steps_per_edge
#         if edge_index >= len(path_coords):
#             return dot,
#
#         (x0, y0), (x1, y1) = path_coords[edge_index]
#         t = (frame % steps_per_edge) / steps_per_edge
#
#         x = (1 - t) * x0 + t * x1
#         y = (1 - t) * y0 + t * y1
#
#         dot.set_data([x], [y])
#         return dot,
#
#     anim = animation.FuncAnimation(fig, update, frames=frames_count, interval=100, blit=True)
#     plt.show()

# def animate_passenger_route(graph, edge_list):
#     pos = nx.nx_agraph.graphviz_layout(graph.G, prog='sfdp')
#
#     fig, ax = plt.subplots(figsize=(14, 12))
#     nx.draw(graph.G, pos, ax=ax,
#             with_labels=True,
#             node_color='skyblue',
#             node_size=900,
#             font_size=14,
#             edge_color='gray',
#             width=2)
#
#     edge_labels = {
#         (u, v): f"{d['weight']}, {d['capacity']}"
#         for u, v, d in graph.G.edges(data=True)
#     }
#     nx.draw_networkx_edge_labels(graph.G, pos, edge_labels=edge_labels, ax=ax)
#
#     dot, = ax.plot([], [], 'ro', markersize=10)  # نقطه قرمز متحرک
#
#     path_coords = []
#     for u, v in edge_list:
#         path_coords.append((pos[u], pos[v]))
#
#     def init():
#         dot.set_data([], [])
#         return dot,
#
#     def update(frame):
#         if frame >= len(path_coords):
#             return dot,
#
#         (x0, y0), (x1, y1) = path_coords[frame]
#         t = (frame % 10) / 10  # درصد پیشرفت روی یال
#         x = (1 - t) * x0 + t * x1
#         y = (1 - t) * y0 + t * y1
#         dot.set_data([x], [y])  # حتما لیست باشه
#         return dot,
#
#     ani = animation.FuncAnimation(
#         fig, update, frames=len(path_coords) + 1,
#         init_func=init, blit=True, repeat=False, interval=700
#     )
#
#     plt.title("Passenger Route Animation")
#     plt.axis('off')
#     plt.show()