from collections import OrderedDict, deque

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

def BreadthFirstSearch(start, end, graph: Ugraph):
    visited = set()
    pending = deque()

    pending.append(start)
    
    while(len(pending) > 0):
        v = pending.popleft()

        if v not in visited:
            visited.add(v)

            connected = graph.getConnectionFrom(v)
            
            for node in connected:
                pending.append(node)
        
    return visited