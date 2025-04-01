from numpy.random import permutation # para generar permutaciones
from numpy.random import randint # para generar los puntos de corte del cromosoma
from random import random # para vefiricar la probabilidad de cruce
from Solution import Solution
from PlanificadorCompleto.SchedulerGenerator import SchedulerGenerator
from PlanificadorCompleto.rules import GA_rule # clase para representar a los individuos del GA

### ---------------------------------------------------------------------------
### CLASE PROBLEMA JSSP
### ---------------------------------------------------------------------------

# Clase que contiene la información del problema
class Problem:
    
    # Constructor, inicializamos los atributos de la clase Problema a un
    # problema vacío   
    # file_name: nombre del fichero con la instancia del problema, puede recibirlo o no
    # name: nombre de la instancia (nombre del fichero con la instancia sin ruta ni extension)
    # num_jobs: número de trabajos
    # num_machines: número de máquinas
    # pi: vector con las duraciones de las tareas
    # mi: vector con las máquinas requeridas por las tareas
    def __init__(self, file_name = ""):
        if (file_name != ""):
            self._read_data(file_name)
            #self._print_data() 
        else:
            # Nombre del archivo con la instancia del problema a resolver
            self.file_name = ""
            # Nombre de la instancia
            self.name = ""
            # Numero de trabajos
            self.num_jobs = 0
            # Numero de máquinas
            self.num_machines = 0
            # Vector con las duraciones de las tareas
            self.pi = []
            # Vector con las máquinas que requieren las tareas
            self.mi = []
    
    # Método que lee los datos del problema del fichero de intancia file_name
    # y los guarda en los atributos de la clase
    def _read_data(self, file_name):
        # Leemos los datos de la instancia del problema del archivo file_name
        # Leer los datos del archivo de texto, y almacenarlos en un vector por columnas
        # a b c
        # d e f
        # se almacenaria
        # a d b e c f
        self.file_name = file_name
        l_name_inst = file_name.split("\\")  # Obtenemos la lista con las partes de la ruta a la instancia separadas por \
        name_inst = l_name_inst[len(l_name_inst) - 1] # Sacamos de la ruta el nombre de la instancia, será el último elemmento de la lista
        self.name = name_inst.split(".")[0] # Le quitamos la extension
            

        # Leemos del archivo file_name los datos del problema: número de trabajos
        # número de máquinas, duración tareas y máquina que requieren
        with open(self.file_name, 'r') as file:
            self.num_jobs, self.num_machines = map(int, file.readline().split()) # Número de trabajos y máquinas
            # Inicializamos los vectores con las duraciones de las tareas y las máquinas
            self.pi=[0] * self.num_jobs*self.num_machines # Vector con las duraciones de las tareas
            self.mi=[0] * self.num_jobs*self.num_machines # Vector con las máquinas de las tareas
            for j in range(self.num_jobs):  
                # Leemos la línea con los datos de un trabajo
                job = list(map(int, file.readline().split())) 
                t=j
                for i in range(0, len(job),2):
                    self.mi[t]=job[i]
                    self.pi[t]=job[i+1] 
                    t=t+self.num_jobs
    
    # Método que muestra los datos del fichero leido tal cual aparecen
    # en el fichero. Así como los atributos vector de furaciones (pi) y 
    # vector de máquinas (mi) cargados desde el fichero
    def _print_data(self):
        print("Instancia ", self.file_name)
        print(self.num_jobs," ", self.num_machines)
        for j in range(self.num_jobs):
            k=j;
            while k<(self.num_jobs*self.num_machines):
                print(self.mi[k],self.pi[k],end=" ")
                k=k+self.num_jobs;
            print() 
        print(self.pi)
        print(self.mi)

#nuevo
    def __str__(self) -> str:
        return "Problema: " + self.file_name + ", Trabajos: " + str(self.num_jobs) + ", Máquinas:  " + str(self.num_machines)
 

### ---------------------------------------------------------------------------
### CLASE OPERADOR DE CREACIÓN DE INDIVIDUOS
### ---------------------------------------------------------------------------
    
