# Importamos el modelo y los agentes
from MultiCleaningSystem.Model.Model import Office
from MultiCleaningSystem.Ugraph.Ugraph import dijkstra, BreadthFirstSearch

# Librerias para mandar informacion al servidor
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging # To log messages ( DEBUG | INFO | WARNING | ERROR | CRITICAL )

from sys import argv


# Importamos matplotlib y seaborn para poder visualizar los resultados
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128


width = 0
height = 0
office = []

flag = True

with open('Tests/input1.txt', 'r') as input: # Abriendo el mapa
    
    for linea in input:
        if flag:
            width, height = [int(num) for num in linea.split(" ")]
            flag = False
        
        else:
            office.append(linea.split(" "))

model = Office(width, height, office) # Inicializamos el modelo


class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200) # Success status

        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    
    def do_GET(self):
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))


    def do_POST(self):
        global model
        model.step()
        

        mapa = ""
        for row in range( len(model.environment) ):

            for col in range( len(model.environment[row]) ):
                mapa += str(model.environment[row][col])

                if col != len(model.environment[row]) - 1: 
                    mapa += "*"
            
            if row != len(model.environment) -1: 
                mapa += ","


        info = {
            "width": model.grid.width,
            "height": model.grid.height,
            
            "steps": model.steps,
            "environment" : mapa
        }
        
        self._set_response()
        self.wfile.write(str(info).encode('utf-8'))


def run(server_class = HTTPServer, handler_class = Server, port = 8585):
    logging.basicConfig(level = logging.INFO)

    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:   # CTRL+C stops the server
        pass

    httpd.server_close()
    logging.info("Stopping httpd...\n")



if len(argv) == 2:
    run(port = int(argv[1])) # Receives port

else:
    run() # Default port

"""
while not model.clean:
   model.step()
  

print("Algoritmo terminado en ", model.steps, " steps")
# Visualizacion
all_grid = model.datacollector.get_model_vars_dataframe() # Arreglo de matrices

fig, axis = plt.subplots(figsize= (width, height))
axis.set_xticks([])
axis.set_yticks([])
patch = plt.imshow(all_grid.iloc[0][0], cmap=sns.color_palette("Paired", as_cmap=True))

def animate(i):
    patch.set_data(all_grid.iloc[i][0])
    
anim = animation.FuncAnimation(fig, animate, frames = model.steps)

plt.show()
"""
