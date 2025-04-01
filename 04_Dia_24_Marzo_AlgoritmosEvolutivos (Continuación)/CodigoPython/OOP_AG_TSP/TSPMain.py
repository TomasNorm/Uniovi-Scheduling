import numpy as np # para estadísticos del experimento
from GeneticAlgorithm import * # Nuestro algoritmo genético
import matplotlib.pyplot as plt # Para pintar soluciones y/o evolución del GA
from TSPConfiguration	import * # Configuración del problema TSP

# Dibuja la mejor ruta encontrada y la evolucion del fitness
def DibujarResultados(coordenadas, ruta, mejor_fitness, evolucion=[]):
   x=[]
   y=[]
   for i in ruta:
      x.append(coordenadas[i][0])
      y.append(coordenadas[i][1])
   plt.figure(figsize=(11,5))
   plt.subplot(121)
   plt.plot(x, y, 'bo', markersize=4.0)
   a_scale = float(max(x))/float(100)
   plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale, color = 'r', length_includes_head=True)
   for i in range(0,len(x)-1):
      plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale, color = 'r', length_includes_head=True)      
   plt.xlim(0,max(x)*1.1)
   plt.ylim(0,max(y)*1.1)
   plt.xlabel("x")
   plt.ylabel("y")
   plt.title(f"Mejor ruta encontrada ({mejor_fitness:.2f})")
   plt.subplot(122)
   plt.plot(evolucion)
   plt.xlabel("Iteración")
   plt.ylabel("Fitness")
   plt.title("Evolución")
   plt.show()

# Función que crea un experimento ejecutándose el GA total_runs veces, y que activando la traza
# muestra la evolución y solución de cada ejecución. 
def experiment(total_runs = 10, traza = False):
     # creamos un objeto configuracion TSP
    cfg = TSPConfiguration()
    # creamos un objeto algoritmo genético configurado con cfg
    ga = GeneticAlgorithm(cfg, traza = traza)
    # definimos dos arrays "mejores" y "tiempos" (inicilamente vacíos)
    # para almacenar el mejor fitness de cada ejecución y el tiempo de la ejecución
    mejores = []
    tiempos = []
    
    # Lanza un bluce que se ejecute "total_runs" veces
        # muestra el número de ejecución actual
        # lanza una ejecución del genético
        # añade al final de "mejores" los resultados del genético
        # añade al final de "tiempos" el tiempo registrado en la clase "Tiempo"
        # muestra los resultados de esta ejecución
        # si la "traza" está activa, además muestra la gráfica de la solución y la evolución
    
    for i in range(total_runs):
        print(f"Run {i+1}")#, end="")
        mejor_solucion, mejor_fitness, evolucion = ga.run()
        mejores.append(mejor_fitness)
        print(f" Tiempo: {Tiempo.total()} segs")
        tiempos.append(Tiempo.total())
        # Mostrar resultados
        #print('¡Ejecucion finalizada! El tiempo de ejecución fue: %s segundos' % Tiempo.total())
        #print('La mejor solucion y su mejor fitness:')
        print('f(%s) = %f' % (mejor_solucion, mejor_fitness))
        if traza:
            DibujarResultados(cfg.problem.coordenadas,mejor_solucion,mejor_fitness,evolucion)
    
    # muestra el array de mejores soluciones "mejores"
    print(mejores)
    # muestra los estadísticos del array "mejores":
    # Best sol: valor mínimo 
    # Average sol: valor promedio
    # StdDev sol: desviación estándar 
    # muestra los estadísticos del array "tiempos":
    # Average time: tiempo promedio de ejecución
    # StdDev time: desviación estándar 
    
    print(f'Best sol: {np.min(mejores):.2f}')
    print(f'Average sol: {np.mean(mejores):.2f}')
    print(f'StdDev sol: {np.std(mejores):.2f}')
    print(f'Average time: {np.mean(tiempos):.2f}')
    print(f'StdDev time: {np.std(tiempos):.2f}')

# Función que lanza una ejecución del GA 
def run_GA():
    # creamos un objeto configuracion TSP
    cfg = TSPConfiguration()
    # creamos un objeto algoritmo genético configurado con cfg
    ga = GeneticAlgorithm(cfg)

    # ejecutamos el algoritmo genético: nos devuelve la mejor solucion, su fitness, y la 
    # evolucion del fitness del mejor, promedio y peor solución en cada generación 
    mejor_solucion, mejor_fitness, evolucion = ga.run()

    # Mostrar resultados
    print('¡Ejecucion finalizada! El tiempo de ejecución fue: %s segundos' % Tiempo.total())
    print('La mejor solucion y su mejor fitness:')
    print('f(%s) = %f' % (mejor_solucion, mejor_fitness))
    # mostrar graficamente los resultados
    DibujarResultados(cfg.problem.coordenadas,mejor_solucion,mejor_fitness,evolucion)
    




### ---------------------------------------------------------------------------
### PROGRAMA PRINCIPAL
### ---------------------------------------------------------------------------

run_GA()
# experiment(10, False)
