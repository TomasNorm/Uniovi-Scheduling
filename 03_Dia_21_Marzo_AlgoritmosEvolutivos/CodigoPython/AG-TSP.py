# Algoritmo Genético con permutaciones aplicado al problema TSP
from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
import matplotlib.pyplot as plt
import time
 
# Función objetivo
def TSP(x):
 suma = sum(matriz[x[i]][x[i+1]] for i in range(len(x)-1))
 suma = suma + matriz[x[len(x)-1]][x[0]]
 return suma

# Función para leer las coordenadas de un fichero
def leer_fichero_TSP(nombre, coordenadas):
    f = open(nombre,"r")
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


# Función para crear la matriz de distancias, a partir de las coordenadas
def crear_matriz_distancias(coord, matriz):
   for i in range(len(coord)):
      linea=[]
      for j in range(len(coord)):
         dist=((coord[i][0]-coord[j][0])**2 + (coord[i][1]-coord[j][1])**2)**(0.5)
         linea.append(dist)
      matriz.append(linea)


# Generar una solución inicial
def crear_solucion_inicial():
   if utilizar_vecino_mas_cercano == False:
      ciudades=[]
      for num in range(len(matriz)):
         ciudades.append(num)
         solucion = permutation(ciudades)
   else:
      solucion = vecino_mas_cercano(cuantos_vecinos_mas_cercanos)
   return solucion


# Función para crear una solución desde 0, utilizando el heurístico del vecino más cercano aleatorizado
def vecino_mas_cercano(num_candidatos):
   solucion=[]
   ciudadesporvisitar=[]
   for i in range(len(matriz)):
      ciudadesporvisitar.append(i)
   # La primera ciudad es aleatoria
   ciudadelegida=randint(len(matriz))
   solucion.append(ciudadelegida)
   ciudadesporvisitar.remove(ciudadelegida)
   # Para el resto de ciudades, elegidos una ciudad al azar de entre las "num_candidatos" ciudades aun no visitadas más cercanas
   while len(solucion)<len(matriz):
      # Para ello, elegimos las "num_candidatos" primeras ciudades que estén en "ciudadesporvisitar"
      candidatas=[]
      contador=0
      while len(candidatas)<num_candidatos and len(candidatas)<len(ciudadesporvisitar):
         candidatas.append(ciudadesporvisitar[contador])
         contador+=1
      # Miramos cual es la más lejana de ellas
      indicemaslejana=0
      for i in range(1,len(candidatas)):
         if matriz[solucion[len(solucion)-1]][candidatas[i]]>matriz[solucion[len(solucion)-1]][candidatas[indicemaslejana]]:
            indicemaslejana=i
      # Y para cada una de las demás, comprobamos si es más cercana que la más lejana de entre las que ya teníamos
      while contador<len(ciudadesporvisitar):
         if matriz[solucion[len(solucion)-1]][ciudadesporvisitar[contador]]<matriz[solucion[len(solucion)-1]][candidatas[indicemaslejana]]:
            candidatas[indicemaslejana]=ciudadesporvisitar[contador]
            # Y si es asi, actualizamos la mas lejana
            indicemaslejana=0
            for i in range(1,len(candidatas)):
               if matriz[solucion[len(solucion)-1]][candidatas[i]]>matriz[solucion[len(solucion)-1]][candidatas[indicemaslejana]]:
                  indicemaslejana=i
         contador+=1
      # Para acabar, elegimos una candidata al azar, la añadimos a la solución parcial, y la quitamos de ciudadesporvisitar
      elegida=randint(0,len(candidatas))
      solucion.append(candidatas[elegida])
      ciudadesporvisitar.remove(candidatas[elegida])
   # Y finalmente devolvemos la solucion completa
   return solucion


# Para saber si un cromosoma es mejor que otro
def esMejorQue(a, b):
   if maximizar==True:
      return a>b
   else:
      return a<b
   

