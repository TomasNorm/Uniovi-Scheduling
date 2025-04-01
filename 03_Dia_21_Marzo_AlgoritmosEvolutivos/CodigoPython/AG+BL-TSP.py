# Búsquedas locales aplicadas al problema TSP
from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
from numpy import exp
import matplotlib.pyplot as plt
import time


# Función objetivo para calcular una ruta de forma completa
def TSP(x):
 suma = sum(matriz[x[i]][x[i+1]] for i in range(len(x)-1))
 suma = suma + matriz[x[len(x)-1]][x[0]]
 return suma


# Evaluar de forma rápida el incremento de fitness de un vecino creado con la vecindad de intercambio
def TSPincremental(x, i, j):
 sumaarcosnuevos=0
 sumaarcosviejos=0
 if i==0 and j==len(x)-1:
    sumaarcosnuevos+=matriz[x[j-1]][x[j]]
    sumaarcosnuevos+=matriz[x[j]][x[i]]
    sumaarcosnuevos+=matriz[x[i]][x[i+1]]
    sumaarcosviejos+=matriz[x[j-1]][x[i]]
    sumaarcosviejos+=matriz[x[i]][x[j]]
    sumaarcosviejos+=matriz[x[j]][x[i+1]]
 elif j==i+1:
    sumaarcosnuevos+=matriz[x[i-1]][x[i]]
    sumaarcosnuevos+=matriz[x[i]][x[i+1]]
    if j==len(x)-1:
       sumaarcosnuevos+=matriz[x[j]][x[0]]
    else:
       sumaarcosnuevos+=matriz[x[j]][x[j+1]]
    sumaarcosviejos+=matriz[x[i-1]][x[j]]
    sumaarcosviejos+=matriz[x[j]][x[i]]
    if j==len(x)-1:
       sumaarcosviejos+=matriz[x[i]][x[0]]
    else:
       sumaarcosviejos+=matriz[x[i]][x[j+1]]    
 else:
    sumaarcosnuevos+=matriz[x[i-1]][x[i]]
    sumaarcosnuevos+=matriz[x[i]][x[i+1]]
    sumaarcosnuevos+=matriz[x[j-1]][x[j]]
    if j==len(x)-1:
       sumaarcosnuevos+=matriz[x[j]][x[0]]
    else:
       sumaarcosnuevos+=matriz[x[j]][x[j+1]]
    sumaarcosviejos+=matriz[x[i-1]][x[j]]
    sumaarcosviejos+=matriz[x[j]][x[i+1]]
    sumaarcosviejos+=matriz[x[j-1]][x[i]]
    if j==len(x)-1:
       sumaarcosviejos+=matriz[x[i]][x[0]]
    else:
       sumaarcosviejos+=matriz[x[i]][x[j+1]]

 return sumaarcosnuevos-sumaarcosviejos


# Funcion para leer las coordenadas de un fichero
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


# Funcion para crear la matriz de distancias, a partir de las coordenadas
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
   

# Función para generar vecinos de una solución (intercambiar dos posiciones)
def vecindadintercambio(solucion):
   vecinos=[]
   intercambios=[]
   numvecinos=0
   for i in range(len(solucion)-1):
      for j in range(i+1,i+rangointercambio+1):
         if j<len(solucion):
            vecinos.append(solucion.copy())
            vecinos[numvecinos][i],vecinos[numvecinos][j] = (vecinos[numvecinos][j], vecinos[numvecinos][i])
            numvecinos+=1
            intercambios.append([i,j])
   return vecinos, intercambios


