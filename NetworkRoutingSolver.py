#!/usr/bin/python3


from CS312Graph import *
from PriorityQueue import *

import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex):
        self.dest = destIndex
        source_node = self.H.network_nodes[self.source]
        destination_node = self.H.network_nodes[destIndex]
        path_edges = []
        total_length = 0

        if self.H.distance[destination_node.node_id] == "inf":
            return {'cost': total_length, 'path': path_edges}

        while source_node != destination_node:
            previous_node = self.H.previous[destination_node.node_id]
            edge = None

            # If there is no valid path, set cost to unreachable
            if previous_node is None:
                cost = float("inf")
                return {'cost':cost, 'path':path_edges}

            for i in previous_node.neighbors:
                if i.dest == destination_node:
                    edge = i

            total_length += edge.length
            path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
            destination_node = previous_node

        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        self.source = srcIndex
        t1 = time.time()

        if use_heap:
            # Constructor of HeapQueue calls the makeHeap function
            self.H = HeapQueue(self.network.nodes, srcIndex)
            # While there are nodes in the heap:
            # delete the minimum node (root of the binary heap, which has the smallest distance as it's key value)
            # update the distances in the distance and previous arrays
            while len(self.H.heap) > 0:
                u = self.H.delete_min()
                self.H.update_neighbors(u)

        else:
            # Constructor of ArrayQueue calls the makeQueue function
            self.H = ArrayQueue(self.network.nodes, srcIndex)

            # While there are nodes in the heap:
            # delete the minimum node (node that has the smallest distance as it's key value)
            # update the distances in the distance and previous arrays
            while len(self.H.queue) > 0:
                u = self.H.deleteMin()
                self.H.update_neighbors(u)

        t2 = time.time()
        return (t2-t1)