# clase Creator: Generadora de soluciones al problema basadas en permutaciones con repitición
class JSSPCreatorRandomRP:

    # Constructor, inicializamos los atributos del operador:
    # problem: objeto que modela la instancia resuelta
    def __init__(self, problem) -> None:
        self.prob = problem

    
    # Método que genera un individuo de permutaciones aleatorias de tareas identificadas por su "trabajo"
    def create(self) -> Solution:
        tareas=[]
        for i in range(self.prob.num_jobs):
            for j in range(self.prob.num_machines):
                tareas.append(i)
    
        tareas = permutation(tareas)
        
        return Solution(genotipo = tareas) 


### ---------------------------------------------------------------------------
### CLASE OPERADOR DE DECODIFICACION DE INDIVIDUOS
### ---------------------------------------------------------------------------
    
# clase JSSPdecoderRP: decodifica una solución del problema JSSP
class JSSPDecoderRP:

    # prob: objto problema a resolver
    def __init__(self, problem) -> None:
        self.prob = problem

    # decodifica una solucion (fenotipo) como un diccionario conteniendo:
    # "st" -> la secuencia de tiempos de inicio de cada tarea
    # "makespan" -> el maximo tiempo de finalización de todas las tareas
    def decode(self, sol):
        solution = sol.genotipo  # genotype
        last_time_job = [] # instante de finalizacion de ultima tarea por trabajo
        last_time_machine = [] # instante de finalizacion de ultima tarea por trabajo
        next_task_job = [] # sgte tarea a planificar en el trabajo
        for i in range(self.prob.num_jobs):
            last_time_job.append(0)
        for i in range(self.prob.num_machines):
            last_time_machine.append(0)
        for i in range(self.prob.num_jobs):
            next_task_job.append(i)
        # tiempo de inicio de cada tarea
        st = [0 for _ in range(self.prob.num_jobs * self.prob.num_machines)]

        for id_job in solution:
            id_task = next_task_job[id_job]
            #print(id_task)
            id_machine = self.prob.mi[id_task]
            t_ini = max(last_time_job[id_job], last_time_machine[id_machine])
            t_fin = t_ini + self.prob.pi[id_task]
            st[id_task] = t_ini
            # actualizamos tiempo de fin de trabajo y maquina
            last_time_job[id_job] = t_fin
            last_time_machine[id_machine] = t_fin
            #avanza tarea en el trabajo
            next_task_job[id_job] += self.prob.num_jobs 

        # definimos el fenotipo
        sol.fenotipo = dict()
        sol.fenotipo["st"] = st
        sol.fenotipo["makespan"] = max(last_time_job)
 
### ---------------------------------------------------------------------------
### CLASE OPERADOR DE EVALUACIÓN DE INDIVIDUOS
### ---------------------------------------------------------------------------
    
# clase Evaluator: Evalua una solución del problema JSSP utilizando como  valor 
# de la función objetivo el Makespan
class JSSPEvaluatorRP:

    # Constructor, inicializamos los atributos del operador:
    # prob: objeto que modela la instancia resuelta
    def __init__(self, problem) -> None:
        self.prob = problem

    # Método que evalua una solución
    def evaluate(self, sol):
        sol.fitness = sol.fenotipo["makespan"]

### ---------------------------------------------------------------------------
### CLASE OPERADOR DE CRUCE DE INDIVIDUOS
### ---------------------------------------------------------------------------
        
