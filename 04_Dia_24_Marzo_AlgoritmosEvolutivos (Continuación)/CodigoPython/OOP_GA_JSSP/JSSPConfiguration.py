# Operadores independientes de problema y representación
from Operators import GenerationalReplacement, SwapMutation, TournamentSelection
# Operadores específicos del problema y la representación
from JSSPProblem import CrossoverGOX, CrossoverPPX, JSSPCreatorRandomRP, JSSPDecoderGyT, JSSPDecoderRP, JSSPEvaluatorRP, Problem

### ---------------------------------------------------------------------------
### CLASE CONFIGURACIÓN DEL ALGORITMO GENÉTICO RESOLVIENDO UNA INSTANCIA JSPP
### ---------------------------------------------------------------------------

# Clase contenedora de la configuración del algoritmo genético para resolver el problema JSSP
# contiene tanto los parámetros:
# Tamaño población
# Criterio de parada: número de generaciones y tiempo máximo de ejecución
# Probabilidad de cruce y probabilidad de mutación
# Uso de elitismo

# Objeto instancia JSSP a resolver
# Objeto operador creacional
# Objeto operador evaluación
# Objeto operador selección
# Objeto operador reemplazamiento
# Objeto operador cruce
# Objeto operador mutacion
class JSSPConfiguration:

  
    # =======PARAMETROS PARA CONFIGURAR EL ALGORITMO GENETICO===============
    # Tamaño de la población
    n_poblacion = 100
    # Número total de generaciones (criterio de parada)
    max_gen = 100
    # Tamaño del torneo (operador de seleccion)
    tam_torneo = 8
    # Probabilidad de cruce
    p_cruce = 0.9
    # Probabilidad de mutación
    p_mut = 0.2
    # Elitismo
    elitismo = True

    # =======PARAMETRO PARA CONFIGURAR EL TIEMPO MAXIMO EN SEGUNDOS===============
    # Tiempo máximo de ejecución en segundos
    tiempo_maximo = 6000


    # instancia a resolver
    #problem = Problem(".\\ft06.txt")
    problem = Problem("la16.txt")
    
    # operadores del algoritmo genetico

    # operadores independientes del problema y la representacion
    # seleccion
    selection = TournamentSelection(tam_torneo)
    # reemplazamiento
    replace = GenerationalReplacement()
    
    # operadores dependientes de la representacion (y el problema)
    # cruce
    crossover = CrossoverGOX(p_cruce, problem)
    #crossover = CrossoverPPX(p_cruce, problem)
    
    # mutacion
    mutation = SwapMutation(p_mut)

    # operadores dependientes del problema y la representacion
    # creacion: TSPCreatorRandom o  TSPCreatorHeuristic
    #creator = TSPCreatorRandom(problem)
    creator = JSSPCreatorRandomRP(problem)

    # decodificacion y evaluacion
    decoder = JSSPDecoderRP(problem)
    #decoder = JSSPDecoderGyT(problem)
    evaluator = JSSPEvaluatorRP(problem)

    # constructor de la clase, se limita a mostrar el nombre de 
    # la instancia configurada para ser resuelta
    # todos los atributos son estáticos y se fijan al iniciarse la ejecución
    def __init__(self, file_name = None) -> None:
        if (file_name != None):
            self.problem = Problem(file_name) 
            self.crossover.set_problem(self.problem)#self.crossover.prob = self.problem
            self.creator.prob = self.problem
            self.decoder.prob = self.problem #<!>
            self.evaluator.prob = self.problem

        
        print(f"Configuración JSSP generada para {self.problem}")

            # <!> metodo que muestra la configuracion actual
    def __str__(self) -> str:
        config = "Configuration:\n"
        config += "Problem: " + str(self.problem) + "\n"
        config += "Creator: " + str(self.creator) + "\n"
        config += "Decoder: " + str(self.decoder) + "\n"
        config += "Evaluator: " + str(self.evaluator) + "\n"
        config += "Selection: " + str(self.selection) + "\n"
        config += "Replacement: " + str(self.replace) + "\n"
        config += "Crossover: " + str(self.crossover) + "\n"
        config += "Mutation: " + str(self.mutation) + "\n"
        

        return config     
    


