### ---------------------------------------------------------------------------
### CLASE PROBLEMA
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
    
    # Método "privado" que lee los datos del problema del fichero de intancia file_name
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
    
    # Método "privado" que muestra los datos del fichero leido tal cual aparecen
    # en el fichero. Así como los atributos vector de furaciones (pi) y 
    # vector de máquinas (mi) cargados desde el fichero
    def _print_data(self):
        print("Instancia ", self.file_name)
        print(self.num_jobs," ", self.num_machines)
        for j in range(self.num_jobs):
            k=j
            while k<(self.num_jobs*self.num_machines):
                print(self.mi[k],self.pi[k],end=" ")
                k=k+self.num_jobs
            print() 
        print(self.pi)
        print(self.mi)
