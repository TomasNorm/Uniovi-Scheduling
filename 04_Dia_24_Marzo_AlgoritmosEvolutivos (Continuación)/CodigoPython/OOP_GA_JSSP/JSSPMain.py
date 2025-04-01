import random # Para generar aleatorios
import numpy as np # para estadísticos del experimento
from GeneticAlgorithm import * # Nuestro algoritmo genético
import matplotlib.pyplot as plt # Para pintar soluciones y/o evolución del GA
from JSSPConfiguration import * # Configuración del problema TSP

#Dibuja la evolucion del fitness
def DibujarResultadosJSSP(problema, mejor_solucion, mejor_fitness, evolucion=[]):
  
   #plt.figure(figsize=(5,5))
   plt.figure(figsize=(11,5))


   
   paint_gantt(problema, plt, mejor_solucion)
   """
   x=[1,2]
   y=[1,2]
 
   plt.subplot(121)
   plt.plot(x, y, 'bo', markersize=4.0)
   a_scale = float(max(x))/float(100)
   plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width = a_scale, color = 'r', length_includes_head=True)
   for i in range(0,len(x)-1):
      plt.arrow(x[i], y[i], (x[i+1] - x[i]), (y[i+1] - y[i]), head_width = a_scale, color = 'r', length_includes_head=True)      
   plt.xlim(0,max(x)*1.1)
   plt.ylim(0,max(y)*1.1)
   plt.xlabel("x")
   plt.ylabel("y")
   plt.title(f"Problema {problema.name} ({mejor_fitness:.2f})")"""
   #plt.subplot(111)
   plt.subplot(122)
   plt.plot(evolucion)
   plt.xlabel("Iteración")
   plt.ylabel("Fitness")
   plt.title(f"Evolución (Mejor fitness: {mejor_fitness:.2f})")
   plt.show()

# Método que pinta el diagrama de Gantt de la solución y lo guarda en
    # una gráfica de formato "jpg" de nombre "nombre_grafica"
def paint_gantt(prob, pl, fenotipo):
    st = fenotipo["st"]
   
    # Generamos un vector de números aleatorios con tantos números aleatorios diferentes como 
    # maquinas tengamos
    colores = generate_machine_colors(prob.num_machines)

    #Creamos los ejes
    a_gnt = pl.subplot(121)

    # Establecemos los limites del Eje "Y"
    limSup_y = prob.num_jobs * 15
    a_gnt.set_ylim(0, limSup_y + 15)

    # Establecemos los limites del Eje "X" 
    ###a_gnt.set_xlim(0, max(self.endTimeMachine)+round(0.05*max(self.endTimeMachine))) # El límite del eje x es el máximo tiempo de fin de entre todas las máquinas más un 5% más


    # Establecemos etiquetas de los ejes "X" e "Y"
    a_gnt.set_xlabel('Tiempo')
    a_gnt.set_ylabel('Trabajos')


    # Calculamos las etiquetas de los tics del eje  "Y"
    # y las posiciones donde colocarlos
    l_ticks = []
    p_ticks = []
    p = 15;
    for i in range(prob.num_jobs):
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
    for m in range(prob.num_machines):
        lbl = "M" + str(m)
        lbl_pool.append(lbl)
        tarea = (0,0)
        a_gnt.broken_barh([(0,0)], (0, 0), facecolors =(colores[m]),label=''+lbl)
        
    # Pintamos las barras de las tareas de los trabajos
    for j in range(prob.num_jobs):
        i = j
        while (i < prob.num_jobs * prob.num_machines):
            tarea = (st[i], prob.pi[i])
            lbl = "M" + str(prob.mi[i])
            if lbl in lbl_pool:
                prefix = '_' # Esto hace que no se vea en la leyenda la máquina
            # pintamos la barra    
            a_gnt.broken_barh([tarea], (p_ticks[j], 10), facecolors =(colores[prob.mi[i]]),label=prefix+lbl)
            # colocamos una etiqueta con el identificador de la máquina (arriba) y el identificador de máquina (debajo), para poder distinguir las tareas y las máquinas cuando el color sea muy parecido
            a_gnt.text(tarea[0]+0.5, p_ticks[j]+8, str(i),fontsize=5)
            a_gnt.text(tarea[0]+0.5, p_ticks[j]+2, str(prob.mi[i]),fontsize=5)
            i = i + prob.num_jobs     

    # Colocamos la leyenda fuera del área de dibujo
    ###lg = fig.legend(bbox_to_anchor=(1.05, 1.0), loc ="upper center")        

    ###title = graphic_name.split(".")[0] + "_coste_" + str(self.objectiveCost)
    ###fig.suptitle(title)
            
     
    # Método "privado" que convierte una lista a un string"
def _list_to_string(list):
        cadena=""
        for i in range(len(list)):
            cadena = cadena+str(list[i])+" "
        return cadena

    # Método "privado" que genera aleatoriamente un vector de colores de longitud 
    # num_machines. Es decir, con tantos colores diferentes como máquinas
    # tenga el problema a resolver
def generate_machine_colors(num_machines):
        set_colors=[]
        copia=set()
        k=0
        while len(copia)!=num_machines:
            color = "#" + ''.join(random.choice('0123456789ABCDEF') for j in range(6))
            set_colors.append(color)
            copia = set(set_colors)
            k = k + 1
        return set_colors 


