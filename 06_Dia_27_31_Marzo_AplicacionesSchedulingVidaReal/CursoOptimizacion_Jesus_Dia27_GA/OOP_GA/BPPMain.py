import numpy as np # para estadísticos del experimento
from GeneticAlgorithm import * # Nuestro algoritmo genético
import matplotlib.pyplot as plt # Para pintar soluciones y/o evolución del GA
from BPPConfiguration import * # Configuración del problema


def Dibujar(problem, bins, printIds = False):
    print("Solución: ")
    binNum = 0
    for bin in bins:
        binNum = binNum + 1
        toStr = "Bin " + str(binNum) + ": ["
        totalWidth = 0
        for id in bin:
            width = problem.get_item_width(id)
            totalWidth = totalWidth + width
            if printIds:
                toStr = toStr + "item: " + str(id) + " ("+ str(width) + "), "
            else:
                toStr = toStr + str(width) + ", "
        toStr = toStr + "] TotalWidth: " + str(totalWidth)
        print(toStr)

# Función que lanza una ejecución del GA 
def run_GA():
    print("Ejecutando GA...")

    # creamos un objeto configuracion
    cfg = BPPConfiguration()
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
    Dibujar(cfg.problem, cfg.evaluator.evaluate(mejor_solucion), True)

# Halla la solución que está codificada por el vector fenotipo
def resolver(instance, fenotipo):
    problem = BPPProblem(instance)
    evaluator = BPPEvaluator(problem)
    contenedores = evaluator.evaluate(fenotipo)
    print('orden (%s)' % (fenotipo))
    Dibujar(problem, contenedores, True)


### ---------------------------------------------------------------------------
### PROGRAMA PRINCIPAL
### ---------------------------------------------------------------------------

resolver("./bpp.txt", [2, 0, 1, 3, 4, 7, 8, 9, 5, 6, 10, 11])
# run_GA()
