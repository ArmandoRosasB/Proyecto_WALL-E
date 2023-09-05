from MultiCleaningSystem.Ugraph.Ugraph import dijkstra, BreadthFirstSearch as bfs
from mesa import Agent, Model # Paquetes para trabajar con agentes y modelos
from collections import deque
import numpy as np
import sys


def get_movements(wallE: Agent, explorando: bool) -> set:
    """
    La funcion get_movements recibe como parametro un robot y un booleano
    que representa
        true: Modo busqueda
        false: Modo limiapr
    
        La funncion retorna todos los movimientos
        posibles que puede hacer un robot dadas
        las restricciones
    """
    
    neighbors = [agent for agent in wallE.model.grid.get_neighbors(wallE.pos, moore = True, include_center = False)]

    neighborhood = set()
    robots = set()
    
    for agent in neighbors:       
        if agent.value == 'R':
            robots.add(agent.pos)

        elif agent.value == 'X':
            robots.add(agent.pos)

            if explorando and agent.pos not in wallE.visited:
                wallE.visited.add(agent.pos)

                if wallE.model.environment[agent.pos[0]][agent.pos[1]] == -1 and wallE.bottom <= agent.pos[0] <= wallE.top:
                    wallE.model.environment[agent.pos[0]][agent.pos[1]] = 'X'
                    wallE.model.cells -= 1
                    wallE.own_cells -= 1

        else: # Si no eres robot u obstáculo, eres un vecino candidato
            neighborhood.add(agent.pos)

    return neighborhood.difference(robots)


class Scavenger(Agent):
    """ Clase heredada de mesa.agent que representa a un robot """

    def __init__(self, id: int, model: Model, bottom:int, top:int, uuid:int) -> None:
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
        self.own_cells = model.grid.height * (top - bottom + 1)

        self.uuid = uuid
        

    def step(self) -> None:
        """ Este método mueve a los robots a la posición más óptima """

        self.visited.add(self.pos)

        if self.own_cells > 0 and self.model.cells > 0:  # Exploración

            if not self.ready: # Mandar al robot a su area de exploracion
                if self.bottom <= self.pos[0] <= self.top:
                    self.ready = True
                    self.gate = self.pos

                    if self.gate == self.model.paper_bin:
                        change = get_movements(self, False)
                        change = [move for move in change if move[0] <= self.top and move[0] >= self.bottom]

                        self.gate = list(change)[0]

                    self.visited = set()
                    self.xVisit = []
                    self.prev = []

                else:
                    movements = get_movements(self, False)
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
                            self.model.robots_positions[self.uuid] = [self.pos[0],self.pos[1]]
                        return

                    if diff[0] in self.xVisit:
                        self.xVisit.remove(diff[0])
                        self.xVisit.append(diff[0])


                    self.prev.append(self.pos)
                    self.model.grid.move_agent(self, self.xVisit.pop())  
                    self.model.robots_positions[self.uuid] = [self.pos[0],self.pos[1]]                 
                    return
            
                


            if self.ready: # Comenzando a explorar la seccion del mapa asignada
                movements = get_movements(self, True)
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
                        self.model.robots_positions[self.uuid] = [self.pos[0],self.pos[1]]
                    return

                self.prev.append(self.pos)
                self.model.grid.move_agent(self, self.xVisit.pop())
                self.model.robots_positions[self.uuid] = [self.pos[0],self.pos[1]]

                aux = [agent.detritus for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T']

                if len(aux) > 0:
                    if self.model.environment[self.pos[0]][self.pos[1]] == -1:
                        self.model.environment[self.pos[0]][self.pos[1]] = aux[0]

                        self.model.garbage += aux[0]
                        self.model.cells -= 1
                        self.own_cells -= 1
            
            if self.model.cells == 0:#model.cells == 0:
                print("Se terminó de explorar ---> ", self.model.steps, " steps")
                for row in self.model.environment:
                    for column in row:
                        print(column, end=" ")
                    print()
                print()

        
        elif self.model.garbage > 0: # Recolección
            if self.pos == self.model.paper_bin:
                self.model.garbage -= (5 - self.storage)
                self.storage = 5
            
            aux = [agent for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T' and agent.detritus > 0]
            
            if len(aux) > 0:
                if self.storage > aux[0].detritus:
                    self.model.environment[aux[0].pos[0]][aux[0].pos[1]] = 0
                    
                    self.storage -= aux[0].detritus
                    aux[0].detritus = 0
                    
                    
                else: # trash > storage
                    self.model.environment[aux[0].pos[0]][aux[0].pos[1]] -= self.storage
                    
                    aux[0].detritus -= self.storage
                    self.storage = 0

            if self.storage == 0:
                self.path = dijkstra(self.pos, self.model.paper_bin, self.model)
                
            else:
                self.path = dijkstra(self.pos, bfs(self.pos, self.model), self.model)

                if len(self.path) == 0:
                    if self.storage != 5:
                        self.path = dijkstra(self.pos, self.model.paper_bin, self.model)
                    
                    else:
                        self.path = dijkstra(self.pos, self.gate, self.model)

            
            if len(self.path) > 0:
                check = self.path.popleft()
                aux = [agent for agent in self.model.grid.iter_cell_list_contents(check) if agent.value == 'R']
                
                if len(aux) == 0:
                    self.model.grid.move_agent(self, check)
                    self.model.robots_positions[self.uuid] = [self.pos[0],self.pos[1]]
                else:
                    rand = list(get_movements(self, False))

                    if len(rand) > 0:
                        self.model.grid.move_agent(self, rand[np.random.choice([i for i in range(len(rand))])])
                        self.model.robots_positions[self.uuid] = [self.pos[0],self.pos[1]]
        
            if self.model.garbage == 0:
                print("Se terminó de limpiar ---> ", self.model.steps, " steps")
                for row in self.model.environment:
                    for column in row:
                        print(column, end=" ")
                    print()
                print()

                self.model.clean = True
            

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
