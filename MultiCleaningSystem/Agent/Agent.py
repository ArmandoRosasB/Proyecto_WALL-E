# Paquetes para trabajar con agentes y modelos
from mesa import Agent, Model
from collections import deque
import sys
from MultiCleaningSystem.Ugraph.Ugraph import dijkstra, BreadthFirstSearch as bfs

class Scavenger(Agent):
    """ Clase heredada de mesa.agent que representa a un robot """

    mapa = []
    cells = 0
    steps = 0

    def __init__(self, id: int, model: Model, bottom:int, top:int) -> None:
        """ El constructor recibe como parámetros el id del agente y el modelo 
        sobre le cual opera """
        super().__init__(id, model)

        self.value = 'R'
        self.storage = 5

        self.top = top
        self.bottom = bottom

        self.extended_top = 0
        self.extended_bottom = 0

        self.visited = set()
        self.xVisit = []
        self.prev = []

        self.path = deque()
        self.gate = ()
        self.setGate = False

        self.ready = False

    def step(self) -> None:
        """ Este metodo mueve a los robots a la posición más óptima """

        self.steps += 1
        
        neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center = False)  # Regresa un vector
        
        movements = set()
        neighborhood = set()
        robots = set()

        self.visited.add(self.pos)
        print("Numero de pasos", self.steps)
        print("Celdas faltantes ", self.model.cells)

        if self.model.cells > 0: # Exploración

            if not self.ready:
                if self.bottom <= self.pos[0] <= self.top:
                    self.ready = True
                    self.gate = self.pos

                    self.visited = set()
                    self.xVisit = []
                    self.prev = []

                else:
                    neighbors = self.model.grid.get_neighbors(self.pos, moore = True, include_center = False)  # Regresa un vector

                    for agent in neighbors:       
                        if agent.value == 'X' or agent.value == 'R':
                            robots.add(agent.pos)

                        else: # Si no eres robot, eres un vecino candidato
                            neighborhood.add(agent.pos)

                    movements = neighborhood.difference(robots) # Las posiciones que solo tengan basura o sean la papelera 
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
                for agent in neighbors:
                    if agent.value == 'R': # Si eres robot u obstáculo ya no eres una posición disponible             
                        robots.add(agent.pos)

                    if agent.value == 'X':
                        robots.add(agent.pos)

                        if agent.pos not in self.visited:
                            self.visited.add(agent.pos)
                            if self.mapa[agent.pos[0]][agent.pos[1]] == -1:
                                self.mapa[agent.pos[0]][agent.pos[1]] = 'X'
                                self.model.cells -= 1

                    else: # Si no eres robot, eres un vecino candidato
                        neighborhood.add(agent.pos)

                movements = neighborhood.difference(robots) # Las posiciones que solo tengan basura o sean la papelera 
               # print("PRE ", movements)
                
                movements = [move for move in movements if move[0] <= self.top and move[0] >= self.bottom]

              #  print("POS ", movements)

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

                # if self.mapa[self.pos[0]][self.pos[1]] == -1:
                self.model.cells -= 1

                aux = [agent.detritus for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T']

                if len(aux) > 0:
                    if self.mapa[self.pos[0]][self.pos[1]] == -1:
                        self.mapa[self.pos[0]][self.pos[1]] = aux[0]
                        self.model.garbage += aux[0]

        elif self.model.garbage > 0: # Recolección
            # Gate
            curr_pos = self.model.target
            while not self.setGate:
                if self.bottom <= curr_pos <= self.top:
                    self.setGate = True
                    self.gate = curr_pos
                else:
                    # busqueda


            if len(self.path) == 0 and :

            if len(self.path) == 0:
                # Buscar basura en tu posición
                aux = [agent for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T' and agent.detritus > 0]
                
                if len(aux) > 0:
                    if self.storage > 0:
                        if self.storage >= aux[0].detritus:
                            self.storage -= aux[0].detritus
                            aux[0].detritus = 0
                        else:
                            aux[0].detritus -= self.storage
                            self.storage = 0

                # Checamos si ya llegamos a la papelera
                if self.pos == self.model.target:
                    self.storage = 5
                
                trash = bfs(self.pos, self.model, self.top, self.bottom)
                
                if trash != ():
                    self.path = dijkstra(self.pos, trash, self.model)
                else:
                    print("Terminé mi sección")
                    return

            # Avanzar
            # aux = [agent.detritus for agent in self.model.grid.iter_cell_list_contents(self.pos) if agent.value == 'T']
            # SI ya recolectaste toda tu basura
            # Llegar a la papelera
            # Llegamos a basura
            
        else:    
            for row in self.mapa:
                for col in row:
                    print(col, end= " ")
                print()

        
        
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