# Selección por torneo
def seleccion(poblacion, fitness, tam_torneo):
 # Elegimos un individuo aleatorio
 elegido = randint(len(poblacion))
 for i in randint(0, len(poblacion), tam_torneo-1):
    # Comprobamos si es mejor (es decir, hacemos un torneo)
    if esMejorQue(fitness[i],fitness[elegido]):
        elegido = i
 return poblacion[elegido]


# Cruzamos dos padres para crear dos hijos (Order Crossover)
def cruce(p1, p2, p_cruce):
 # Los hijos, por defecto, son copias de los padres
 c1, c2 = p1.copy(), p2.copy()
 # Comprobamos si hay que cruzarlos (probabilidad de cruce)
 if rand() < p_cruce:
    # Seleccionamos dos puntos aleatorios
    puntomin = randint(0, len(p1))
    puntomax = randint(0, len(p1))
    while puntomin==puntomax:
       puntomax = randint(0, len(p1))
    if puntomin>puntomax:
       puntomin, puntomax = puntomax, puntomin
    punterop1=0
    punterop2=0
    # Y construimos los hijos según el operador Order Crossover
    for i in range(len(p1)):
       if i<puntomin or i>puntomax:
          while p2[punterop2] in c1[puntomin:puntomax+1]:
             punterop2+=1
          c1[i]=p2[punterop2]
          punterop2+=1
          while p1[punterop1] in c2[puntomin:puntomax+1]:
             punterop1+=1
          c2[i]=p1[punterop1]
          punterop1+=1
 return [c1, c2]


# Operador de mutación (intercambio)
def mutacion(cromosoma, p_mut):
 if rand() < p_mut:
    punto1 = randint(0, len(cromosoma))
    punto2 = randint(0, len(cromosoma))
    cromosoma[punto1],cromosoma[punto2] = (cromosoma[punto2], cromosoma[punto1])


# Para ver cuál es el fitness mejor, medio y peor de la población
def MejorMediaPeor(fitness):
   mejor_cromosoma, mejor_fitness, peor_fitness = 0, fitness[0], fitness[0]
   media_fitness=0
   for i in range(n_poblacion):
       media_fitness+=fitness[i]
       if esMejorQue(fitness[i],mejor_fitness):
         mejor_cromosoma, mejor_fitness = i, fitness[i]
       if esMejorQue(peor_fitness,fitness[i]):
         peor_fitness = fitness[i]           
   media_fitness=media_fitness/n_poblacion
   return [mejor_cromosoma,mejor_fitness,media_fitness,peor_fitness]


# Algoritmo Genético
def algoritmo_genetico(objetivo, n_bits, max_gen, n_poblacion, p_cruce, p_mut):
 gen=0
 evolucion=[]
 # Crear población inicial
 poblacion=[crear_solucion_inicial() for _ in range(n_poblacion)]
 # Evaluar la población
 fitness = [objetivo(c) for c in poblacion]
 # Comprobar cuál es la mejor solución y la media y la peor
 mejor_cromosoma,mejor_fitness,media_fitness,peor_fitness=MejorMediaPeor(fitness)
 print(">Generación %d: Peor: %.3f Media: %.3f Mejor: %.3f" % (gen, peor_fitness, media_fitness, mejor_fitness))
 evolucion.append([mejor_fitness,media_fitness,peor_fitness])
 #Y actualizar el tiempo
 tiempo_actual=time.time()

 # Bucle principal del genético
 while gen<max_gen and tiempo_actual-tiempo_inicio<tiempo_maximo:
    # Aumentar el contador de generaciones
    gen=gen+1
    # Elegir padres (selección)
    seleccionados = [seleccion(poblacion, fitness, tam_torneo) for _ in range(n_poblacion)]
    # Inicializar la lista de hijos
    hijos = list()
    # Si utilizamos elitismo, el primer elemento de la nueva poblacion será el mejor de la anterior
    if elitismo==True:
       hijos.append(poblacion[mejor_cromosoma])
    # Y ahora el resto de elementos
    for i in range(0, n_poblacion, 2):
        # Coger una pareja de padres
        p1, p2 = seleccionados[i], seleccionados[i+1]
        # Aplicar cruce y mutación
        for c in cruce(p1, p2, p_cruce):
            # Mutación
            mutacion(c, p_mut)
            # Guardar el hijo en la lista de hijos (el if es para no meter el ultimo hijo si usamos elitismo)
            if len(hijos)<n_poblacion:
               hijos.append(c)
    # Reemplazar padres por hijos
    poblacion = hijos
    # Evaluar la nueva población
    fitness = [objetivo(c) for c in poblacion]
    # Comprobar cuál es la mejor solución y la media y la peor
    mejor_cromosoma,mejor_fitness,media_fitness,peor_fitness=MejorMediaPeor(fitness)
    print(">Generación %d: Peor: %.3f Media: %.3f Mejor: %.3f" % (gen, peor_fitness, media_fitness, mejor_fitness))
    evolucion.append([mejor_fitness,media_fitness,peor_fitness])
    #Y actualizar el tiempo, para poder comprobar en el bucle si hemos llegado al maximo
    tiempo_actual=time.time()

 #Cuando el bucle principal acaba, simplemente devolvemos la mejor solución de la población
 return [poblacion[mejor_cromosoma], fitness[mejor_cromosoma], evolucion]
 

