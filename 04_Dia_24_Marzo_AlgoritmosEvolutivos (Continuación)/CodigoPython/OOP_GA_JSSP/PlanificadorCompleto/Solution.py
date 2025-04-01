import random # Para generar aleatorios
import os # Para trabajar con rutas 
import matplotlib.pyplot as plt # Para pintar gráficos


### ---------------------------------------------------------------------------
### CLASE SOLUCIÓN
### ---------------------------------------------------------------------------
# Clase que contiene la solución al problema
class Solution:
    
    # Constructor de la clase Solution, inicializa los atributos de la clase
    # st: Vector con los tiempos de Inicio 
    # objectiveCost: Coste de la solución
    # endTimeMachine: Vector con los tiempos de fin de las máquinas
    # scheduled_tasks: vector de booleanos donde indicar si una tarea 
    #                  está (True) o no (False)  planificada
    def __init__(self, problem):
        self.num_jobs = problem.num_jobs
        self.num_machines = problem.num_machines
        self.prob = problem
        self.init_solution()
        """
        self.st=[0] * prob.num_jobs*prob.num_machines
        self.objectiveCost=0
        self.endTimeMachine=[0] * prob.num_machines
        """
    # Método que inicializa los atributos de la solución:
    # tiempos de inicio de las tareas (st), incialmente todas a 0
    # coste de la función objetivo (objectiveCost), inicialmente a 0
    # estructura auxiliar donde se almacenan los tiempos de fin de las máquinas (endTimeMachine)
    #     inicialmente todas a cero pues no hay ninguna tarea planificada
    # vector con las tareas del problema que están planificadas, inicialmente todas a false 
    def init_solution(self):
        self.st = [0] * self.num_jobs * self.num_machines
        self.objectiveCost = 0
        self.endTimeMachine = [0] * self.num_machines
        self.scheduled_tasks=[False]* self.prob.num_jobs*self.prob.num_machines
    
        
    # Método que muestra los atributos que conforman la solución
    # Vector de tiempos de inicio de las tareas y coste de la solución
    def print_solution(self):
        print(self.st)
        print(self.objectiveCost)
    
    # Método que guarda la solución del problema en el fichero file_name
    def save_solution(self, file_name):
        rutaSol = os.getcwd()+"\\Solutions\\"
        if not os.path.exists(rutaSol):
             # Si  no existe la carpeta para guardar las soluciones crearla
            os.makedirs(rutaSol)
        name = rutaSol + file_name.split(".")[0] + "_coste_" + str(self.objectiveCost)
        file = open(name+".txt","w")
        c = str(self.num_jobs)+" "+str(self.num_machines)
        file.write(c + "\n")
        c = str(self._list_to_string(self.prob.pi))
        file.write(c + "\n")
        c = str(self._list_to_string(self.prob.mi))
        file.write(c + "\n")
        c = str(self._list_to_string(self.st))
        file.write(c + "\n")
        file.write(str(self.objectiveCost) + " ")
        file.close()
   
   
    # Método que pinta el diagrama de Gantt de la solución y lo guarda en
    # una gráfica de formato "jpg" de nombre "nombre_grafica"
    def paint_gantt(self, graphic_name):
        rutaGantts = os.getcwd() + "\\GanttImages\\"
        if not os.path.exists(rutaGantts):
             # Si  no existe la carpeta para guardar las soluciones crearla
            os.makedirs(rutaGantts)
        # Generamos un vector de números aleatorios con tantos números aleatorios diferentes como 
        # maquinas tengamos
        colores = self._generate_machine_colors(self.prob.num_machines)

        # Declaramos el espacio de dibujo para la figura "gsnnt" y 
        # los ejes de la misma
        fig = plt.figure(graphic_name.split(".")[0])
       
    
         #Creamos los ejes
        a_gnt = plt.axes()

        # Establecemos los limites del Eje "Y"
        limSup_y = self.prob.num_jobs * 15
        a_gnt.set_ylim(0, limSup_y + 15)
    
        # Establecemos los limites del Eje "X" 
        a_gnt.set_xlim(0, max(self.endTimeMachine)+round(0.05*max(self.endTimeMachine))) # El límite del eje x es el máximo tiempo de fin de entre todas las máquinas más un 5% más
        
        
        # Establecemos etiquetas de los ejes "X" e "Y"
        a_gnt.set_xlabel('Tiempo')
        a_gnt.set_ylabel('Trabajos')
        
        
        # Calculamos las etiquetas de los tics del eje  "Y"
        # y las posiciones donde colocarlos
        l_ticks = []
        p_ticks = []
        p = 15;
        for i in range(self.prob.num_jobs):
            l_ticks.append("Job " + str(i))
            p_ticks.append(p)
            p = p + 15;

        #Establecemos posición de los ticks del eje "Y"
        a_gnt.set_yticks(p_ticks)
       
        # Establecemos las etiquetas de los tics del eje "Y" 
        a_gnt.set_yticklabels(l_ticks)
     
        # Activar la cuadrícula
        a_gnt.grid(color='grey', linestyle='dashed', linewidth=0.75)
        
        j = 0

        # Para no mostrar en la leyenda todas las apariciones de cada máquina
        # creamos un pool de etiquetas
        lbl_pool = []
        
        
        # Para que la leyenda salga en el orden de las máquinas pintamos primero 
        # un trabajo ficticio, con las barras en color blanco y 
        # en la posición negativa de los ejes.
        for m in range(self.prob.num_machines):
            lbl = "M" + str(m)
            lbl_pool.append(lbl)
            tarea = (0,0)
            a_gnt.broken_barh([(0,0)], (0, 0), facecolors =(colores[m]),label=''+lbl)
          
        # Pintamos las barras de las tareas de los trabajos
        for j in range(self.prob.num_jobs):
            i = j
            while (i < self.prob.num_jobs * self.prob.num_machines):
                tarea = (self.st[i], self.prob.pi[i])
                lbl = "M" + str(self.prob.mi[i])
                if lbl in lbl_pool:
                    prefix = '_' # Esto hace que no se vea en la leyenda la máquina
                # pintamos la barra    
                a_gnt.broken_barh([tarea], (p_ticks[j], 10), facecolors =(colores[self.prob.mi[i]]),label=prefix+lbl)
                # colocamos una etiqueta con el identificador de la máquina (arriba) y el identificador de máquina (debajo), para poder distinguir las tareas y las máquinas cuando el color sea muy parecido
                a_gnt.text(tarea[0]+0.5, p_ticks[j]+8, str(i),fontsize=5)
                a_gnt.text(tarea[0]+0.5, p_ticks[j]+2, str(self.prob.mi[i]),fontsize=5)
                i = i + self.prob.num_jobs     

        # Colocamos la leyenda fuera del área de dibujo
        lg = fig.legend(bbox_to_anchor=(1.05, 1.0), loc ="upper center")        

        title = graphic_name.split(".")[0] + "_coste_" + str(self.objectiveCost)
        fig.suptitle(title)
                
   
        # Guardamos el gráfico de gantt en formato JPG
        fig.savefig(rutaGantts+title+".jpg", 
            dpi=300, # Resolución 300 inch (pulgadas), a mayor resolución mayor tamaño de imagen guardada
            format='jpg', # Formato en el que se guarda la imagen
            bbox_extra_artists=(lg,), # Lista de elementos adidionales a considerar al renderizar la imagen, así no se corta la leyenda
            bbox_inches='tight') # Cuadro delimitador en pulgadas: solo se guarda la parte dada de la figura. 
        
        """
        fig.show()  # Descomentar para mostrarla en ejecución
        #fig.canvas.draw()
        plt.pause(0.8) # Da 0.8 segundos para visualizar la imagen  
        """
    
        fig.clf()

            
    # Método "privado" que convierte una lista a un string"
    def _list_to_string(self, list):
        cadena=""
        for i in range(len(list)):
            cadena = cadena+str(list[i])+" "
        return cadena

    # Método "privado" que genera aleatoriamente un vector de colores de longitud 
    # num_machines. Es decir, con tantos colores diferentes como máquinas
    # tenga el problema a resolver
    def _generate_machine_colors(self, num_machines):
        set_colors=[]
        copia=set()
        k=0
        while len(copia)!=num_machines:
            color = "#" + ''.join(random.choice('0123456789ABCDEF') for j in range(6))
            set_colors.append(color)
            copia = set(set_colors)
            k = k + 1
        return set_colors 
    


