from collections import deque
from mesa import Model
import heapq
from collections import deque

class Node(object):
    """
    La clase nodo es una clase cuyas instancias
    se componen de una tupla, representando una posicion
    y un entero que representa el costo para llegar a tal coordenada
    """
    def __init__(self, pos: tuple, steps : int) -> None:
        self.pos = pos
        self.steps = steps

    def __repr__(self):
        return f"Node value: {self.pos}\tSteps: {self.steps}"
    
    def __lt__(self, other):
        return self.steps < other.steps
    
    def __eq__(self, other):
        return self.pos == other.pos and self.steps == other.steps

def BreadthFirstSearch(start: tuple, model: Model) -> list:
    """
    La funion BreadthFirstSearch realiza una busqueda en aplitud que devuelve
    la primera posicion de basura encontrada
    """
    visited = set()
    pending = deque()

    pending.append(start)
    
    while(len(pending) > 0):
        v = pending.popleft()

        if v not in visited:
            visited.add(v)

            robots = set()
            neighborhood = set()

            neighbors = [agent for agent in model.grid.get_neighbors(v, moore = True, include_center = True)] 

            for agent in neighbors:       
                if agent.value == 'X':
                    robots.add(agent.pos)

                else: # Si no eres robot, eres un vecino candidato
                    if agent.value != 'P' and agent.value != 'R' and agent.detritus > 0:
                        return agent.pos
                    
                    neighborhood.add(agent.pos)

            movements = neighborhood.difference(robots) 
            
            for node in movements:
                pending.append(node)
        
    return ()

def dijkstra(start:tuple, end:tuple, model: Model) -> list :
    """
    La funcion dijkstra recibe dos puntos y un modelo y regresa
    el camino mas rapido a seguir para llegar del punto de 
    inicio al punto final
    """
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

            neighbors = model.grid.get_neighbors(v, moore = True, include_center = False) 

            for agent in neighbors:       
                if agent.value == 'X':
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
        return deque()
    
    node = path[end]

    while node != start:
        minPath.insert(0, node)
        node = path[node]
        
    return deque(minPath)
