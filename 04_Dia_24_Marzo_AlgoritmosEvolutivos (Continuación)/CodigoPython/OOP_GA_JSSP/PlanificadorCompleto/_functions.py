import sys # Para procesar argumentos en linea de comandos
import random # Para generar aleatorios
import matplotlib.pyplot as plt # Para pintar gráficos
import os # Para trabajar con rutas 
 
# Función que genera aleatoriamente un vector de colores de longitud 
# num_machines. Es decir, con tantos colores diferentes como máquinas
# tenga el problema a resolver
def generaMachineColors(num_machines):
    set_colors=[]
    copia=set()
    k=0
    while len(copia)!=num_machines:
        color = "#"+''.join(random.choice('0123456789ABCDEF') for j in range(6))
        set_colors.append(color)
        copia=set(set_colors)
        k=k+1
    return set_colors 


def pintaGantt(prob, sol, graphic_name):

    rutaGantts=os.getcwd()+"\\GanttImages\\"
    if not os.path.exists(rutaGantts):
         # Si  no existe la carpeta para guardar las soluciones crearla
        os.makedirs(rutaGantts)

     
    # Generamos un vector de números aleatorios con tantos números aleatorios diferentes como 
    # maquinas tengamos
    colores=generaMachineColors(prob.num_machines)

    # Declaramos el espacio de dibujo para la figura "gsnnt" y 
    # los ejes de la misma
    fig=plt.figure(graphic_name.split(".")[0])
   

    #Creamos los ejes
    a_gnt=plt.axes()

    # Establecemos los limites del Eje "Y"
    limSup_y=prob.num_jobs*15
    a_gnt.set_ylim(0, limSup_y+15)
    
    # Establecemos los limites del Eje "X" 
    a_gnt.set_xlim(0, sol.objectiveCost+round(0.1*sol.objectiveCost))
        
        
    # Establecemos etiquetas de los ejes "X" e "Y"
    a_gnt.set_xlabel('Tiempo')
    a_gnt.set_ylabel('Trabajos')
        
        
    # Calculamos las etiquetas de los tics del eje  "Y"
    # y las posiciones donde colocarlos
    l_ticks=[]
    p_ticks=[]
    p=15;
    for i in range(prob.num_jobs):
        l_ticks.append("Job "+str(i))
        p_ticks.append(p)
        p=p+15;

    # Establecemos posición de los ticks del eje "Y"
    a_gnt.set_yticks(p_ticks)
       
    # Establecemos las etiquetas de los tics del eje "Y" 
    a_gnt.set_yticklabels(l_ticks)
     
    # Activar la cuadrícula
    a_gnt.grid(color='grey', linestyle='dashed', linewidth=0.75)
        
    j=0

    # Para no mostrar en la leyenda todas las apariciones de cada máquina
    # creamos un pool de etiquetas
    lbl_pool = []
        
        
    # Para que la leyenda salga en el orden de las máquinas pintamos primero 
    # un trabajo ficticio, con las barras en color blanco y 
    # en la posición negativa de los ejes.
    for m in range(prob.num_machines):
        lbl="M"+str(m)
        lbl_pool.append(lbl)
        tarea=(0,0)
        a_gnt.broken_barh([(0,0)], (0, 0), facecolors =(colores[m]),label=''+lbl)
          
    # Pintamos las barras de las tareas de los trabajos
    for j in range(prob.num_jobs):
        i=j
        while (i<prob.num_jobs*prob.num_machines):
            tarea=(sol.st[i],prob.pi[i])
            lbl="M"+str(prob.mi[i])
            if lbl in lbl_pool:
                prefix = '_' # Esto hace que no se vea en la leyenda la máquina
            a_gnt.broken_barh([tarea], (p_ticks[j], 10), facecolors =(colores[prob.mi[i]]),label=prefix+lbl)
            i=i+prob.num_jobs     

    # Colocamos la leyenda fuera del área de dibujo
    lg= fig.legend(bbox_to_anchor=(1.05, 1.0), loc ="upper center")        

    title=graphic_name.split(".")[0]+"_coste_"+str(sol.objectiveCost)
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


