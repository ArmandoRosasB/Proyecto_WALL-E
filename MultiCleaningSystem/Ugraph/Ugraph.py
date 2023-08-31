from collections import deque
from mesa import Model
import heapq
from collections import deque

class Node(object):
    def __init__(self, pos, steps):
        self.pos = pos
        self.steps = steps

    def __repr__(self):
        return f"Node value: {self.pos}\tSteps: {self.steps}"
    
    def __lt__(self, other):
        return self.steps < other.steps
    
    def __eq__(self, other):
        return self.pos == other.pos and self.steps == other.steps

def BreadthFirstSearch(start, model: Model, top : int, bottom : int) -> list:
    visited = set()
    pending = deque()

    pending.append(start)
    
    while(len(pending) > 0):
        v = pending.popleft()

        if v not in visited:
            visited.add(v)

            robots = set()
            neighborhood = set()

            neighbors = model.grid.get_neighbors(v, moore = True, include_center = True)  # Regresa un vector

            for agent in neighbors:       
                if agent.value == 'X' or agent.value == 'R':
                    robots.add(agent.pos)

                else: # Si no eres robot, eres un vecino candidato
                    if agent.value != 'P' and agent.detritus > 0:
                        
                        if agent.pos[0] <= top and agent.pos[0] >= bottom:
                            return agent.pos
                    
                    neighborhood.add(agent.pos)

            movements = neighborhood.difference(robots) 
            movements = [move for move in movements if move[0] <= top and move[0] >= bottom]
            
            for node in movements:
                pending.append(node)
        
    return ()

def dijkstra(start:tuple, end:tuple, model: Model) -> list():
    visited = set()

    path = {}

    pending = [Node(start,0)]
    heapq.heapify(pending)

    while(len(pending) > 0):
        cell = heapq.heappop(pending)
        v = cell.pos
        c = cell.steps

        if v == end:
            break

        if v not in visited:
            visited.add(v)

            robots = set()
            neighborhood = set()

            neighbors = model.grid.get_neighbors(v, moore = True, include_center = False)  # Regresa un vector

            for agent in neighbors:       
                if agent.value == 'X' or agent.value == 'R':
                    robots.add(agent.pos)
                
                else:
                    neighborhood.add(agent.pos)

            movements = neighborhood.difference(robots) # Las posiciones que solo tengan basura o sean la papelera 
            
            for node in movements:
                heapq.heappush(pending,Node(node, c + 1))
                
                if node not in path:
                    path[(node)] = v

    minPath = [end]


    if end not in path.keys():
        print("No hay camino")
        return deque()
    
    node = path[end]

    while node != start:
        minPath.insert(0, node)
        node = path[node]
        
    return deque(minPath)
