class QueueNode:
    def __init__(self, vertex, weight, parent = None):
        self.vertex = vertex
        self.weight = weight
        self.parent = parent
        self.next = None

    def __str__(self):
        return f"{self.vertex}, {self.weight}, {self.parent}"

class PriorityQueue:


    def __init__(self):
        self.front = None

    def is_empty(self):
        return self.front is None

    def enqueue(self, vertex, weight, parent = None):
        new_node = QueueNode(vertex, weight, parent)

        if self.is_empty() or self.front.weight > weight:
            new_node.next = self.front
            self.front = new_node
            return

        curr = self.front

        while curr.next is not None and new_node.weight >= curr.next.weight:
            curr = curr.next

        new_node.next = curr.next
        curr.next = new_node

    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = self.front.next
        return temp

    def print_queue(self):
        if self.is_empty():
            print("empty")
            return

        curr = self.front
        print("\n")
        while curr:
            print(curr, end =" ")
            curr = curr.next



