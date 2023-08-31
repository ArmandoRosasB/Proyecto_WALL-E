from MultiCleaningSystem.Agent.Agent import Scavenger, Trash, Wall, Target
from mesa.datacollection import DataCollector # Paquete para obtener informacion del ambiente
import numpy as np # Paquete para el manejo de valores numéricos

from mesa import Model # Paquetes para trabajar con modelos
from mesa.space import MultiGrid # Paquete para poder alojar a varios agentes en un mismo cuadrante
from mesa.time import BaseScheduler # Paquete para activar todos los robots al mismo tiempo


colores = []

def get_grid(model):
    """
    La función get_grid recibe como parámetro el modelo 
    y regresa el mapa del modelo con determinados valores
    en forma de matriz
    """
    grid = np.zeros( (model.grid.width, model.grid.height) )

    for (content, (x, y)) in model.grid.coord_iter():

        for c in colores:
            grid[c[0]][c[1]] = 4 # Robot

        if len(content) == 1:  
            if content[0].value == 'X':
                grid[x][y] = 11 # Obstáculo

            elif content[0].value == 'P' and [x, y] not in colores:
                grid[x][y] = 0 # Papelera

            elif [x, y] not in colores:
                grid[x][y] = 2 # Solo basura
            
            continue
        
        colores.append([x, y])
        grid[x][y] = 4000 # Robot

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
        self.mapa = [[-1 for column in range (height)] for row in range (width)]
        
        self.garbage = 0
        self.target = None

        id = 0
        for (content, (x, y)) in self.grid.coord_iter():
            agent = None

            if office[x][y] == 'X':
                agent = Wall(id, self)

            elif office[x][y] == 'P':
                agent = Target(id, self)

                self.target = [x, y]
                self.mapa[x][y] = 'P'

            elif office[x][y] == 'S':
                agent = Trash(id, self, 0)

                self.grid.place_agent(agent, (x, y))
                self.mapa[x][y] = 0

                id += 1
                robots = 5
          
                if width <= 10:
                    robots -= 3;

                offset = 0
                partition = [width // robots for i in range(5)]

                for i in range(width % robots):
                    partition[i] += 1

                for i in range(robots):
                    agent = Scavenger(id, self,  offset, offset + partition[i] - 1)
                    offset += partition[i]

                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

                    id += 1
                
                continue

            else:
                agent = Trash(id, self, int(office[x][y]))
            
            self.grid.place_agent(agent, (x, y))
            id += 1

        self.datacollector = DataCollector(model_reporters={"Grid": get_grid})
    
    def step(self): 
        self.datacollector.collect(self)
        self.schedule.step()

        self.steps += 1