# Escalada de maximo gradiente
def escalada_maximo_gradiente(objetivo, objetivoincremental, solucioninicial, genera_vecinos):
 solucionactual = solucioninicial
 fitnessactual = objetivo(solucionactual)
 evolucion=[]
 #Bucle principal del método
 hayMejora=True
 while hayMejora==True:
    evolucion.append(fitnessactual)
    hayMejora=False
    #Generamos y evaluamos todos los vecinos
    vecinos,intercambios=genera_vecinos(solucionactual)
    fitness_vecinos=[]
    for i in range(len(vecinos)):
       if evaluacionincrementalvecinos==False:
          fitness_vecinos.append(objetivo(vecinos[i]))
       else:
          fitness_vecinos.append(fitnessactual+objetivoincremental(vecinos[i],intercambios[i][0],intercambios[i][1]))
    #Miramos qué vecino es el mejor de todos
    mejor_vecino=0
    fitness_mejor_vecino=fitness_vecinos[0]
    for i in range(1,len(vecinos)):
       if esMejorQue(fitness_vecinos[i],fitness_mejor_vecino):
          mejor_vecino=i
          fitness_mejor_vecino=fitness_vecinos[i]
    #Y si es mejor que la solución actual, continuamos la escalada
    if esMejorQue(fitness_mejor_vecino,fitnessactual):
       solucionactual=vecinos[mejor_vecino]
       fitnessactual=fitness_mejor_vecino
       hayMejora=True

 return [solucionactual, fitnessactual, evolucion]


# Búsqueda local multiarranque / GRASP
def BusquedaLocalMultiarranque(objetivo, objetivoincremental, genera_vecinos):
   evolucion=[]
   mejor_fitness=0
   iter=0
   tiempo_actual=time.time()
   # Bucle principal
   while iter<max_iter and tiempo_actual-tiempo_inicio<tiempo_maximo_multiarranque:
      # Generar una solución inicial
      solucioninicial=crear_solucion_inicial()
      fitnessinicial = objetivo(solucioninicial)
      # Aplicarle una búsqueda local
      optimolocal,fitnessmejorado,evolucionescalada=escalada_maximo_gradiente(objetivo,objetivoincremental,solucioninicial,genera_vecinos)
      # Actualizar si es la mejor solución encontrada hasta el momento
      if iter==0 or esMejorQue(fitnessmejorado,mejor_fitness):
         mejor_solucion=optimolocal
         mejor_fitness=fitnessmejorado
      print('Iteración %d: Fitness solución inicial %f, Fitness solución mejorada %f' % (iter, fitnessinicial, fitnessmejorado))
      iter=iter+1
      evolucion.append([mejor_fitness,fitnessmejorado])
      #Y actualizar el tiempo, para poder comprobar en el bucle si hemos llegado al maximo
      tiempo_actual=time.time()

   return [mejor_solucion, mejor_fitness, evolucion]


