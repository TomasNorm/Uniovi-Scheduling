import random # Para generar aleatorios


### ---------------------------------------------------------------------------
### REGLAS DE PRIORIDAD IMPLEMENTADAS
### ---------------------------------------------------------------------------

# Función que elige de manera aleatoria la siguiente tarea a planificar del
# conjunto A (primeras tareas sin planificar de cada trabajo)
# Retorna la tarea a planificar  
def random_rule(A,prob):
    task=-1
    if len(A)>0:
        # Aleatoria
        task=random.choice(A)
        
        """
        # Determinista
        # Nos quedamos con la tarea del trabajo con menor índice
        task=A[0]
        for i in range (1,len(A)):
            if ((A[i]%prob.num_jobs)<(task%prob.num_jobs)):
                task=A[i]
        """
    return task

# Función que elige del conjunto A (primeras tareas sin planificar de cada trabajo) 
# la siguiente tarea a planificar aplicando la regla SPT ( Shortest Processing Time) 
# Es decir elegiría la tarea que tenga el menor tiempo de procesamiento pi
# Los empates se resuelven aleatoriamente
# Retorna la tarea a planificar  
def SPT_rule(A,prob):
    if len(A)>0:
        lsort=[]
        t_sort=prob.pi[A[0]]
        lsort.append(A[0])
        for i in range (1,len(A)):
            if prob.pi[A[i]]<t_sort:
                t_sort=prob.pi[A[i]]
                lsort.clear()
                lsort.append(A[i])
            else:
                if prob.pi[A[i]]==t_sort:
                    lsort.append(A[i]) 
        # Aleatoria
        task=random.choice(lsort)
        
        """
        # Determinista
        # Nos quedamos con la tarea del trabajo con menor índice
        task=lsort[0]
        for i in range (1,len(lsort)):
            if ((lsort[i]%prob.num_jobs)<(task%prob.num_jobs)):
                task=lsort[i]        
        """      
    return task 




# Función que elige del conjunto A (primeras tareas sin planificar de cada trabajo) 
# la siguiente tarea a planificar aplicando la regla LPT (Largest Processing Time) 
# Es decir elegiría la tarea que tenga el mayor tiempo de procesamiento pi
# Los empates se resuelven aleatoriamente
# Retorna la tarea a planificar  
def LPT_rule(A,prob):
    if len(A)>0:
        lsort=[]
        t_sort=prob.pi[A[0]]
        lsort.append(A[0])
        for i in range (1,len(A)):
            if prob.pi[A[i]]>t_sort:
                t_sort=prob.pi[A[i]]
                lsort.clear()
                lsort.append(A[i])
            else:
                if prob.pi[A[i]]==t_sort:
                    lsort.append(A[i]) 
        task=random.choice(lsort)        
    return task 



# Función que elige del conjunto A (primeras tareas sin planificar de cada trabajo) 
# la siguiente tarea a planificar aplicando la regla MWR (most work remaining): 
# Es decir elegiría la tarea del trabajo con mayor tiempo de
# procesamiento pendiente
# Retorna la tarea a planificar  
def MWR_rule(A,prob):
    #print("US:",US)
    if len(A)>0:
        lsort=[]
        aux_wr=0 # 
        for i in range(len(A)):
            wr=0
            #print("Tarea US:",US[i])
            # Calculamos el tiempo de procesamiento en el trabajo 
            # tras US[i]
            j=A[i]+prob.num_jobs
            while j<prob.num_jobs*prob.num_machines:
                wr=wr+prob.pi[j]
                j=j+prob.num_jobs
            #print("tareaUS:",US[i],"wp=",wr)
            if i==0:
                aux_wr=wr
                lsort.append(A[i])
            else:
                if wr>aux_wr:
                    aux_wr=wr
                    lsort.clear()
                    lsort.append(A[i])
                else:
                    if wr==aux_wr:
                        lsort.append(A[i])
        #print("lsort",lsort)
        task=random.choice(lsort)
        #print("task",task)
    return task 


# Función que elige del conjunto A (primeras tareas sin planificar de cada trabajo) 
# la siguiente tarea a planificar aplicando la regla LWR (less work remaining): 
# Es decir elegiría la tarea del trabajo con menor tiempo de
# procesamiento pendiente
# Retorna la tarea a planificar  
def LWR_rule(A,prob):
    #print("US:",US)
    if len(A)>0:
        lsort=[]
        aux_wr=0 # 
        for i in range(len(A)):
            wr=0
            #print("Tarea US:",US[i])
            # Calculamos el tiempo de procesamiento en el trabajo 
            # tras US[i]
            j=A[i]+prob.num_jobs
            while j<prob.num_jobs*prob.num_machines:
                wr=wr+prob.pi[j]
                j=j+prob.num_jobs
            #print("tareaUS:",US[i],"wp=",wr)
            if i==0:
                aux_wr=wr
                lsort.append(A[i])
            else:
                if wr<aux_wr:
                    aux_wr=wr
                    lsort.clear()
                    lsort.append(A[i])
                else:
                    if wr==aux_wr:
                        lsort.append(A[i])
        # Aleatoria
        task=random.choice(lsort)


        
    return task 


