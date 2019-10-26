import math


class ArrayQueue:
    def __init__(self, network_nodes, source_node):
        self.network_nodes = network_nodes
        self.source_node = source_node
        self.distance = [None] * len(network_nodes)
        self.previous = [None] * len(network_nodes)
        self.queue = self.makeQueue(network_nodes)

        # Set the distances of the nodes to infinity, and previous array values to null
        # Set the distance of the root node to 0
        for i in network_nodes:
            self.distance[i.node_id] = float("inf")
            self.previous[i.node_id] = None
        self.distance[self.source_node] = 0

    # Makes the self.queue by calling insert on a local function array and setting it equal to it
    # after all nodes have been appended to it
    def makeQueue(self, network_nodes):
        queue = []
        for i in network_nodes:
            # queue.append(i)
            self.insert(queue, i)

        return queue

    # Inserts by appending nodes into the queue that will be made into the self.queue
    def insert(self, queue, node):
        queue.append(node)

    # Iterates through the distance array, finds the node x associated with the smallest distancce
    # returns node x
    def deleteMin(self):
        minDistance = float("inf")
        node = self.queue[0]

        for i in self.queue:
            if self.distance[i.node_id] < minDistance:
                minDistance = self.distance[i.node_id]
                node = i

        self.queue.remove(node)

        return node

    # For each node in the neighbor list of the passed in node, get its length
    # compare lengths of the three edges to find the shortest edge
    # update distance and previous arrays, makes a call to decrease_key
    def update_neighbors(self, node):
        for i in node.neighbors:
            edge_length = i.length
            destination = i.dest

            if self.distance[destination.node_id] > self.distance[node.node_id] + edge_length:
                new_edge_length = self.distance[node.node_id] + edge_length
                self.distance[destination.node_id] = new_edge_length
                self.previous[destination.node_id] = node
                self.decrease_key(destination, new_edge_length)

    # Updates the distance of the node in the distance array
    def decrease_key(self, node, updated_distance):
        self.distance[node.node_id] = updated_distance


class HeapQueue:
    def __init__(self, network_nodes, source_node):
        self.network_nodes = network_nodes
        self.root_node = source_node
        self.nodes = network_nodes
        self.distance = [None] * len(network_nodes)
        self.previous = [None] * len(network_nodes)
        self.lookUpArray = [None] * len(network_nodes)
        self.heap = []

        # Set the distances of each node to infinity
        # Set the distance of the root node to 0
        for i in network_nodes:
            self.distance[i.node_id] = float("inf")
        self.distance[self.root_node] = 0

        self.make_heap(self.nodes)

    # Makes the heap by first inserting the root node at index 0
    # lookUpArray is the inverse array of the heap so we can have fast look up times later in the code.
    def make_heap(self, network_nodes):
        # Place the root node in the heap array at index 0
        self.heap.append(network_nodes[self.root_node])
        self.lookUpArray[self.root_node] = 0

        # Create heap in random node order with root node at beginning
        # Make sure not to append the root node again to the heap
        # Keep lookUpArray inverse properties intact
        for node in network_nodes:
            if node.node_id != self.root_node:
                self.heap.append(node)
                self.insert(node)
                self.lookUpArray[node.node_id] = node.node_id

    # Returns the index of the child with the smallest key value
    def min_child(self, i):
        # Call the helper function to compare children distances
        left, right = self.get_children(i)

        # If left is 0, there are no children
        if left == 0:
            return 0
        # If right is 0, parent only had left child
        elif right == 0:
            return left
        else:
            # Compare distances of the left and right child of i. Return the one with shortest distance.
            if self.distance[self.heap[left].node_id] < self.distance[self.heap[right].node_id]:
                return left

            return right

    # Gets the index of the left and right child of a parent node
    def get_children(self, parent_index):
        # Out of bounds range check
        if 2 * parent_index >= len(self.heap) - 1:
            return 0, 0

        # If parent only has left child, enter if condition
        left_child = (parent_index * 2) + 1

        if (2 * parent_index) + 1 >= len(self.heap) - 1:
            return left_child, 0

        # Parent had both children
        right_child = (parent_index * 2) + 2

        # returning the index of the left and right children
        return left_child, right_child

    # Place node in parent position and let it sift down the heap into the proper place in heap
    def sift_down(self, node, parent):
        # Return index of the smallest child of parent
        c = self.min_child(parent)

        # While the parent node has children, compare the distances of the child with the node
        # If distance of the child is less than the distance of the node, swap them in the heap
        # Make sure to keep the loopUpArray properties intact
        while c != 0 and self.distance[self.heap[c].node_id] < self.distance[node.node_id]:
            self.modify_heap(parent, self.heap[c])
            parent = c
            c = self.min_child(parent)

        # Change properties in the heap and lookUpArray
        self.modify_heap(parent, node)

        return

    # For each node in the neighbor list of the passed in node, get its length
    # compare lengths of the three edges to find the shortest edge
    # update distance and previous arrays, makes a call to decrease_key
    def update_neighbors(self, node):
        for i in node.neighbors:
            edge_length = i.length
            destination = i.dest

            if self.distance[destination.node_id] > self.distance[node.node_id] + edge_length:
                new_edge_length = self.distance[node.node_id] + edge_length
                self.distance[destination.node_id] = new_edge_length
                self.previous[destination.node_id] = node
                self.decrease_key(destination)

    # This function gets called by insert
    # Grabs the last node in the heap and compares it to its parent.
    # While the distance value of the parent is greater than the node being bubbled up, swap them
    def bubble_up(self, node, index):
        p = math.ceil(index / 2)

        # Out of bounds check
        if index < len(self.heap):
            while index > 1 and self.distance[self.heap[p].node_id] > self.distance[node.node_id]:
                self.modify_heap(index, self.heap[p])
                index = p
                p = math.ceil(index / 2)

            # Change properties in the heap and lookUpArray
            self.modify_heap(index, node)

    # Insert function's only responsibility is to call bubble_up
    def insert(self, node):
        self.bubble_up(node, len(self.heap) - 1)

        return

    # Returns the root node of the heap
    # Grabs the last node in the heap and places it at the root node and calls sift_down to sift it down to its proper location
    # based of distance values
    def delete_min(self):
        if len(self.heap) == 0:
            return None
        else:
            x = self.heap[0]
            # parameters are the last node in the heap, and index of the root.
            # keep track of where the node is at in the heap
            self.sift_down(self.heap[len(self.heap) - 1], 0)
            reference_node = self.heap[len(self.heap) - 1]
            reference_node_index = reference_node.node_id

            # Pops off the last element of heap
            # Keep track of the nodes location in the heap so we can look it up in constant time
            self.heap.pop(len(self.heap) - 1)
            self.lookUpArray[reference_node.node_id] = reference_node_index

        return x

    # Only responsibility is to call bubble_up with the node
    # Passes in the node and where it is located in the heap (constant time)
    def decrease_key(self, node):
        self.bubble_up(node, self.lookUpArray[node.node_id])

    # Takes care of keeping the heap and lookUpArray inverse arrays
    def modify_heap(self, index, node):
        self.heap[index] = node
        self.lookUpArray[node.node_id] = index