#Dibuja la mejor ruta encontrada y la evolución del fitness
def DibujarResultados(coordenadas, ruta, evolucion):
   x=[]
   y=[]
   for i in ruta:
      x.append(coordenadas[i][0])
      y.append(coordenadas[i][1])
   plt.figure(figsize=(11,5))
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
   plt.title("Mejor ruta encontrada")
   plt.subplot(122)
   plt.plot(evolucion)
   plt.legend(["Mejor","Media","Peor"])
   plt.xlabel("Generación")
   plt.ylabel("Fitness")
   plt.title("Evolución")
   plt.show()


# ============DEFINICIÓN DE LA INSTANCIA=================================
# Nombre del fichero de coordenadas del TSP (datos del problema a resolver)
nombre = "c:/Users/Usuario/Desktop/instanciasTSP/eil51.tsp"


#========¿QUIERES QUE EL ALGORITMO GENÉTICO MAXIMICE O MINIMICE?==========
# Maximimar o minimizar (si esta a True maximizará)
maximizar = False

# =======COMO CREAR SOLUCIONES INICIALES==============================
# ¿Crear soluciones iniciales utilizando vecino más cercano? Si no, serán aleatorias
utilizar_vecino_mas_cercano = False
# En caso afirmativo, ¿cuántos vecinos más cercanos considerar?
cuantos_vecinos_mas_cercanos = 2

# =======PARÁMETROS PARA CONFIGURAR EL ALGORITMO GENÉTICO===============
# Tamaño de la población
n_poblacion = 100
# Tamaño del torneo (operador de selección)
tam_torneo = 4
# Probabilidad de cruce
p_cruce = 0.9
# Probabilidad de mutación (probabilidad de mutar un cromosoma)
p_mut = 0.1
# Elitismo
elitismo = True

# =======CRITERIOS DE PARADA============================================
# Tiempo máximo de ejecución en segundos
tiempo_maximo = 60
# Número total de generaciones
max_gen = 200
# NOTA: si solo se quiere utilizar uno de los dos criterios, poner el otro valor muy grande



# Ejecutar el Algoritmo Genético
coordenadas=[]
leer_fichero_TSP(nombre, coordenadas)
matriz=[]
crear_matriz_distancias(coordenadas, matriz)
tiempo_inicio=time.time()
mejor_solucion, mejor_fitness, evolucion = algoritmo_genetico(TSP, len(matriz), max_gen, n_poblacion, p_cruce, p_mut)
tiempo_fin=time.time()
print('¡Ejecución finalizada! El tiempo de ejecución fue: %f segundos' % (tiempo_fin-tiempo_inicio))
print('La mejor solución y su fitness:')
print('f(%s) = %f' % (mejor_solucion, mejor_fitness))
DibujarResultados(coordenadas,mejor_solucion,evolucion)