#Enfriamiento simulado
def EnfriamientoSimulado(objetivo, objetivoincremental, genera_vecinos):
   evolucion=[]
   # Generar una solucion inicial y evaluarla
   solucionactual=crear_solucion_inicial()
   fitnessactual=objetivo(solucionactual)
   # Guardarla como la mejor hasta el momento
   mejor_solucion=solucionactual
   mejor_fitness=fitnessactual
   evolucion.append([mejor_fitness,fitnessactual])
   # Inicializar la temperatura y el tiempo
   temp=temperaturainicial
   tiempo_actual=time.time()
   # Variable que indica si hay que crear la vecindad de la solución o si ya la tenemos creada
   hay_que_crear_vecindad=True
   # Bucle principal (ejecutar hasta que no lleguemos a la temperatura final)
   while temp>temperaturafinal and tiempo_actual-tiempo_inicio<tiempo_maximo_enfriamiento:
      # Ejecutamos un cierto número de iteraciones en cada temperatura
      for iter in range(iters_cada_temperatura):
         # Creamos la vecindad si no lo estuviese ya
         if hay_que_crear_vecindad==True:
            vecinos,intercambios=genera_vecinos(solucionactual)
            hay_que_crear_vecindad=False
         # Elegimos un vecino aleatorio y lo evaluamos
         numaleatorio=randint(len(vecinos))
         if evaluacionincrementalvecinos==False:
            fitnessvecino=objetivo(vecinos[numaleatorio])
         else:
            fitnessvecino=fitnessactual+objetivoincremental(vecinos[numaleatorio],intercambios[numaleatorio][0],intercambios[numaleatorio][1])
         # Si el vecino es mejor o igual que la solución actual, nos lo quedamos, y también con una cierta probabilidad si es peor
         aceptacion=False
         if esMejorQue(fitnessvecino,fitnessactual) or (fitnessvecino==fitnessactual):
            aceptacion=True
            if mostrarejecucion==True: print('Temp %f Iter %d Fitness actual %f Fitness vecino %f. SE ACEPTA (es mejor o igual)' % (temp, iter, fitnessactual, fitnessvecino))
         else:
            metropolis=exp((-abs(fitnessvecino-fitnessactual))/temp)
            aleat=rand()
            if aleat<metropolis:
               aceptacion=True
               if mostrarejecucion==True: print('Temp %f Iter %d Fitness actual %f Fitness vecino %f. SE ACEPTA (%f < %f)' % (temp, iter, fitnessactual, fitnessvecino, aleat, metropolis))
            else:
               if mostrarejecucion==True: print('Temp %f Iter %d Fitness actual %f Fitness vecino %f. SE RECHAZA (%f >= %f)' % (temp, iter, fitnessactual, fitnessvecino, aleat, metropolis))
         if aceptacion==True:
            solucionactual=vecinos[numaleatorio]
            fitnessactual=fitnessvecino
            hay_que_crear_vecindad=True
            # Y comprobamos si es el mejor hasta el momento
            if esMejorQue(fitnessactual,mejor_fitness):
               mejor_solucion=solucionactual
               mejor_fitness=fitnessactual
         evolucion.append([mejor_fitness,fitnessactual])
      print('Temperatura: %f. Mejor fitness hasta el momento: %f' % (temp, mejor_fitness))
      # Y decrementamos la temperatura
      temp=temp*factor_decrecimiento
      # Y actualizar el tiempo, para poder comprobar en el bucle si hemos llegado al maximo
      tiempo_actual=time.time()


   # Finalmente, devolvemos la mejor solución encontrada
   return [mejor_solucion, mejor_fitness, evolucion]


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
def algoritmo_genetico(objetivo, objetivoincremental, genera_vecinos, n_bits, max_gen, n_poblacion, p_cruce, p_mut, p_busquedalocal):
 gen=0
 evolucion=[]
 # Crear población inicial
 poblacion=[crear_solucion_inicial() for _ in range(n_poblacion)]
 # Aplicar búsqueda local a la población y evaluarla
 fitness=[]
 for i in range(n_poblacion):
    if (metodo==4) and (rand() < p_busquedalocal):
       optimolocal,fitnessmejorado,evolucionescalada=escalada_maximo_gradiente(objetivo,objetivoincremental,poblacion[i],genera_vecinos)
       fitness.append(fitnessmejorado)
       if evolucion_lamarckiana==True: poblacion[i]=optimolocal
    else:
       fitness.append(objetivo(poblacion[i]))
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
    # Aplicar búsqueda local a la población y evaluarla
    fitness=[]
    for i in range(n_poblacion):
       if (metodo==4) and (rand() < p_busquedalocal):
          optimolocal,fitnessmejorado,evolucionescalada=escalada_maximo_gradiente(objetivo,objetivoincremental,poblacion[i],genera_vecinos)
          fitness.append(fitnessmejorado)
          if evolucion_lamarckiana==True: poblacion[i]=optimolocal
       else:
          fitness.append(objetivo(poblacion[i]))
    # Comprobar cuál es la mejor solución y la media y la peor
    mejor_cromosoma,mejor_fitness,media_fitness,peor_fitness=MejorMediaPeor(fitness)
    print(">Generación %d: Peor: %.3f Media: %.3f Mejor: %.3f" % (gen, peor_fitness, media_fitness, mejor_fitness))
    evolucion.append([mejor_fitness,media_fitness,peor_fitness])
    #Y actualizar el tiempo, para poder comprobar en el bucle si hemos llegado al maximo
    tiempo_actual=time.time()

 #Cuando el bucle principal acaba, simplemente devolvemos la mejor solución de la población
 return [poblacion[mejor_cromosoma], fitness[mejor_cromosoma], evolucion]