# Función que elige del conjunto A (primeras tareas sin planificar de cada trabajo) 
# la siguiente tarea a planificar aplicando la regla MOR (most operations remaining): 
# Es decir elegiría la tarea del trabajo en el que queden más tareas pendientes
# Retorna la tarea a planificar  
def MOR_rule(A,prob):
    #print("US:",US)
    if len(A)>0:
        lsort=[]
        aux_nt=0 # 
        for i in range(len(A)):
            nt=0
            #print("Tarea US:",US[i])
            # Calculamos las tareas sin procesar en el trabajo tras US[i]
            j=A[i]+prob.num_jobs
            while j<prob.num_jobs*prob.num_machines:
                nt=nt+1
                j=j+prob.num_jobs
            #print("tareaUS:",US[i],"nt=",nt)
            if i==0:
                aux_nt=nt
                lsort.append(A[i])
            else:
                if nt>aux_nt:
                    aux_nt=nt
                    lsort.clear()
                    lsort.append(A[i])
                else:
                    if nt==aux_nt:
                        lsort.append(A[i])
        #print("lsort",lsort)
        task=random.choice(lsort)
        #print("task",task)
    return task

# Función que elige del conjunto A (primeras tareas sin planificar de cada trabajo) 
# la siguiente tarea a planificar aplicando la regla LOR (less operations remaining): 
# Es decir elegiría la tarea del trabajo en el que queden más tareas pendientes
# Retorna la tarea a planificar  
def LOR_rule(A,prob):
    #print("US:",US)
    if len(A)>0:
        lsort=[]
        aux_nt=0 # 
        for i in range(len(A)):
            nt=0
            #print("Tarea US:",US[i])
            # Calculamos las tareas sin procesar en el trabajo tras US[i]
            j=A[i]+prob.num_jobs
            while j<prob.num_jobs*prob.num_machines:
                nt=nt+1
                j=j+prob.num_jobs
            #print("tareaUS:",US[i],"nt=",nt)
            if i==0:
                aux_nt=nt
                lsort.append(A[i])
            else:
                if nt<aux_nt:
                    aux_nt=nt
                    lsort.clear()
                    lsort.append(A[i])
                else:
                    if nt==aux_nt:
                        lsort.append(A[i])
        #print("lsort",lsort)
        task=random.choice(lsort)
        #print("task",task)
    return task

"""

# Función que elige del conjunto US (primeras tareas sin planificar de cada trabajo) 
# la siguiente tarea a planificar aplicando la regla LOR (less operations remaining): 
# Es decir elegiría la tarea del trabajo en el que queden menos tareas pendientes
# Retorna la tarea a planificar  
def LOR_rule(US,prob):
    if len(US)>0:
       
    return task 
"""

# Necesitamos proporcionarle el genotipo, pero no puede ser por argumento porque 
# estaríamos violando el formato de argumentos del resto de reglas.
# así que hacemos un campo estático (de contexto del genotipo) que utilice el
# método estático apply() que realmente será la regla "GA"
class GA_rule:
    genotipo = None

    @staticmethod
    def apply(A,prob):
        task = None
        # conversion RP a NRP
        tasks_job = [0] * prob.num_jobs
        for id_job in GA_rule.genotipo:
            id_task = id_job + prob.num_jobs * tasks_job[id_job]
            tasks_job[id_job] += 1
            # buscamos la tarea del genotipo en el cjto a
            if id_task in A:
                task = id_task
                break;
        return task

### ---------------------------------------------------------------------------
### FACTORIA DE REGLAS 
### ---------------------------------------------------------------------------

# Reglas disponibles
switchRule = {"RR" : random_rule, "SPT": SPT_rule, "LPT":LPT_rule, "MWR":MWR_rule, "LWR":LWR_rule, "MOR":MOR_rule, "LOR":LOR_rule, "GA":GA_rule.apply}

def rule_factory(name):
    rule = switchRule.get(name)
    if (rule == None):
        raise Exception("\"" + name + "\"", "no es argumento válido, el segundo argumento ha de ser uno de estos: " + _rules_to_string())
        #print("\"" + name + "\"", "no es argumento válido, ")
        #print("el segundo argumento ha de ser uno de estos: " + _rules_to_string())

    return rule

def _rules_to_string():
    text = ""
    for i, k in enumerate(switchRule):
        text += k + " "

    return text




"""
# tests
print(rule_factory("RR"))
print(rule_factory("RR2"))
"""