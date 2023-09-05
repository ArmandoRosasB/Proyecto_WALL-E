from MultiCleaningSystem.Agent.Agent import Scavenger, Trash, Wall, Target
from mesa.datacollection import DataCollector # Paquete para obtener informacion del ambiente
import numpy as np # Paquete para el manejo de valores numéricos

from mesa import Model # Paquetes para trabajar con modelos
from mesa.space import MultiGrid # Paquete para poder alojar a varios agentes en un mismo cuadrante
from mesa.time import BaseScheduler # Paquete para activar todos los robots al mismo tiempo


def get_grid(model: Model) -> list:
    """
    La función get_grid recibe como parámetro el modelo 
    y regresa el mapa del modelo con determinados valores
    en forma de matriz
    """
    grid = np.zeros( (model.grid.width, model.grid.height) )

    for (content, (x, y)) in model.grid.coord_iter():
        if len(content) == 1:  
            if content[0].value == 'X':
                grid[x][y] = 3 # Obstáculo

            elif content[0].value == 'P':
                grid[x][y] = 2 # Papelera
            
            continue
        
        grid[x][y] = 1 # Robot

    return grid


class Office(Model):
    """ Clase heredada de mesa.model que representa la oficina """
    
    def __init__(self, width:float, height:float, office) -> None:
        """
        El constructor recibe como parámetros el ancho y alto de la oficina,
        así como una matriz representando lo que contiene la oficina
        """
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = BaseScheduler(self)

        self.cells = width * height
        self.steps = 0
        self.environment = [[-1 for column in range (height)] for row in range (width)]
        
        self.garbage = 0
        self.paper_bin = ()
        self.clean = False

        self.robots_positions = []

        id = 0
        for (content, (x, y)) in self.grid.coord_iter(): # Acomodar a los agentes como muestra en el mapa
            agent = None

            if office[x][y].strip() == 'X':
                agent = Wall(id, self)

            elif office[x][y].strip() == 'P':
                agent = Target(id, self)
                self.paper_bin = (x, y)

                self.environment[x][y] = 'P'
                self.cells -= 1

            elif office[x][y].strip() == 'S':
                agent = Trash(id, self, 0)
                self.grid.place_agent(agent, (x, y))
                
                self.environment[x][y] = 0
                self.cells -= 1

                id += 1
                robots = 5
          
                if width < 10:
                    robots = 2

                elif width < 16:
                    robots = 3

                elif width < 21:
                    robots = 4

                self.robots_positions = [[0,0] for robot in range(robots)]
                
                offset = 0
                partition = [width // robots for i in range(5)]

                for i in range(width % robots):
                    partition[i] += 1

                for i in range(robots):
                    agent = Scavenger(id, self,  offset, offset + partition[i] - 1, i)
                    offset += partition[i]

                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

                    self.robots_positions[i] = [agent.pos[0],agent.pos[1]]

                    id += 1
                
                continue

            else:
                agent = Trash(id, self, int(office[x][y]))
            
            self.grid.place_agent(agent, (x, y))
            id += 1

        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})
    
    def step(self) -> None: 
        """
        El metodo step avanza un paso en el schedule
        """
        self.datacollector.collect(self)
        self.schedule.step()

        self.steps += 1
