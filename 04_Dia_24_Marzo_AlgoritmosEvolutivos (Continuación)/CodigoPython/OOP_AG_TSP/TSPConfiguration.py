# Operadores independientes de problema y representación
from  Operators import GenerationalReplacement, TournamentSelection 
# Operadores dependientes de la representación
from  Operators import OrderCrossover, SwapMutation
# Operadores específicos del problema y la representación
from TSPProblem import TSPProblem, TSPCreatorHeuristic, TSPCreatorRandom, TSPDecoder,  TSPEvaluator



### ---------------------------------------------------------------------------
### CLASE CONFIGURACIÓN DEL ALGORITMO GENÉTICO RESOLVIENDO UNA INSTANCIA TSP
### ---------------------------------------------------------------------------

# Clase contenedora de la configuración del algoritmo genético para resolver el problema TSP
# contiene tanto los parámetros:
# Tamaño población
# Criterio de parada: número de generaciones y tiempo máximo de ejecución
# Probabilidad de cruce y probabilidad de mutación
# Uso de elitismo

# Objeto instancia TSP a resolver
# Objeto operador creacional
# Objeto operador decodificación
# Objeto operador evaluación
# Objeto operador selección
# Objeto operador reemplazamiento
# Objeto operador cruce
# Objeto operador mutacion
class TSPConfiguration:

    # =======PARAMETROS PARA CONFIGURAR EL ALGORITMO GENETICO/MEMETICO===============
    # Tamaño de la población
    n_poblacion = 100
    # Número total de generaciones (criterio de parada)
    max_gen = 100
    # Tamaño del torneo (operador de seleccion)
    tam_torneo = 8
    # Probabilidad de cruce
    p_cruce = 0.9
    # Probabilidad de mutación
    p_mut = 0.1
    # Elitismo
    elitismo = True
 
    # =======PARAMETRO PARA CONFIGURAR EL TIEMPO MAXIMO EN SEGUNDOS===============
    # Tiempo máximo de ejecución en segundos (criterio de parada)
    tiempo_maximo = 6000

    # instancia a resolver
    problem = TSPProblem("./rd100.tsp")
    
    # operadores del algoritmo genetico (objetos)

    # operadores independientes del problema y la representacion
    # seleccion
    selection = TournamentSelection(tam_torneo)
    # reemplazamiento
    replace = GenerationalReplacement()
    
    # operadores dependientes de la representacion (y el problema)
    # cruce
    crossover = OrderCrossover(p_cruce)
    # mutacion
    mutation = SwapMutation(p_mut)

    # operadores dependientes del problema y la representacion
    # creacion: TSPCreatorRandom o  TSPCreatorHeuristic
    creator = TSPCreatorHeuristic(problem, num_candidatos = 3)
    #creator = TSPCreatorRandom(problem)

    # decodificacion y evaluacion
    decoder = TSPDecoder(problem)
    evaluator = TSPEvaluator(problem)

    # constructor de la clase, se limita a mostrar el nombre de 
    # la instancia configurada para ser resuelta
    # todos los atributos son estáticos y se fijan al iniciarse la ejecución
    def __init__(self, file_name = None) -> None:
        if (file_name != None):
            self.problem = TSPProblem(file_name) 
            self.crossover.prob = self.problem
            self.creator.prob = self.problem
            self.evaluator.prob = self.problem
        print(f"Configuración TSP generada para {self.problem}")


