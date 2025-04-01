

### ---------------------------------------------------------------------------
### FUNCIONES OBJETIVO CONSIDERADAS
### ---------------------------------------------------------------------------

# Función que calcula y retorna el Makespan, 
# tiempo de fin de la tarea que termina más tarde en la planificación solución
def makespan(prob,sol):
    return max(sol.endTimeMachine) 

# Función que calcula y retorna el Total Flow Time (Tiempo de flujo total), 
# suma de los tiempos de fin de todos los trabajos
def total_flow_time(prob,sol):
    tft=0
    last_task_job=prob.num_jobs*prob.num_machines-1
    for j in range(prob.num_jobs):        
        tft=tft+sol.st[last_task_job]+prob.pi[last_task_job]
        last_task_job=last_task_job-1
    return tft


### ---------------------------------------------------------------------------
### FACTORIA DE FUNCIONES OBJETIVO
### ---------------------------------------------------------------------------

# Funciones objetivo disponibles
switchOF = {"MK" : makespan, "TFT": total_flow_time}

def objective_fuction_factory(name):
    function = switchOF.get(name)
    if (function == None):
        print("\"" + function + "\"", "no es argumento válido, ")
        print("el segundo argumento ha de ser uno de estos: " + _functions_to_string())

    return function

def _functions_to_string():
    text = ""
    for i, k in enumerate(switchOF):
        text += k + " "

    return text