# Operador de cruce GOX (Generalized Order Crossover)
class CrossoverGOX:
    
    # Constructor, inicializamos los atributos del operador:
    # p_cruce: probabilidad de cruce
    # prob: objeto que modela la instancia resuelta
    def __init__(self, p_cruce, prob: Problem) -> None:
        self.p_cruce = p_cruce
        self.prob = prob
        self.p1_NRP = [0] * (self.prob.num_jobs * self.prob.num_machines)
        self.p2_NRP = [0] * (self.prob.num_jobs * self.prob.num_machines)
        
    def set_problem(self, prob: Problem):
        self.prob = prob
        self.p1_NRP = [0] * (self.prob.num_jobs * self.prob.num_machines)
        self.p2_NRP = [0] * (self.prob.num_jobs * self.prob.num_machines)


  # Método que cruza dos padres generando dos descendientes cruzados
    def apply(self, p1, p2):
        # Comprobamos si hay que cruzarlos (probabilidad de cruce)
        if random() < self.p_cruce:
            # convierte la permutación con repetición en permutación SIN repetición
            p1_NRP = self.__from_RP_to_NRP(p1)
            p2_NRP = self.__from_RP_to_NRP(p2)

            # aplica el cruce basado en orden OrderedCrossover (OX) para permutaciones SIN repetición
            [c1, c2] = self.__apply(p1_NRP, p2_NRP)

            # devuelve los individuos cruzados de nuevo como permutaciones CON repetición
            return [self.__from_NRP_to_RP(c1), self.__from_NRP_to_RP(c2)]


        else:
            return [p1.copy(), p2.copy()]    

  

    # Método que cruza dos padres generando dos descendientes cruzados
    def apply_optimizado(self, p1, p2):
        # Comprobamos si hay que cruzarlos (probabilidad de cruce)
        if random() < self.p_cruce:
            # convierte la permutación con repetición en permutación SIN repetición
            self.__from_RP_to_NRPv2(p1, p2)
            

            # aplica el cruce basado en orden OrderedCrossover (OX) para permutaciones SIN repetición
            [c1, c2] = self.__apply(self.p1_NRP, self.p2_NRP)

            # devuelve los individuos cruzados de nuevo como permutaciones CON repetición
            self.__from_NRP_to_RPv2(c1, c2)
            
            return [c1, c2]


        else:
            return [p1.copy(), p2.copy()]    

        
    # Método que cruza dos padres para crear dos hijos (Order Crossover)
    def __apply(self, p1, p2):
        
        # Los hijos, por defecto, son copias de los padres
        c1, c2 = p1.copy(), p2.copy()
        
        puntomin = randint(0, len(p1))
        puntomax = randint(0, len(p1))
        while puntomin==puntomax:
            puntomax = randint(0, len(p1))
        if puntomin > puntomax:
            puntomin, puntomax = puntomax, puntomin
        #print(f"puntomin:{puntomin} puntomax:{puntomax}")
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

    # Método auxiliar que pasa de una permutación CON repetición a una SIN repetición
    def __from_RP_to_NRP(self, cromosome):
        max = self.prob.num_jobs
        counters =  [0  for x in range(max)] 
        cromosome_NRP = []
        for i in cromosome:
            cromosome_NRP.append((i,counters[i]))
            counters[i] += 1

        return cromosome_NRP
    
    # Método auxiliar que pasa de una permutación SIN repetición a una CON repetición
    def __from_NRP_to_RP(self, cromosome):
        cromosome_RP = [i for (i,j) in cromosome]
        
        return cromosome_RP
    
 # Método auxiliar que pasa de una permutación CON repetición a una SIN repetición
    def __from_RP_to_NRPv2(self, cromosome1, cromosome2):

        counters =  [0  for x in range(self.prob.num_jobs)]
        pos = 0
        for i in cromosome1:
            self.p1_NRP[pos] = [i, counters[i]]
            counters[i] += 1
            pos += 1

        counters =  [0  for x in range(self.prob.num_jobs)]
        pos = 0
        for i in cromosome2:
            self.p2_NRP[pos] = [i, counters[i]]
            counters[i] += 1
            pos += 1
        
    
    # Método auxiliar que pasa de una permutación SIN repetición a una CON repetición
    def __from_NRP_to_RPv2(self, cromosome1, cromosome2):
        for i in range(len(cromosome1)):
            cromosome1[i] = cromosome1[i][0]
            cromosome2[i] = cromosome2[i][0]
    
### ---------------------------------------------------------------------------
### CLASE OPERADOR DE CRUCE DE INDIVIDUOS
### ---------------------------------------------------------------------------
        
