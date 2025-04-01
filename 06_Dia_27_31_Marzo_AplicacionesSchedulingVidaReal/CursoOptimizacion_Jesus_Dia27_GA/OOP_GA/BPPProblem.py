from numpy.random import permutation # para generar permutaciones
from numpy.random import randint # para generar los puntos de corte del cromosoma
from Solution import Solution # clase para representar a los individuos del GA

### ---------------------------------------------------------------------------
### CLASE PROBLEMA BPP
### ---------------------------------------------------------------------------

class BPPItem:
    def __init__(self, id, width):
        self.id = id
        self.width = width

# clase BPPProblem:  modela una instancia del problema BPP
class BPPProblem:
    # nombre: nombre del fichero con la instancia a resolver
    def __init__(self, file_name: str = ""):
        self.nombre = file_name
        if (self.nombre != ""):
            self.__lee_instancia()
        else:
            #instancia
            self.binSize = 0
            self.items = []

    def __str__(self) -> str:
        return "Problema: " + self.nombre + ", Items: " + str(len(self.items))        

    # Funcion para leer la instancia desde un fichero
    def __lee_instancia(self):
        self.items = []
        f = open(self.nombre,"r")
        c = f.readline().split(", ")
        self.binSize = int(c[0])
        numlines = int(c[1])
        id = 0
        for i in range(numlines):
            li = f.readline()
            c = li.split(", ")
            width = int(c[0])
            demand = int(c[1])
            for j in range(demand):
                item = BPPItem(id, width)
                self.items.append(item)
                id = id + 1

    # Para obtener el ancho a empaquetar a partir de su ID
    def get_item_width(self, id):
        for i in range(len(self.items)):
            item = self.items[i]
            if item.id == id:
                return item.width
        return None


### ---------------------------------------------------------------------------
### CLASE GENERADORA DE INDIVIDUOS ALEATORIOS
### ---------------------------------------------------------------------------

# clase BPPCreatorRandom: Generadora de soluciones al problema BPP de forma aleatoria
class BPPCreatorRandom:

    # prob: objeto problema a resolver
    def __init__(self, problem) -> None:
        self.prob = problem
    
    # Genera individuo de permutaciones aleatorias
    def create(self) -> Solution:
        itemIds=[]
        for i in range(len(self.prob.items)):
            itemIds.append(i)
    
        return Solution(permutation(itemIds))    

### ---------------------------------------------------------------------------
### CLASE DECODIFICADORA DE SOLUCIONES
### ---------------------------------------------------------------------------

# clase BPPDecoder: decodifica una solución del problema BPP
class BPPDecoder:

    # prob: objeto problema a resolver
    def __init__(self, problem) -> None:
        self.prob = problem

    # decodifica una solucion como la secuencia de items a empaquetar (fenotipo = genotipo)
    def decode(self, sol):
        sol.fenotipo = sol.genotipo

### ---------------------------------------------------------------------------
### CLASE EVALUADORA DE SOLUCIONES
### ---------------------------------------------------------------------------

# clase Evaluator: Evalua una solución del problema
class BPPEvaluator:

    # prob: objeto problema a resolver
    def __init__(self, problem) -> None:
        self.prob = problem

    # evalua una solucion
    def evaluate(self, sol):
        solution = sol
        if isinstance(sol, Solution):
            solution = sol.fenotipo

        # Nuestro planificador va a empaquetar el item de menor índice del fenotipo que aún no haya sido empaquetado
        #   Si no cabe en la bin actual, se omite
        #   Si llegamos al final del fenotipo y quedan items por empaquetar, volvemos a empezar desde el principio
        #   Si llegamos al final del fenotipo y todo está empaquetado, ya terminamos
        bins = []
        itemIds = solution
        packedIds = dict() #{} # Set de ids que han sido empaquetados, para omitirlos si nos los encontramos
        numItemsEmpaquetados = 0
        numItemsAEmpaquetar = len(solution)
        binSize = self.prob.binSize

        while (numItemsEmpaquetados < numItemsAEmpaquetar):
            bin = []
            binTotalWidth = 0
            for i in range(len(itemIds)):
                id = itemIds[i]
                width = self.prob.get_item_width(id)
                # Ha sido empaquetado?
                if not id in packedIds:
                    # Cabe en la bin?
                    if (binTotalWidth + width <= binSize):
                        # Cabe, lo empaquetamos
                        packedIds[id] = True
                        bin.append(id)
                        binTotalWidth = binTotalWidth + width
                        numItemsEmpaquetados = numItemsEmpaquetados + 1
            bins.append(bin)
        
        # El número de contenedores utilizados es nuestro objetivo a minimizar
        if isinstance(sol, Solution):
            sol.fitness = len(bins)
        return bins


"""
prueba = BPPProblem( "./bpp.txt")
c = BPPCreatorRandom(prueba)
d = BPPDecoder(prueba)
e = BPPEvaluator(prueba)
print(prueba)

sol = c.create()
d.decode(sol)
print(sol)
bins = e.evaluate(sol)
print(sol)

for bin in bins:
    toStr = "["
    totalWidth = 0
    for id in bin:
        width = prueba.get_item_width(id)
        totalWidth = totalWidth + width
        toStr = toStr + str(width) + ", "
    toStr = toStr + "] TotalWidth: " + str(totalWidth)
    print(toStr)
"""
"""print(prueba.nombre)
print(prueba.coordenadas)
print(prueba.costes)"""
