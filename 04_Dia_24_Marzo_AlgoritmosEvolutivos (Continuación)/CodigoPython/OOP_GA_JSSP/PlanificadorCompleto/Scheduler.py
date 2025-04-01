import sys # Para procesar argumentos en linea de comandos
import random # Para generar aleatorios
import matplotlib.pyplot as plt # Para pintar gráficos
import os # Para trabajar con rutas 
 
from Problem import *
from Solution import *
from SchedulerGenerator import *
from rules import *


### ---------------------------------------------------------------------------
### FUNCION COMPROBACIÓN ARGUMENTOS EN LINEA DE COMANDOS
### ---------------------------------------------------------------------------

# Función que comprueba que los argumentos que se pasan en línea de comandos y
# son necesarios para ejecutar el planificador son correctos.
def check_args(vArgs):
    error = False
    #file_name=rule=objectiveF=""
    num_args = len(vArgs)-1 # sin contar el nombre del script

    # argumentos por defecto: instancia ft03, la regla Random (RR), con objetivo el Makespan (MK), con el planificador (_basic)
    file_name = 'ft03.txt'  
    rule="RR"
    objectiveF="MK"

    if (num_args > 3): # Numero de argumentos mayor que 3
        msg = "Error. Ha pasado " + str(num_args) + " argumentos\n" +\
        "El programa debe recibir tres argumenos: \n" +\
        "Primer argumento fichero con la instancia\n" +\
        "Segundo argumento nombre de la regla (RR, SPT, LPT, MWR, LWR, MOR, LOR) | all\n" +\
        "Tercer argumento nombre de la funcion objetivo (MK, TFT)\n" +\
        "Ejemplo: python " + sys.argv[0] + " datos.txt RR MK _basic"
         #"Ejemplo: python schedule_basico_G&T_V11.py datos.txt RR MK"
        raise Exception(msg)
       
    else:
        if (num_args >= 1): # Se ejecuta con el archivo que se le pase
            file_name = sys.argv[1]
        if (num_args >= 2): # y se utiliza ademas la regla especificada            
            rule = sys.argv[2]
        if (num_args == 3): # y se utiliza la funcion objetivo especificada
            objectiveF = sys.argv[3] 

                                
    return file_name, rule, objectiveF,  error

    
### ---------------------------------------------------------------------------
### PROGRAMA PRINCIPAL
### ---------------------------------------------------------------------------


# Comprobamos que los argumentos son correctos
 

try:
    
    if len(sys.argv) > 1:        

                                   
        # LINEA DE COMANDOS 
        file_name, rule, objectiveF, error = check_args(sys.argv)

        if not error:
            # "Scheduler.py" ft03.txt RR MK
            sch = SchedulerGenerator(file_name, rule, objectiveF)
            

            
            coste_basico = sch.execute_basic_scheduler()
            sch.save_solution()
            sch.paint_gannt_schedule()
                   
           
            #""" # Descomentar cuando tenga simplementado el G&T
            coste_gyt = sch.execute_GyT()     
            sch.save_solution()  # Descomentar para guardar la solución
            sch.paint_gannt_schedule() # Descomentar para guardar la imagen del Gannt con la solución
            #"""

            #print(sch.configuration, " coste ", coste_basico) # Comentar cuando tengas implementado el G&T
            print(sch.configuration, " coste ", coste_basico, coste_gyt) # Descomentar cuando tenga simplementado el G&T

    else:
            
        # EJECUCIÓN POR PROGRAMA
        print("Carpeta actual:", os.getcwd());

        # Instancia del problema por defecto 
        instance = os.getcwd() + "\\Instances\\"+"ft03.txt"


        file_name = instance
        print(file_name)
        
            
              
        # MAKESPAN
        sch = SchedulerGenerator(file_name,"RR","MK")
        coste_MK = sch.execute_basic_scheduler()
        #sch.save_solution()  # Descomentar para guardar la solución
        #sch.paint_gannt_schedule()  # Descomentar para guardar la solución

        """ # Descomentar cuando tenga simplementado el G&T   
        coste_MK_gt = sch.execute_GyT()
        #sch.save_solution() # Descomentar para guardar la solución
        #sch.paint_gannt_schedule() # Descomentar para guardar la imagen del Gannt con la solución
        """

        print("MAKESPAN")
        print("Basico MK", coste_MK) # Comentar cuando tengas implementado el G&T
        #print("Basico ", coste_MK,"G&T ",coste_MK_gt)  # Descomentar cuando tenga simplementado el G&T
    

        
        # TOTAL FLOW TIME
        sch = SchedulerGenerator(file_name,"RR","TFT")
        coste_TFT = sch.execute_basic_scheduler()
        #sch.save_solution()
        #sch.paint_gannt_schedule()

        """  # Descomentar cuando tenga simplementado el G&T 
        coste_TFT_gt = sch.execute_GyT()
        #sch.save_solution()
        #sch.paint_gannt_schedule()
        """
        
        print("TOTAL FLOW TIME")
        print("Basico TFT", coste_TFT) # Comentar cuando tengas implementado el G&T
        #print("Basico ", coste_TFT,"G&T ",coste_TFT_gt) # Descomentar cuando tenga simplementado el G&T
        
   
               
except (FileNotFoundError, ValueError) as e:
    print("Problemas con el fichero")
    print(str(e))
except (Exception) as e: # posible error en argumentos
    print(str(e))
        
  