# Operador de cruce PPX (Partia Preservative Order Crossover)
class CrossoverPPX:
    
    # Constructor, inicializamos los atributos del operador:
    # p_cruce: probabilidad de cruce
    # prob: objeto que modela la instancia resuelta
    def __init__(self, p_cruce, prob) -> None:
        self.p_cruce = p_cruce
        self.prob = prob
    
    # Método que cruza dos padres generando dos descendientes cruzados
    def apply(self, p1, p2):
        # Comprobamos si hay que cruzarlos (probabilidad de cruce)
        if random() < self.p_cruce:
            c1, c2 = [],[]
            i1, i2 = 0, 0
            for i in range(0, len(p1)):
                if (random() < 0.5):
                    # busco primer gen de p1 que no esta en c1
                    while p1[i1] in c1:
                        i1 += 1
                    # y lo añado a c1
                    c1.append(p1[i1])
                    i1 += 1
                    # busco primer gen de p2 que no esta en c2
                    while p2[i2] in c2:
                        i2 += 1
                    # y lo añado a c2
                    c2.append(p2[i2])
                    i2 += 1
            return [c1, c2]
        else:
            return [p1.copy(), p2.copy()]    


### ---------------------------------------------------------------------------
### CLASE OPERADOR DE DECODIFICACION DE INDIVIDUOS
### ---------------------------------------------------------------------------
    
# clase JSSPdecoderRP: decodifica una solución del problema JSSP
class JSSPDecoderGyT:

    # prob: objto problema a resolver
    def __init__(self, problem: Problem) -> None:
        self.prob = problem

        # "Scheduler.py" ft03.txt RR MK
        self.sch = SchedulerGenerator(self.prob.file_name, "GA", "MK")

    # decodifica una solucion (fenotipo) como un diccionario conteniendo:
    # "st" -> la secuencia de tiempos de inicio de cada tarea
    # "makespan" -> el maximo tiempo de finalización de todas las tareas
    def decode(self, sol):

        GA_rule.genotipo = sol.genotipo # genotype
        coste_gyt = self.sch.execute_GyT()   

        # definimos el fenotipo
        sol.fenotipo = dict()
        sol.fenotipo["st"] = self.sch.sol.st
        sol.fenotipo["makespan"] = coste_gyt
 

              


def pruebaRP():
    #creamos un problema JSSP
    problem = Problem(".\\instances\\la16.txt")
    print(problem)
    
    #creamos operadores JSSP
    creator = JSSPCreatorRandomRP(problem)
    decoder = JSSPDecoderRP(problem)
    evaluator = JSSPEvaluatorRP(problem)

    # muestra operadores

    # crea una nueva solucion y muestrala (solo debería tener genotipo)
    solution = creator.create()
    print (f"Solución inicial \n{solution}\n")

    # decodifica la solucion y muestrala de nuevo (ahora debería tener fenotipo)
    decoder.decode(solution)
    print (f"Solución decodificada \n{solution}\n")

    # evalua la solucion y muestrala de nuevo (ahora debería tener fitness)
    evaluator.evaluate(solution)
    print (f"Solución evaluada \n{solution}\n")
    
    # creamos operador de cruce GOX para JSSP con p_cruce=1.0
    xop = CrossoverGOX(1.0, problem)
    # muestra el operador
    # crea una segunda solucion
    solution2 = creator.create()
    # muestra la segunda solucion
    print (f"Segunda solución \n{solution2}\n")

    # cruza las dos soluciones y recoge el resultado en: genotipo_hijos
    genotipo_hijos = xop.apply(solution.genotipo, solution2.genotipo)

    # muestra el genotipo de los hijos

    # convierte los genotipos en nuevas soluciones: hijos

    # muestra los hijos

    print("Tras un cruce")
    hijos = [Solution(genotipo) for genotipo in xop.apply(solution.genotipo, solution2.genotipo)]
    for hijo in hijos:
        print(hijo)



#pruebaRP()

'''#creamos un problema JSSP
problem = Problem(".\\la16.txt")
print(problem)

#creamos operadores JSSP
creator = JSSPCreatorRandomRP(problem)
decoder = JSSPDecoderGyT(problem)
decoder0 = JSSPDecoderRP(problem)
evaluator = JSSPEvaluatorRP(problem)

# muestra operadores

# crea una nueva solucion y muestrala (solo debería tener genotipo)
solution = creator.create()
print (f"Solución inicial \n{solution}\n")

# decodifica la solucion y muestrala de nuevo (ahora debería tener fenotipo)


decoder.decode(solution)
print (f"Solución decodificada GyT\n{solution}\n")
decoder0.decode(solution)
print (f"Solución decodificada Semiactiva Directa\n{solution}\n")
'''