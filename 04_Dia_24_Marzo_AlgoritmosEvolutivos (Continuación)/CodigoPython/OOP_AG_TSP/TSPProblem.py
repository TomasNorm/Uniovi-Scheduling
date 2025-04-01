from numpy.random import permutation # para generar permutaciones
from numpy.random import randint # para generar los puntos de corte del cromosoma
from Solution import Solution # clase para representar a los individuos del GA

### ---------------------------------------------------------------------------
### CLASE PROBLEMA TSP
### ---------------------------------------------------------------------------

# clase TSPProblem:  modela una instancia del problema TSP
class TSPProblem:
    
    # nombre: nombre del fichero con la instancia a resolver
    # coordenadas: array con las coordenadas de las ciudades
    # costes: matriz de costes de las distancias entre las ciudades
    def __init__(self, file_name: str = ""):
        self.nombre = file_name
        if (self.nombre != ""):
            self.__lee_instancia()
        else:
            #instancia
            coordenadas = []
            #costes
            costes = []

    def __str__(self) -> str:
        return "Problema: " + self.nombre + ", Ciudades: " + str(len(self.coordenadas))        

    # Funcion para leer la instancia desde un fichero
    def __lee_instancia(self):
        # Leer el fichero del problema y crear la matriz de distancias
        self.coordenadas = self.__leer_fichero_TSP()
        self.costes= self.__crear_matriz_distancias(self.coordenadas)

    # Funcion para leer las coordenadas de un fichero
    def __leer_fichero_TSP(self):
        coordenadas=[]
        f = open(self.nombre,"r")
        f.readline()
        f.readline()
        f.readline()
        numlines = int(f.readline().split()[1])
        f.readline()
        f.readline()
        for i in range(numlines):
            li=f.readline()
            c = li.split()
            coord = [float(c[1]), float(c[2])]
            coordenadas.append(coord)
        return coordenadas

    # Funcion para crear la matriz de distancias, a partir de las coordenadas
    def __crear_matriz_distancias(self, coord):
        matriz = []
        for i in range(len(coord)):
            linea=[]
            for j in range(len(coord)):
                dist=((coord[i][0]-coord[j][0])**2 + (coord[i][1]-coord[j][1])**2)**(0.5)
                linea.append(dist)
            matriz.append(linea)
        return matriz

### ---------------------------------------------------------------------------
### CLASE GENERADORA DE INDIVIDUOS ALEATORIOS
### ---------------------------------------------------------------------------

# clase TSPCreatorRandom: Generadora de soluciones al problema TSP de forma aleatoria
class TSPCreatorRandom:

    # prob: objeto problema a resolver
    def __init__(self, problem) -> None:
        self.prob = problem
    
    # Genera individuo de permutaciones aleatorias
    def create(self) -> Solution:
        ciudades=[]
        for i in range(len(self.prob.costes)):
            ciudades.append(i)
    
        return Solution(permutation(ciudades))    

### ---------------------------------------------------------------------------
### CLASE GENERADORA DE INDIVIDUOS HEURISTICOS
### ---------------------------------------------------------------------------

# clase TSPCreatorHeuristic: Generadora de soluciones al problema TSP 
# utilizando el heurístico del vecino más cercano aleatorizado
class TSPCreatorHeuristic:
    def __init__(self, problem, num_candidatos = 3) -> None:
        self.prob = problem
        self.num_candidatos = num_candidatos

    # Función para crear una solución desde 0, utilizando el heurístico del vecino más cercano aleatorizado
    def create(self) -> Solution:
        solucion=[] 
        ciudadesporvisitar=[]
        for i in range(len(self.prob.costes)):
            ciudadesporvisitar.append(i)
        # La primera ciudad es aleatoria
        ciudadelegida=randint(len(self.prob.costes))
        solucion.append(ciudadelegida)
        ciudadesporvisitar.remove(ciudadelegida)
        # Para el resto de ciudades, elegidos una ciudad al azar de entre las "num_candidatos" ciudades aun no visitadas más cercanas
        while len(solucion)<len(self.prob.costes):
            # Para ello, elegimos las "num_candidatos" primeras ciudades que estén en "ciudadesporvisitar"
            candidatas=[]
            contador=0
            while len(candidatas)<self.num_candidatos and len(candidatas)<len(ciudadesporvisitar):
                candidatas.append(ciudadesporvisitar[contador])
                contador+=1
            # Miramos cual es la más lejana de ellas
            indicemaslejana=0
            for i in range(len(candidatas)):
                if self.prob.costes[solucion[len(solucion)-1]][candidatas[i]]>self.prob.costes[solucion[len(solucion)-1]][candidatas[indicemaslejana]]:
                    indicemaslejana=i
            # Y para cada una de las demás, comprobamos si es más cercana que la más lejana de entre las que ya teníamos
            while contador<len(ciudadesporvisitar):
                if self.prob.costes[solucion[len(solucion)-1]][ciudadesporvisitar[contador]]<self.prob.costes[solucion[len(solucion)-1]][candidatas[indicemaslejana]]:
                    candidatas[indicemaslejana]=ciudadesporvisitar[contador]
                    # Y si es asi, actualizamos la mas lejana
                    indicemaslejana=0
                    for i in range(len(candidatas)):
                        if self.prob.costes[solucion[len(solucion)-1]][candidatas[i]]>self.prob.costes[solucion[len(solucion)-1]][candidatas[indicemaslejana]]:
                            indicemaslejana=i
                contador+=1
            # Para acabar, elegimos una candidata al azar, la añadimos a la solución parcial, y la quitamos de ciudadesporvisitar
            elegida=randint(0,len(candidatas))
            solucion.append(candidatas[elegida])
            ciudadesporvisitar.remove(candidatas[elegida])
        # Y finalmente devolvemos la solucion completa
        return Solution(solucion)

### ---------------------------------------------------------------------------
### CLASE DECODIFICADORA DE SOLUCIONES
### ---------------------------------------------------------------------------

# clase TSPDecoder: decodifica una solución del problema TSP
class TSPDecoder:

    # prob: objto problema a resolver
    def __init__(self, problem) -> None:
        self.prob = problem

    # decodifica una solucion como la secuencia de ciudades a visitar (fenotipo = genotipo)
    def decode(self, sol):
        sol.fenotipo = sol.genotipo

### ---------------------------------------------------------------------------
### CLASE EVALUADORA DE SOLUCIONES
### ---------------------------------------------------------------------------

# clase Evaluator: Evalua una solución del problema TSP
class TSPEvaluator:

    # prob: objto problema a resolver
    def __init__(self, problem) -> None:
        self.prob = problem

    # evalua una solucion calculando la longitud del fenotipo: la ruta entre ciudades
    def evaluate(self, sol):
        solution = sol.fenotipo 
        # Función objetivo para calcular una ruta de forma completa
        suma = sum(self.prob.costes[solution[i]][solution[i+1]] for i in range(len(solution)-1))
        suma = suma + self.prob.costes[solution[len(solution)-1]][solution[0]]
        sol.fitness = suma 

"""
prueba = TSPProblem( "./rd100.tsp")
c = TSPCreatorRandom(prueba)
e = TSPEvaluator(prueba)
print(prueba)

sol = c.create()
print(sol)
e.evaluate(sol)
print(sol)
"""


"""print(prueba.nombre)
print(prueba.coordenadas)
print(prueba.costes)"""
