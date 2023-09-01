from MultiCleaningSystem.Ugraph.Ugraph import dijkstra, BreadthFirstSearch as bfs
from mesa import Agent, Model # Paquetes para trabajar con agentes y modelos
from collections import deque

import numpy as np
import sys


def getMovements(wallE:Agent, explorando:bool) -> set():
    
    neighbors = [agent for agent in wallE.model.grid.get_neighbors(wallE.pos, moore = True, include_center = False)]  # Regresa un vector

    neighborhood = set()
    robots = set()
    
    for agent in neighbors:       
        if agent.value == 'R':
            robots.add(agent.pos)

        elif agent.value == 'X':
            robots.add(agent.pos)

            if explorando and agent.pos not in wallE.visited:
                wallE.visited.add(agent.pos)

                if wallE.model.mapa[agent.pos[0]][agent.pos[1]] == -1:
                    wallE.model.mapa[agent.pos[0]][agent.pos[1]] = 'X'
                    wallE.model.cells -= 1

        else: # Si no eres robot u obstáculo, eres un vecino candidato
            neighborhood.add(agent.pos)

    return neighborhood.difference(robots)


class Scavenger(Agent):
    """ Clase heredada de mesa.agent que representa a un robot """

    def __init__(self, id: int, model: Model, bottom:int, top:int) -> None:
        """
        El constructor recibe como parámetros el id del agente y el modelo 
        sobre el cual opera
        """
        super().__init__(id, model)

        self.value = 'R'
        self.storage = 5

        self.bottom = bottom
        self.ready = False
        self.top = top

        self.visited = set()
        self.xVisit = []
        self.prev = []

        self.path = deque()
        self.gate = ()
        

    def step(self) -> None:
        """ Este método mueve a los robots a la posición más óptima """

        self.visited.add(self.pos)

        if self.model.cells > 0: # Exploración

            if not self.ready:
                if self.bottom <= self.pos[0] <= self.top:
                    self.ready = True
                    self.gate = self.pos

                    if self.gate == self.model.target:
                        change = getMovements(self, False)
                        change = [move for move in change if move[0] <= self.top and move[0] >= self.bottom]

                        self.gate = list(change)[0]

                    self.visited = set()
                    self.xVisit = []
                    self.prev = []

                else:
                    movements = getMovements(self, False)
                    back = True

                    diff = [(-1, -1), sys.maxsize]
                    for move in movements:
                        if move not in self.visited:
                            top_diff = abs(move[0] - self.bottom)

                            if top_diff < diff[1]:
                                diff[1] = top_diff
                                diff[0] = move

                            back = False
                            if move not in self.xVisit:
                                self.xVisit.append(move)
                
                    if len(movements) == 0 or back:
                        if (len(self.prev) > 0):
                            self.model.grid.move_agent(self, self.prev.pop())
                        return

                    if diff[0] in self.xVisit:
                        self.xVisit.remove(diff[0])
                        self.xVisit.append(diff[0])


                    self.prev.append(self.pos)
                    self.model.grid.move_agent(self, self.xVisit.pop())                    
                    return
            
                


            if self.ready:
                movements = getMovements(self, True)
                movements = [move for move in movements if move[0] <= self.top and move[0] >= self.bottom]

                back = True
                for move in movements:
                    if move not in self.visited:
                        back = False
                        if move in self.xVisit:
                            self.xVisit.remove(move)

                        self.xVisit.append(move)
            
                if len(movements) == 0 or back:
                    if len(self.prev) > 0:
                        self.model.grid.move_agent(self, self.prev.pop())
                    return

                self.prev.append(self.pos)
                self.model.grid.move_agent(self, self.xVisit.pop())

                aux = [agent.detritus for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T']

                if len(aux) > 0:
                    if self.model.mapa[self.pos[0]][self.pos[1]] == -1:
                        self.model.mapa[self.pos[0]][self.pos[1]] = aux[0]

                        self.model.garbage += aux[0]
                        self.model.cells -= 1
            
            if self.model.cells == 0:
                print("Se termino de explorar")
                for row in self.model.mapa:
                    for column in row:
                        print(column, end=" ")
                    print()

        
        
        elif self.model.garbage > 0: # Recolección
            if self.pos == self.model.target:
                self.model.garbage -= (5 - self.storage)
                self.storage = 5
            
            aux = [agent for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T' and agent.detritus > 0]
            
            if len(aux) > 0:
                if self.storage > aux[0].detritus:
                    self.model.mapa[aux[0].pos[0]][aux[0].pos[1]] = 0
                    
                    self.storage -= aux[0].detritus
                    aux[0].detritus = 0
                    
                    
                else: # trash > storage
                    self.model.mapa[aux[0].pos[0]][aux[0].pos[1]] -= self.storage
                    
                    aux[0].detritus -= self.storage
                    self.storage = 0

            if self.storage == 0:
                self.path = dijkstra(self.pos, self.model.target, self.model)
                
            else:
                self.path = dijkstra(self.pos, bfs(self.pos, self.model), self.model)

                if len(self.path) == 0:
                    if self.storage != 5:
                        self.path = dijkstra(self.pos, self.model.target, self.model)
                    
                    else:
                        self.path = dijkstra(self.pos, self.gate, self.model)

            
            if len(self.path) > 0:
                self.model.grid.move_agent(self, self.path.popleft())
        
            if self.model.garbage == 0:
                print("Se termino de limpiar")
                for row in self.model.mapa:
                    for column in row:
                        print(column, end=" ")
                    print()

                self.model.done = True
            

class Trash(Agent):
    """ Clase heredada de mesa.agent que representa una pila de basura """

    def __init__(self, id: int, model: Model, detritus:int) -> None:
        """ El constructor recibe como parámetros el id del agente, el modelo 
        sobre le cual opera y la basura que contiene esa casilla """
        super().__init__(id, model)

        self.value = 'T'
        self.detritus = detritus


class Wall (Agent):
    """ Clase heredada de mesa.agent que representa una pared u obstáculo"""

    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)
        
        self.value = 'X'


class Target (Agent):
    """ Clase heredada de mesa.agent que representa la papelera"""
    def __init__(self, id: int, model: Model) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """

        super().__init__(id, model)
        self.value = 'P'