def experiment(instancia = "la16.txt", total_runs = 30, traza = False, pob = 100, gens = 100):
    cfg = JSSPConfiguration(instancia)
    cfg.n_poblacion = pob
    cfg.max_gen = gens
    ga = GeneticAlgorithm(cfg, traza = traza)
    mejores = []
    tiempos = []
    
    for i in range(total_runs):
        print(f"Run {i+1}")#, end="")
        mejor_solucion, mejor_fitness, evolucion = ga.run()
        mejores.append(mejor_fitness)
        print(f" Tiempo: {Tiempo.total()} segs")
        tiempos.append(Tiempo.total())
        # Mostrar resultados
        #print('¡Ejecucion finalizada! El tiempo de ejecución fue: %s segundos' % Tiempo.total())
        #print('La mejor solucion y su mejor fitness:')
        print('f(%s) = %f' % (mejor_solucion, mejor_fitness))
        if traza:
            DibujarResultadosJSSP(cfg.problem.coordenadas,mejor_solucion,mejor_fitness,evolucion)

    print(mejores)
    print(f'Best sol: {np.min(mejores):.2f}')
    print(f'Average sol: {np.mean(mejores):.2f}')
    print(f'StdDev sol: {np.std(mejores):.2f}')
    print(f'Average time: {np.mean(tiempos):.2f}')
    print(f'StdDev time: {np.std(tiempos):.2f}')

    return [pob, gens, np.min(mejores), np.mean(mejores), np.std(mejores), np.mean(tiempos), np.std(tiempos), mejores]

def run_GA(file_name = None):
    cfg = JSSPConfiguration(file_name)
    print(cfg)
    ga = GeneticAlgorithm(cfg)
    #print(dir(ga))
    mejor_solucion, mejor_fitness, evolucion = ga.run()
    # Mostrar resultados
    print('¡Ejecucion finalizada! El tiempo de ejecución fue: %s segundos' % Tiempo.total())
    print('La mejor solucion y su mejor fitness:')
    print('f(%s) = %f' % (mejor_solucion, mejor_fitness))
    #DibujarResultados(cfg.problem.coordenadas,mejor_solucion,mejor_fitness,evolucion)
    DibujarResultadosJSSP(cfg.problem, mejor_solucion, mejor_fitness,evolucion)
    


### ---------------------------------------------------------------------------
### PROGRAMA PRINCIPAL
### ---------------------------------------------------------------------------
#run_GA("./la16.txt")

def muestra_resultados(fichero, i,resultados):
    for [a,b,c,d,e,f,g,h] in resultados:
        cadena = f"{i} {a:.2f} {b:.2f} {c:.2f} {d:.2f} {e:.2f} {f:.2f} {g:.2f}"
        for v in h:
            cadena = cadena + f" {v:.2f}"            
        
        show(fichero, cadena)

def show(fichero,s):
    print(s)
    fichero.write(s+"\n")

def main():
    runs = 10

    for i in [ "la01.txt", "la02.txt", "la03.txt", "la04.txt", "la05.txt", "la06.txt", "la07.txt", "la08.txt", "la09.txt", "la10.txt", "la11.txt", "la12.txt", "la13.txt", "la14.txt", "la15.txt", "la16.txt", "la17.txt", "la18.txt", "la19.txt", "la20.txt"]:
        fichero = open("salida/"+i,"w")
        
        show(fichero, "Resultados:runsx100x100")
        resultados = []
        resultados.append(experiment("instances/"+i,runs, pob=100, gens=100))
        muestra_resultados(fichero, i,resultados)
        

        show(fichero, "Resultados:runsx200x400")
        resultados = []
        resultados.append(experiment("instances/"+i,runs, pob=200, gens=400))
        muestra_resultados(fichero, i,resultados)
        
        show(fichero, "Resultados:runsx80000x1")
        resultados = []
        resultados.append(experiment("instances/"+i,runs, pob=200*400, gens=1))
        muestra_resultados(fichero, i,resultados)
        '''show(fichero, "Resultados:runsx100x[100-500]")
        resultados.append(experiment(i,runs, pob=100, gens=100))
        resultados.append(experiment(i,runs, pob=100, gens=200))
        resultados.append(experiment(i,runs, pob=100, gens=300))
        resultados.append(experiment(i,runs, pob=100, gens=400))
        resultados.append(experiment(i,runs, pob=100, gens=500))
        muestra_resultados(fichero, i,resultados)
        
        resultados = []
        show(fichero, "Resultados:runsx[10000-50000]x1")
        resultados.append(experiment(i,runs, pob=10000, gens=1))
        resultados.append(experiment(i,runs, pob=20000, gens=1))
        resultados.append(experiment(i,runs, pob=30000, gens=1))
        resultados.append(experiment(i,runs, pob=40000, gens=1))
        resultados.append(experiment(i,runs, pob=50000, gens=1))
        muestra_resultados(fichero, i,resultados)

        resultados = []
        show(fichero, "Resultados:runsx200x[100-500]")
        resultados.append(experiment(i,runs, pob=200, gens=100))
        resultados.append(experiment(i,runs, pob=200, gens=200))
        resultados.append(experiment(i,runs, pob=200, gens=300))
        resultados.append(experiment(i,runs, pob=200, gens=400))
        resultados.append(experiment(i,runs, pob=200, gens=500))
        muestra_resultados(fichero, i, resultados)'''
        fichero.close()


#main()

#print (resultados)

run_GA("la16.txt")

