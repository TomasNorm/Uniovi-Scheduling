from random import random
from numpy.random import randint

### ---------------------------------------------------------------------------
### CLASE OPERADOR DE SELECCIÓN
### ---------------------------------------------------------------------------
    
# clase operador de seleccion por torneo
class TournamentSelection:
    # Constructor de la clase, inicializa los atributos necesarios para generar 
    # realizar la selección por torneo:
    # tam_torneo: número de individuos seleccionados al azar
    def __init__(self, tam_torneo) -> None:
        self.tam_torneo = tam_torneo

    # Método que elige una población completa de parejas
    # de individuos aplicando la selección por torneo tantas
    # veces como tamaño tenga la población
    def apply(self, poblacion):
        seleccionados = [self.__select(poblacion) for _ in range(len(poblacion))]
        return seleccionados

    # Método que selecciona un individuo por torneo tam_torneo:1
    # Escoge el mejor entre los tam_torneo escogidos al azar
    def __select(self, poblacion):
        # Elegimos un individuo aleatorio
        elegido = randint(len(poblacion))
        for i in randint(0, len(poblacion), self.tam_torneo-1):
            # Comprobamos si es mejor (es decir, hacemos un torneo)
            if poblacion[i].fitness < poblacion[elegido].fitness:
                elegido = i
        return poblacion[elegido]   


### ---------------------------------------------------------------------------
### CLASE OPERADOR DE CRUCE
### ---------------------------------------------------------------------------

# clase operador de cruce basado en orden (OX)   
class OrderCrossover:

    # Constructor, inicializamos los atributos del operador:
    # p_cruce: probabilidad de cruce
    def __init__(self, p_cruce) -> None:
        self.p_cruce = p_cruce
    
    # Método que cruza dos progenitores para crear dos hijos (Order Crossover)
    def apply(self, p1, p2):
        # Los hijos, por defecto, son copias de los padres
        c1, c2 = p1.copy(), p2.copy()
        # Comprobamos si hay que cruzarlos (probabilidad de cruce)
        if random() < self.p_cruce:
            puntomin = randint(0, len(p1))
            puntomax = randint(0, len(p1))
            while puntomin==puntomax:
                puntomax = randint(0, len(p1))
            if puntomin > puntomax:
                puntomin, puntomax = puntomax, puntomin
            punterop1 = 0
            punterop2 = 0
            for i in range(len(p1)):
                if i < puntomin or i > puntomax:
                    while p2[punterop2] in c1[puntomin:puntomax+1]:
                        punterop2 += 1
                    c1[i] = p2[punterop2]
                    punterop2 += 1
                    while p1[punterop1] in c2[puntomin:puntomax+1]:
                        punterop1 += 1
                    c2[i] = p1[punterop1]
                    punterop1 += 1
        return [c1, c2]


### ---------------------------------------------------------------------------
### CLASE OPERADOR DE MUTACIÓN
### ---------------------------------------------------------------------------
    
# clase operador de mutación basado en intercambio de 2 genes al azar (SWAP)   
class SwapMutation:

    # Constructor, inicializamos los atributos del operador:
    # p_mut: probabilidad de mutación
    def __init__(self, p_mut) -> None:
        self.p_mut = p_mut
        
    # Método que recibe un cromosoma y se muta intercambiando la posición de dos genes al azar (SWAP)
    def apply(self, cromosoma):
        # Comprobamos si hay que mutarlo
        if random() < self.p_mut:
            punto1 = randint(0, len(cromosoma))
            punto2 = randint(0, len(cromosoma))
            cromosoma[punto1],cromosoma[punto2] = (cromosoma[punto2], cromosoma[punto1])
        #print("Mutacion")    
        return cromosoma


### ---------------------------------------------------------------------------
### CLASE OPERADOR DE REEMPLAZO
### ---------------------------------------------------------------------------

# clase operador de remplazo generacional     
class GenerationalReplacement:

    # Constructor
    def __init__(self) -> None:
        pass

    # Método que recibe las poblaciones de progenitores e hijos y devuelve directamente
    # la población de hijos
    def apply(self, progenitores, hijos):
        return hijos
    

