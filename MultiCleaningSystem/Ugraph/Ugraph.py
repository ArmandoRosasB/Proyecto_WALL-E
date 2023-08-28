from collections import OrderedDict, deque
from mesa import Model, Agent
import heapq
import sys

class Ugraph:
    def __init__(self, direction : bool) -> None:
        self.__direction = direction
        self.__vertexes = set()
        self.__edges = OrderedDict()

    def addEdge(self, origin, destiny):
        flag = lambda node : node in list(self.__vertexes)

        if not flag(origin):
            self.__vertexes.add(origin)
            self.__edges[origin] = set()

        if not flag(destiny):
            self.__vertexes.add(origin)
            self.__edges[destiny] = set()

        self.__edges[origin].add(destiny)

        if not self.__direction:
            self.__edges[destiny].add(origin)
        
    def containsVertex(self, vertex) -> bool:
        return vertex in self.__vertexes
    
    def getVertexes(self) -> set():
        return self.__vertexes

    def getConnectionFrom(self, vertex) -> set():
        return self.__edges[vertex]

    def __str__(self) -> str:
        aux = ""
        
        for vertex in self.__vertexes:
            aux += vertex + "\t"

            for edge in self.__edges[vertex]:
                aux += edge + "\t"
            aux += "\n"

        aux += "\n"
        return aux

def BreadthFirstSearch(start, map: Model) -> list():
    visited = set()
    pending = deque()

    pending.append(start)
    
    while(len(pending) > 0):
        v = pending.popleft()

        if v not in visited:
            visited.add(v)

            robots = set()
            neighborhood = set()

            neighbors = map.grid.get_neighbors(v, moore = True, include_center = True)  # Regresa un vector

            for agent in neighbors:       
                if agent.value == 'X' or agent.value == 'R':
                    robots.add(agent.pos)

                else: # Si no eres robot, eres un vecino candidato
                    if agent.detritus > 0:
                        return list(agent.pos)
                    
                    neighborhood.add(agent.pos)


            movements = neighborhood.difference(robots) # Las posiciones que solo tengan basura o sean la papelera 
            
            for node in movements:
                pending.append(node)
        
    return []

def dijkstra(start, end, map: Model) -> list():
    visited = set()

    minimum = sys.maxsize
    path = []

    pending = [[start,0,[]]]
    heapq.heapify(pending)

    while(len(pending) > 0):
        cell = heapq.heappop(pending)
        v = cell[0]
        c = cell[1]
        cell[2].append(v)
        prev = cell[2]

        if v == end:
            if c < minimum:
                path = prev
                minimum = c

        if v not in visited:
            visited.add(v)

            robots = set()
            neighborhood = set()

            neighbors = map.grid.get_neighbors(v, moore = True, include_center = False)  # Regresa un vector

            for agent in neighbors:       
                if agent.value == 'X' or agent.value == 'R':
                    robots.add(agent.pos)
                
                else:
                    neighborhood.add(agent.pos)

            movements = neighborhood.difference(robots) # Las posiciones que solo tengan basura o sean la papelera 
            
            for node in movements:
                heapq.heappush(pending,[node, c + 1, prev])
        
    return minimum, path
