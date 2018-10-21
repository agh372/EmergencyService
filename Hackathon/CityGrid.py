import random
import sys
from jsonParser import get_source,get_destination

from pushNotification import sendNotification

class Node(object):
    def __init__(self, i, j):
        # [WN, NE, ES, SW]
        self.lights = [0, 0, 0, 0]
        green = random.randint(0,3)
        self.lights[green] = 1
        self.i = i
        self.j = j
        self.locked = False


class Edge(object):
    def __init__(self, weight=-1):
        self.state = True
        if weight == -1:
            self.weight = random.randint(10,20)
        else:
            self.weight = weight

    def toggle_state(self):
        if self.state:
            self.state = False
        else:
            self.state = True


class Grid(object):
    def __init__(self, N):
        self.N = N
        self.nodes = []
        self.adjacency = [[None for j in range(self.N * self.N)]for i in range(self.N * self.N)]
        self.shortestPath = []


    def create_graph(self):
        for i in range(self.N):
            nodesRow = []
            for j in range(self.N):
                nodesRow.append(Node(i, j))
            self.nodes.append(nodesRow)

        for i in range(self.N):
            for j in range(self.N):
                current_node = i*self.N + j
                if j+1 < self.N:
                    link_node = i*self.N + (j+1)
                    self.adjacency[current_node][link_node] = Edge()
                if i+1 < self.N:
                    link_node = (i+1)*self.N + j
                    self.adjacency[current_node][link_node] = Edge()
                if i-1 >= 0:
                    link_node = (i-1)*self.N + j
                    self.adjacency[current_node][link_node] = Edge()
                if j-1 >= 0:
                    link_node = i*self.N + (j-1)
                    self.adjacency[current_node][link_node] = Edge()

    def print_adjacency(self):
        for i in range(self.N * self.N):
            for j in range(self.N * self.N):
                if self.adjacency[i][j] is not None:
                    print("(" + str(int(i/self.N)) + "," + str(i%self.N) +
                          "),("+ str(int(j/self.N)) + "," + str(j%self.N) +
                          "): " + str(self.adjacency[i][j].weight))

    def minDistance(self, distances, sptSet):
        min_distance = sys.maxsize
        min_index = -1

        for i in range(self.N * self.N):
            if distances[i] < min_distance and sptSet[i] is False:
                min_distance = distances[i]
                min_index = i

        return min_index

    def get_path(self, path, parents, dest):
        if parents[dest] == -1:
            path = [dest] + path
            self.shortestPath = path
            return

        path = [dest] + path
        self.get_path(path, parents, parents[dest])

    def shortest_path(self, src, dest):
        distances = [100000 for i in range(self.N * self.N)]

        sptSet = [False for i in range(self.N * self.N)]
        parents = [-2 for i in range(self.N * self.N)]
        distances[src] = 0
        parents[src] = -1

        for i in range(self.N * self.N - 1):
            node_index = self.minDistance(distances, sptSet)
            sptSet[node_index] = True

            for j in range(self.N * self.N):
                if sptSet[j] is False and self.adjacency[node_index][j] is not None and distances[j] > (self.adjacency[node_index][j].weight + distances[node_index]):
                    distances[j] = self.adjacency[node_index][j].weight + distances[node_index]
                    parents[j] = node_index

        self.get_path([], parents, dest)
        print(self.shortestPath)



    def path_value(self, src, dest):
        self.shortest_path(src, dest)
        path_distance = 0
        for i in range(len(self.shortestPath)-1):
            path_distance += self.adjacency[self.shortestPath[i]][self.shortestPath[i+1]].weight

        return path_distance


grid = Grid(10)
grid.create_graph()
grid.print_adjacency()

import threading


source = get_source()
print("Source: ",source)


if source is not None:

    destList = get_destination()
    print("Hospital list:",destList)

    print("Distance:", grid.path_value(0,1))


    pathsHospitals = []
    for i in range(0,len(destList)):
        pathsHospitals.append(grid.path_value(source, destList[i]))


    print("Index: ", pathsHospitals.index(min(pathsHospitals)))

    #sendNotification() //sends notification  to the particular hospital which has least traffic and can reach sooner