#Dibuja la mejor ruta encontrada y la evolucion del fitness
def DibujarResultados(coordenadas, ruta, evolucion=[]):
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
   if metodo==0:
      plt.legend(["Fitness de la solución actual"])
      plt.xlabel("Iteración de la escalada")
   if metodo==1:
      plt.legend(["Mejor solución hasta el momento","Solución devuelta por cada escalada"])
      plt.xlabel("Número de la escalada")
   if metodo==2:
      plt.legend(["Mejor solución","Solución actual"])
      plt.xlabel("Iteración de enfriamiento simulado")
   if metodo==3 or metodo==4:
      plt.legend(["Mejor","Media","Peor"])  
      plt.xlabel("Generación")
   plt.ylabel("Fitness")
   plt.title("Evolución")
   plt.show()


# ==============DEFINICIÓN DE LA INSTANCIA===================================
# Nombre del fichero de coordenadas del TSP (datos del problema a resolver)
nombre = "c:/Users/Usuario/Desktop/instanciasTSP/eil51.tsp"

# =========SELECCIÓN DEL MÉTODO DE RESOLUCIÓN================================
# Una única escalada (0), Multiarranque/GRASP (1), enfriamiento simulado (2), algoritmo genético (3), algoritmo memético (4) ?
metodo = 4

#========¿QUIERES MAXIMIZAR O MINIMIZAR?==========
# Maximimar o minimizar (si esta a True maximizará)
maximizar = False

# ===COMO CREAR SOLUCIONES INICIALES (TANTO EN BÚSQUEDA LOCAL COMO EN GENÉTICOS)===
# ¿Crear soluciones iniciales utilizando vecino más cercano? Si no, serán aleatorias
utilizar_vecino_mas_cercano = True
# En caso afirmativo, ¿cuántos vecinos más cercanos considerar?
cuantos_vecinos_mas_cercanos = 3

# =========PARÁMETROS PARA CONFIGURAR TODAS LAS BÚSQUEDAS LOCALES================
# Rango de intercambio para la vecindad de intercambio (p.ej. 1=solo intercambiar posiciones adyacentes)
rangointercambio = 60
# Utilizar la evaluación incremental de vecinos para acelerar la ejecución
evaluacionincrementalvecinos = True

# =======CRITERIO DE PARADA PARA LA BÚSQUEDA MULTIARRANQUE/GRASP===============
# Multiarranque/GRASP: Número total de iteraciones
max_iter = 1000
# Multiarranque/GRASP: Tiempo máximo de ejecución en segundos
tiempo_maximo_multiarranque = 30
# NOTA: si solo se quiere utilizar uno de los dos criterios, poner el otro valor muy grande

# ============PARAMETROS PARA CONFIGURAR EL ENFRIAMIENTO SIMULADO================
# Enfriamiento simulado: temperatura inicial
temperaturainicial = 12
# Por cuánto multiplicamos la temperatura cada vez que la disminuimos
factor_decrecimiento = 0.997
# Enfriamiento simulado: iteraciones en cada temperatura
iters_cada_temperatura = 400
# Enfriamiento simulado: mostrar ejecución detallada paso a paso
mostrarejecucion = False

