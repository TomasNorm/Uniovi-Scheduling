from . Problem import *
from . Solution import *
from . rules import *
from . objective_functions import *

### ---------------------------------------------------------------------------
### CLASE GENERADOR DE SCHEDULES
### ---------------------------------------------------------------------------

# Clase para generar las planificaciones              
class SchedulerGenerator:
    
    # Constructor de la clase, inicializa los atributos necesarios para generar 
    # una planificación:
    # configuracion: string con los datos de la planificación:
    #                nombre del fichero, la regla y la función objetivo
    # prob: objeto de la clase problema con la información del problema a resolver
    # sol: objeto de la clase solución donde guardar la solución del problema
    # _select_rule: nombre de la función de la regla a aplicar
    # _select_objective_functiongyt: nombre de la función objetivo a considerar
    def __init__(self, file_name, rule, objectiveF):
        # cargamos la instancia
        self.prob = Problem(file_name)

        # creamos una solucion inicial
        self.sol = Solution(self.prob)
        
        # describimos la configuración de la planificación que no cambia
        self.configuration = self.prob.name + "_" + rule + "_" + objectiveF   

        # nombre del fichero de grafica de salida, se incializa con la
        # confifuración pero va a contener también el tipo de la
        # planificación, este 
        self.graphName = self.configuration
    
        # escogemos la regla a aplicar
        self._select_rule = rule_factory(rule)

        # escogemos la funcion objetivo a evaluar
        self._objective_function = objective_fuction_factory(objectiveF)

    
                    
    # Método que ejecuta un planificador sencillo. Parte de una planificación
    # vacía, en cada paso calcula las tareas de los trabajos candidatas a ser planificadas
    # (primeras sin planificar de cada trabajo) y selecciona la siguiente a planificar
    # aplicando una regla de prioridad (RR, SPT, LPT, ...)
    # Cuando tiene la planificación solución, calcula el coste de la misma 
    # según la funcion objetivo considerada (MK, TFT) y lo retorna
    def execute_basic_scheduler(self):
       # Inicializamos las estructuras de la solución
       self._initialize("_basic")

       # Inicializamos el contador de tareas a planificar al nº de tareas totales del problema 
       unscheduledTasks = self.prob.num_jobs*self.prob.num_machines

       # Construir conjunto tareas candidatas a ser planificadas (primeras tareas sin planificar de cada trabajo)
       A = self._first_unschedule_tasks()
       
       # Mientras no se hayan planificado todas las tareas
       while (unscheduledTasks > 0):
           # Elegimos mediante una función de prioridad la siguiente tarea a planificar
           task = self._select_rule(A, self.prob)
           # La planificamos
           self._schedule_task(task)
           # Actualizamos el conjunto de tareas no planificadas:
           # Borrar la tarea planificada de US y añadir la siguiente del
           # tabajo
           #print(A, "task", task)
           A = self._update_A(A,task)
           #print(A)
           # Actualizar la función objetivo
           self.sol.objectiveCost=self._objective_function(self.prob, self.sol)
           # Decrementamos el contador de las tareas sin planificar
           unscheduledTasks -= 1

       return self.sol.objectiveCost    
   
    # Método que ejecuta un planifocador G&T. Parte de una planificación
    # vacía, en cada paso calcula las tareas de los trabajos candidatas a ser planificadas
    # (primeras sin planificar de cada trabajo) --> Conjunto A
    # A <-- Tareas candidatas a ser planificadas
    # Mientras que A no esté vacío
    #    Construir el conjunto B: para ello primero determina el menor tiempo de fin de las 
    #    tareas del conjunto A, valor C, y seja en B las tareas que emplean la misma máquina
    #    que la tarea que determinó C y pueden comenzar antes que C.
    #    Obviamente la tarea que determina C siempre estará en el conjunto B
    #    Selecciona de B la siguiente tarea a planificar aplicando algún criterio 
    #    una regla de prioridad (RR, SPT, LPT)
    #    Recalcular A <-- Tareas candidatas a ser planificadas
    # Cuando tiene la planificación solución, todas las tareas planificadas
    # calcula el coste de la misma según la funcion objetivo considerada (MK, TFT) y lo retorna
    def execute_GyT(self):
       # Inicializamos las estructuras 
       self._initialize("_gyt")

       # Inicializamos el contador de tareas a planificar al nº de tareas totales del problema       
       unscheduledTasks = self.prob.num_jobs*self.prob.num_machines
       
       # Construir conjunto tareas candidatas a ser planificadas (primeras tareas sin planificar de cada trabajo)
       A = self._first_unschedule_tasks()
       
       while (unscheduledTasks > 0):
           
           # Construir el conjunto B
           B = self._calculate_set_B(A)

           # Elegimos mediante una función de prioridad la siguiente tarea a planificar
           task = self._select_rule(B, self.prob)

           self._schedule_task(task)
           # Actualizamos el conjunto de tareas no planificadas:
           # Borrar la tarea planificada de US y añadir la siguiente del
           # tabajo
           A = self._update_A(A,task)
           # Actualizar la función objetivo
           self.sol.objectiveCost=self._objective_function(self.prob,self.sol)
           # Decrementamos el contador de las tareas sin planificar
           unscheduledTasks -= 1

       return self.sol.objectiveCost   
    
    # Método que pinta el diagrama de Gannt de la solución calculada 
    def paint_gannt_schedule(self):
        self.sol.paint_gantt(self.graphName+".jpg")

    # Método que salva a fichero la solución calculada
    def save_solution(self):
        self.sol.save_solution(self.graphName)

    # Método que inicializa la solución y la descripción de la planificación
    # permite realizar varias ejecuciones del panificador con la configuración
    # Recibe como argumento el tipo de planificador a utilizar:
    # _basic: Planificador básico
    # _gyt: Planificador G&T
    def _initialize(self, scheduleType):
        self.sol.init_solution()
        self.graphName = self.configuration+scheduleType
          
    # Método que calcula las primeras tareas sin planificar de cada trabajo
    # y las rectorna en el vector US     
    def _first_unschedule_tasks(self):
        US = []
        for j in range(self.prob.num_jobs):
            k = j;
            while k < (self.prob.num_jobs*self.prob.num_machines):
                if not self.sol.scheduled_tasks[k]:
                    US.append(k)
                    break
                k = k + self.prob.num_jobs
        return US
    
    # Método que planifica la tarea que recibe como argumento
    # La marca como planificada en scheduled_tasks
    # Calcula su tiempo de inicio como maximo entre el tiempo de fin de la
    # tarea anterior en el trabajo y de la tarea anterior en la máquiba
    # Actualiza el tiempo de fin de la máquina que requiere la tarea planificada
    # en la estructura "endTimeMachine"
    def _schedule_task(self,task):
        
        #Planificamos la tarea seleccionada
        self.sol.scheduled_tasks[task] = True

        # Calculamos el mínimo tiempo de inicio de la tarea planificada
        # Como el máximo entre: el tiempo de fin de la tarea anterior en
        # el trabajo y en la máquina
        # Calculamos el tiempo de fin de la tarea anterior en el trabajo
        if task >= self.prob.num_jobs:   
            # si no es la primera tarea del trabajo, su tiempo de inicio será 
            # el tiempo de fin de la tarea anterior en el trabajo, es decir
            # el tiempo de inicio mas la duración de la tarea anterior en el 
            # trabajo
            previousTaskInJob = task - self.prob.num_jobs  
            endBeforeJob = self.sol.st[previousTaskInJob] + self.prob.pi[previousTaskInJob];        
        else:
            # Si es la primera del trabajo será 0 
            endBeforeJob = 0

        # Obtenemos el tiempo de fin de la tarea anterior en la máquina
        endBeforeMachine = self.sol.endTimeMachine[self.prob.mi[task]]

        # Asignamos el tiempo de inicio a la tarea planificada   
        self.sol.st[task] = max(endBeforeJob, endBeforeMachine)
        
        # Actualizamos el tiempo de fin de la máquina, al de fin de la última
        # tarea planificada en la máquina
        tfin_task = self.sol.st[task] + self.prob.pi[task]
        self.sol.endTimeMachine[self.prob.mi[task]] = tfin_task

    # Mérodo que actualiza el conjunto de tareas planificadas
    # borra una tarea del conjunto de tareas a planificar
    # y añade la siguiente tarea del trabajo al que pertenece la 
    # tarea borrada
    def _update_A(self, A, task):
        # Borrar la tarea planificada de US y añadir la siguiente del
        # trabajo
        #i=A.index(task)
        A.remove(task)
        next_task_job = task + self.prob.num_jobs
        if next_task_job < (self.prob.num_jobs*self.prob.num_machines):
            #A.insert(i,next_task_job) # Inserta en la posición i la siguiente tarea sin planificar del trabajo
            A.append(next_task_job) # En realidad se podría hacer con append pues el orden de insercción no es relevante
        return A
  
    # Método que construye el conjunto B a partir del conjunto A, con las tareas candidatas
    # a ser planificadas, cuya planificación garantiza mantener un schedule activo 
    # Para ello:
    # Se determina C: menor tiempo de fin de las tareas del conjunto A
    # Se introduce en B las tareas de A que emplean la misma máquinan que la tarea que deteminó C
    # y pueden comenzar antes que C
    def _calculate_set_B(self, A):
        #Inicializamos B a vacío
        B = []

        # Calculamos los tiempos de inicio de las tareas del conjunto A:
        # max (tfin anterior trabajo, tfin anterior máquina)
        st_A = self._calculate_st_US_Tasks(A)

        # Se calcula el menor de los tiempos de fin de las tareas (C), la maquina de la tarea
        # que determinó C (machine) y el índice de la tarea en A (i_tt)
        C, machine,i_tt = self._task_ends_before(A, st_A)

        # Guardamos en B la tarea que determino C 
        # Guardamos la tarea en B, si no lo hacemos aquí y da la casualidad de que la duración de la tarea que nos da T es 0 (hay instancias en las que eso es así como la ORB07)
        # no se guardaría pues no cumpliría que st_A[i] < T, pues su tiempo de inicio sería igual que su tiempo de fin y T al tener de duración 0 
        B.append(A[i_tt])  
        
        # Se recorre el conjunto A y se añaden a B las tareas que cumplan la condición: que empleen la máquina
        # que la tarea que determinó C y puedan comenzar antes que C
        for i in range(len(A)):
            if (i_tt!=i) and (st_A[i] < C) and (self.prob.mi[A[i]] == machine):
                B.append(A[i])
        return B  

    # Método que calcula los tiempos de inicio de las tareas del conjunto A
    def _calculate_st_US_Tasks(self, A):
       st_A=[]
       for i in range(len(A)):
           task=A[i]
           # Calculamos el mínimo tiempo de inicio de las tareas sin planificar
           # Como el máximo entre: el tiempo de fin de la tarea anterior en
           # el trabajo y en la máquina
           # Calculamos el tiempo de fin de la tarea anterior en el trabajo
           if task>=self.prob.num_jobs:   
               # si no es la primera tarea del trabajo, su tiempo de inicio será 
               # el tiempo de fin de la tarea anterior en el trabajo, es decir
               # el tiempo de inicio mas la duración de la tarea anterior en el 
               # trabajo
               endBeforeJob=self.sol.st[task-self.prob.num_jobs]+self.prob.pi[task-self.prob.num_jobs];        
           else:
               # Si es la primera del trabajo será 0 
               endBeforeJob=0
           # Obtenemos el tiempo de fin de la tarea anterior en la máquina
           endBeforeMachine=self.sol.endTimeMachine[self.prob.mi[task]]
           # Guardamos el minimo tiempo de inicio de la tarea no planificada
           taskEndsTime=max(endBeforeJob,endBeforeMachine)
           # Añadimos su tiempo de fin a st_A
           st_A.append(taskEndsTime)
           
       return st_A 

    # Método que calcula el menor de los tiempos de fin de las tareas (C), la maquina de la tarea
    # que determinó C (machine) y el índice de la tarea en A (i_tt)
    def _task_ends_before(self, A, st_A):
    # Esta función calcula de las tareas sin planificar aquella que termina antes y
    # retorna su tiempo de fin T, el índice de la tarea en US y la máquina de la tarea
        C = float('inf')
        machine = -1
        i_tt = -1
        for i in range(len(A)):
            task=A[i]
            # Calculamos el tiempo de fin de la tarea task
            taskEndsTime = st_A[i] + self.prob.pi[task]

            if taskEndsTime < C:
                C = taskEndsTime
                machine=self.prob.mi[task]
                i_tt = i
        return C, machine, i_tt
   

    def _task_ends_before2(self, A, st_A):
        if len(A)>0:
            lmin=[]
            C = float('inf')
            machine = -1
            i_tt = -1
            for i in range(len(A)):
                task=A[i]
                # Calculamos el tiempo de fin de la tarea task
                taskEndsTime = st_A[i] + self.prob.pi[task]
                if taskEndsTime < C:
                    C = taskEndsTime
                    #machine=self.prob.mi[task]
                    i_tt = i
                    lmin.clear()
                    lmin.append(i_tt)
                else:
                    if taskEndsTime==C:
                        lmin.append(i_tt)         
            if len(lmin)>1:
                print(lmin)
            i_tt=random.choice(lmin)
            task=A[i_tt]
            machine=self.prob.mi[task]

            #"""
            # Determinista
            # Nos quedamos con la tarea del trabajo con menor índice
            it1=lmin[0]
            t1=A[i_tt]
            for i in range (1,len(lmin)):
                it2=lmin[i]
                t2=A[it2]
                if ((t2%self.prob.num_jobs)<(t1%self.prob.num_jobs)):
                    it1=lmin[i]
                    t1=A[it2]      
            i_tt=it1
            task=A[i_tt]
            machine=self.prob.mi[task]
            

            #"""


        return C, machine, i_tt