# =======CRITERIO DE PARADA PARA EL ENFRIAMIENTO SIMULADO===============
# Enfriamiento simulado: temperatura final
temperaturafinal = 0.4
# Enfriamiento simulado: Tiempo máximo de ejecución en segundos
tiempo_maximo_enfriamiento = 30
# NOTA: si solo se quiere utilizar tiempo, poner una temperatura final negativa
# NOTA: si solo se quiere utilizar temperatura final, poner un tiempo muy elevado

# =======PARÁMETROS PARA CONFIGURAR EL ALGORITMO GENÉTICO/MEMÉTICO===============
# Tamaño de la población
n_poblacion = 100
# Tamaño del torneo (operador de seleccion)
tam_torneo = 3
# Probabilidad de cruce
p_cruce = 0.9
# Probabilidad de mutación (probabilidad de mutar un cromosoma)
p_mut = 0.1
# Elitismo
elitismo = True

# =======CRITERIOS DE PARADA PARA EL ALGORITMO GENÉTICO/MEMÉTICO================
# Tiempo máximo de ejecución en segundos
tiempo_maximo = 30
# Número total de generaciones
max_gen = 10000
# NOTA: si solo se quiere utilizar uno de los dos criterios, poner el otro valor muy grande

# =======PARÁMETROS PARA CONFIGURAR EL ALGORITMO MEMÉTICO=====================
# Probabilidad de aplicar escalada a cada cromosoma
p_busquedalocal = 1
# Evolución Lamarckiana (True) o Baldwiniana (False)
evolucion_lamarckiana = True


# ==============EJECUCIÓN DE LOS MÉTODOS=========================================
# Leer el fichero del problema y crear la matriz de distancias
coordenadas=[]
leer_fichero_TSP(nombre, coordenadas)
matriz=[]
crear_matriz_distancias(coordenadas, matriz)

# Una unica escalada
if metodo==0:
   # Generar una solucion inicial
   solucioninicial=crear_solucion_inicial()
   DibujarResultados(coordenadas,solucioninicial)
   #Y ahora ejecutar escalada
   tiempo_inicio=time.time()
   mejor_solucion, mejor_fitness, evolucion = escalada_maximo_gradiente(TSP, TSPincremental, solucioninicial, vecindadintercambio)
# Búsqueda Local Multiarranque / GRASP
if metodo==1:
   tiempo_inicio=time.time()
   mejor_solucion, mejor_fitness, evolucion = BusquedaLocalMultiarranque(TSP, TSPincremental, vecindadintercambio)
# Enfriamiento simulado
if metodo==2:
   tiempo_inicio=time.time()
   mejor_solucion, mejor_fitness, evolucion = EnfriamientoSimulado(TSP, TSPincremental, vecindadintercambio)
# Algoritmo genético / memético
if metodo==3 or metodo==4:
   tiempo_inicio=time.time()
   mejor_solucion, mejor_fitness, evolucion = algoritmo_genetico(TSP, TSPincremental, vecindadintercambio, len(matriz), max_gen, n_poblacion, p_cruce, p_mut, p_busquedalocal)
# Mostrar resultados
tiempo_fin=time.time()
print('¡Ejecución finalizada! El tiempo de ejecución fue: %f segundos' % (tiempo_fin-tiempo_inicio))
print('La mejor solución y su fitness:')
print('f(%s) = %f' % (mejor_solucion, mejor_fitness))
DibujarResultados(coordenadas,mejor_solucion,evolucion)
# Si hemos utilizado un memético con evolución baldwiniana, mostramos también el resultado de aplicar escalada al mejor cromosoma
if metodo==4 and p_busquedalocal>0 and evolucion_lamarckiana==False:
   mejor_solucion_bis, mejor_fitness_bis, evolucion_bis = escalada_maximo_gradiente(TSP, TSPincremental, mejor_solucion, vecindadintercambio)
   print('Al ser un memético con evolución baldwiniana, mostramos también el resultado de aplicar escalada al mejor cromosoma')
   DibujarResultados(coordenadas,mejor_solucion_bis,evolucion_bis)