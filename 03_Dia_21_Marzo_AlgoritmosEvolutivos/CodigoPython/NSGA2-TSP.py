# Búsquedas locales aplicadas al problema TSP
from numpy.random import randint
from numpy.random import rand
from numpy.random import permutation
from numpy import exp
import matplotlib.pyplot as plt
import time


# Función objetivo para calcular los valores de fitness de una ruta
def TSP(x):
 fitness1 = sum(matriz1[x[i]][x[i+1]] for i in range(len(x)-1))
 fitness1 = fitness1 + matriz1[x[len(x)-1]][x[0]]
 fitness2 = sum(matriz2[x[i]][x[i+1]] for i in range(len(x)-1))
 fitness2 = fitness2 + matriz2[x[len(x)-1]][x[0]]
 return fitness1,fitness2


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
         if (i==0 and j==0) or (i!=j and dist<minimo): minimo=dist
         if (i==0 and j==0) or (i!=j and dist>maximo): maximo=dist
         linea.append(dist)
      matriz.append(linea)
   return minimo,maximo

# Función para crear una solución desde 0, utilizando el heurístico del vecino más cercano aleatorizado
def vecino_mas_cercano(num_candidatos, weightX, weightY):
   solucion=[]
   ciudadesporvisitar=[]
   for i in range(len(matriz1)):
      ciudadesporvisitar.append(i)
   # La primera ciudad es aleatoria
   ciudadelegida=randint(len(matriz1))
   solucion.append(ciudadelegida)
   ciudadesporvisitar.remove(ciudadelegida)
   # Para el resto de ciudades, elegimos una ciudad al azar de entre las "num_candidatos" ciudades aun no visitadas más cercanas
   while len(solucion)<len(matriz1):
      # Para ello, elegimos las "num_candidatos" primeras ciudades que estén en "ciudadesporvisitar"
      candidatas=[]
      contador=0
      while len(candidatas)<num_candidatos and len(candidatas)<len(ciudadesporvisitar):
         candidatas.append(ciudadesporvisitar[contador])
         contador+=1
      # Miramos cuál es la más lejana de ellas (normalizando los objetivos)
      indicemaslejana=0
      distanciamaslejana=(((matriz1[solucion[len(solucion)-1]][candidatas[indicemaslejana]]-minmatriz1)/(maxmatriz1-minmatriz1))*weightX)+(((matriz2[solucion[len(solucion)-1]][candidatas[indicemaslejana]]-minmatriz2)/(maxmatriz2-minmatriz2))*weightY)
      for i in range(1,len(candidatas)):
         dist=(((matriz1[solucion[len(solucion)-1]][candidatas[i]]-minmatriz1)/(maxmatriz1-minmatriz1))*weightX)+(((matriz2[solucion[len(solucion)-1]][candidatas[i]]-minmatriz2)/(maxmatriz2-minmatriz2))*weightY)
         if dist>distanciamaslejana:
            indicemaslejana=i
            distanciamaslejana=(((matriz1[solucion[len(solucion)-1]][candidatas[i]]-minmatriz1)/(maxmatriz1-minmatriz1))*weightX)+(((matriz2[solucion[len(solucion)-1]][candidatas[i]]-minmatriz2)/(maxmatriz2-minmatriz2))*weightY)
      # Y para cada una de las demás, comprobamos si es más cercana que la más lejana de entre las que ya teníamos
      while contador<len(ciudadesporvisitar):
         dist=(((matriz1[solucion[len(solucion)-1]][ciudadesporvisitar[contador]]-minmatriz1)/(maxmatriz1-minmatriz1))*weightX)+(((matriz2[solucion[len(solucion)-1]][ciudadesporvisitar[contador]]-minmatriz2)/(maxmatriz2-minmatriz2))*weightY)
         if dist<distanciamaslejana:
            candidatas[indicemaslejana]=ciudadesporvisitar[contador]
            # Y si es así, actualizamos la más lejana (normalizando los objetivos)
            indicemaslejana=0
            distanciamaslejana=(((matriz1[solucion[len(solucion)-1]][candidatas[indicemaslejana]]-minmatriz1)/(maxmatriz1-minmatriz1))*weightX)+(((matriz2[solucion[len(solucion)-1]][candidatas[indicemaslejana]]-minmatriz2)/(maxmatriz2-minmatriz2))*weightY)
            for i in range(1,len(candidatas)):
               dist=(((matriz1[solucion[len(solucion)-1]][candidatas[i]]-minmatriz1)/(maxmatriz1-minmatriz1))*weightX)+(((matriz2[solucion[len(solucion)-1]][candidatas[i]]-minmatriz2)/(maxmatriz2-minmatriz2))*weightY)
               if dist>distanciamaslejana:
                  indicemaslejana=i
                  distanciamaslejana=(((matriz1[solucion[len(solucion)-1]][candidatas[i]]-minmatriz1)/(maxmatriz1-minmatriz1))*weightX)+(((matriz2[solucion[len(solucion)-1]][candidatas[i]]-minmatriz2)/(maxmatriz2-minmatriz2))*weightY)
         contador+=1
      # Para acabar, elegimos una candidata al azar, la añadimos a la solución parcial, y la quitamos de ciudadesporvisitar
      elegida=randint(0,len(candidatas))
      solucion.append(candidatas[elegida])
      ciudadesporvisitar.remove(candidatas[elegida])
   # Y finalmente devolvemos la solución completa
   return solucion


# Selección por torneo
def seleccion(poblacion, rank, crowdingdistance, tam_torneo):
 # Elegimos un individuo aleatorio
 elegido = randint(len(poblacion))
 for i in randint(0, len(poblacion), tam_torneo-1):
    # Comprobamos si es mejor (es decir, hacemos un torneo)
    if (rank[i] < rank[elegido]) or (rank[i] == rank[elegido] and crowdingdistance[i]>crowdingdistance[elegido]):
        elegido = i
 return poblacion[elegido]


# Cruzamos dos padres para crear dos hijos (Order Crossover)
def cruce(p1, p2, p_cruce):
 # Los hijos, por defecto, son copias de los padres
 c1, c2 = p1.copy(), p2.copy()
 # Comprobamos si hay que cruzarlos (probabilidad de cruce)
 if rand() < p_cruce:
    puntomin = randint(0, len(p1))
    puntomax = randint(0, len(p1))
    while puntomin==puntomax:
       puntomax = randint(0, len(p1))
    if puntomin>puntomax:
       puntomin, puntomax = puntomax, puntomin
    punterop1=0
    punterop2=0
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


# Devuelve True si ind1 domina a ind2, y devuelve False si no (supuesto que estamos minimizando dos objetivos)
def dominaA(ind1, ind2, fitness):
   if fitness[ind1][0]<fitness[ind2][0] and fitness[ind1][1]<=fitness[ind2][1]: return True
   if fitness[ind1][0]<=fitness[ind2][0] and fitness[ind1][1]<fitness[ind2][1]: return True
   return False


# Función que divide un conjunto de soluciones en varios frentes no-dominados
def fast_nondominated_sort(fitness):
   frentes = [[]]
   domination_count = [0 for _ in range(len(fitness))]
   dominated_solutions = [[] for _ in range(len(fitness))]
   rank = [0 for _ in range(len(fitness))]
   for i in range(len(fitness)):
      for j in range(len(fitness)):
         if dominaA(i,j,fitness):
            dominated_solutions[i].append(j)
         elif dominaA(j,i,fitness):
            domination_count[i] += 1
      if domination_count[i] == 0:
         rank[i] = 0
         frentes[0].append(i)
   i = 0
   while len(frentes[i]) > 0:
      temp = []
      for ind in frentes[i]:
         for ind2 in dominated_solutions[ind]:
            domination_count[ind2] -= 1
            if domination_count[ind2] == 0:
               rank[ind2] = i + 1
               temp.append(ind2)
      i = i + 1
      frentes.append(temp)
   frentes.pop()
   return rank, frentes


# Función que determina cuáles son las soluciones más diversas, dentro de un mismo frente
def calculate_crowding_distance(frentes,fitness):
   crowdingdistance = [0 for _ in range(len(fitness))]
   for numfrente in range(len(frentes)):
      for objetivo in range(len(fitness[0])):
         # Ordena el frente de menor a mayor segun el objetivo
         frentetemp=sorted(frentes[numfrente], key=lambda x: fitness[x][objetivo])
         crowdingdistance[frentetemp[0]]=10**9
         crowdingdistance[frentetemp[len(frentetemp)-1]]=10**9
         escalado = fitness[frentetemp[len(frentetemp)-1]][objetivo] - fitness[frentetemp[0]][objetivo]
         if escalado == 0: escalado = 1
         for i in range(1,len(frentetemp)-1):
            crowdingdistance[frentetemp[i]] += (fitness[frentetemp[i+1]][objetivo]-fitness[frentetemp[i-1]][objetivo]) / escalado
   return crowdingdistance


# Función que penaliza (envía a los últimos frentes) a las soluciones "repetidas"
def penaliza_repetidos(fitness, rank, frentes):
   numFrentesActual=len(frentes)
   for i in range(0,numFrentesActual):
      frentes.append([])
      for j in range(0,len(frentes[i])-1):
         for h in range(len(frentes[i])-1, j, -1):
            if fitness[frentes[i][j]]==fitness[frentes[i][h]]:
               # Si entramos aquí, es porque los individuos j y h del frente i son iguales
               frentes[len(frentes)-1].append(frentes[i][h])
               rank[frentes[i][h]]=len(frentes)-1
               del frentes[i][h]
      if len(frentes[len(frentes)-1])==0: del frentes[len(frentes)-1]


# Algoritmo Genético NSGA-II
def algoritmo_genetico(objetivo, max_gen, n_poblacion, p_cruce, p_mut):
 gen=0
 evolucion=[]
 # Población inicial de permutaciones aleatorias o heurísticas
 if utilizar_vecino_mas_cercano == False:
   ciudades=[]
   for i in range(len(matriz1)):
      ciudades.append(i)
   poblacion = [permutation(ciudades) for _ in range(n_poblacion)]
 else:
   poblacion=[]
   for i in range(n_poblacion):
      poblacion.append(vecino_mas_cercano(cuantos_vecinos_mas_cercanos,i/(n_poblacion-1),1-(i/(n_poblacion-1))))
 # Evaluar la población inicial
 fitness=[]
 for i in range(n_poblacion): fitness.append(objetivo(poblacion[i]))
 # Separar la poblacion en frentes y calcular el crowding distance
 rank, frentes = fast_nondominated_sort(fitness)
 if QuieroPenalizarRepetidos==True: penaliza_repetidos(fitness, rank, frentes)
 crowdingdistance = calculate_crowding_distance(frentes,fitness)
 # Datos de la población inicial
 fitnesspoblacioninicial=[]
 for i in range(n_poblacion): fitnesspoblacioninicial.append(fitness[i])
 hip=hipervolumen(frentes[0], fitness, referencepoint, originpoint)
 print('Generación', gen, 'Hipervolumen:', hip)
 evolucion.append(hip)
 # Y actualizar el tiempo
 tiempo_actual=time.time()

 # Bucle principal del genético
 while gen<max_gen and tiempo_actual-tiempo_inicio<tiempo_maximo:
    # Aumentar el contador de generaciones
    gen=gen+1
    # Elegir padres (selección)
    seleccionados = [seleccion(poblacion, rank, crowdingdistance, tam_torneo) for _ in range(n_poblacion)]
    # Crear la siguiente generación
    hijos = list()
    for i in range(0, n_poblacion, 2):
        # Coger una pareja de padres
        p1, p2 = seleccionados[i], seleccionados[i+1]
        # Aplicar cruce y mutación
        for c in cruce(p1, p2, p_cruce):
            # Mutación
            mutacion(c, p_mut)
            # Guardar para la siguiente generación
            hijos.append(c)
    # Juntar padres e hijos
    poblacion += hijos
    # Evaluar los hijos
    for i in range(n_poblacion,n_poblacion*2): fitness.append(objetivo(poblacion[i]))
    # Separar la poblacion en frentes y calcular el crowding distance
    rank, frentes = fast_nondominated_sort(fitness)
    if QuieroPenalizarRepetidos==True: penaliza_repetidos(fitness, rank, frentes)
    crowdingdistance = calculate_crowding_distance(frentes,fitness)
    # Elegir qué individuos pasan a la siguiente generación
    cuantos_en_poblacion=0
    numfrente=0
    while cuantos_en_poblacion+len(frentes[numfrente])<=n_poblacion:
       cuantos_en_poblacion+=len(frentes[numfrente])
       numfrente+=1
    # Cuando lleguemos aquí es porque el frente "numfrente" no cabe entero
    frentetemp=sorted(frentes[numfrente], key=lambda x: crowdingdistance[x])
    # Utilizaremos un vector "hayQueQuitarlos" para ir marcando cuáles hay que quitar
    hayQueQuitarlos = [0 for _ in range(len(poblacion))]
    # Hay que quitar los peores cuantos_en_poblacion+len(frentes[numfrente])-n_poblacion
    for i in range(0,cuantos_en_poblacion+len(frentetemp)-n_poblacion):
       hayQueQuitarlos[frentetemp[i]]=1
    # Y quitar el resto de frentes
    for quefrente in range(numfrente+1,len(frentes)):
       for indenfrente in range(0,len(frentes[quefrente])):
          hayQueQuitarlos[frentes[quefrente][indenfrente]]=1
    # Antes de quitarlos, mostramos datos de la nueva población
    hip=hipervolumen(frentes[0], fitness, referencepoint, originpoint)
    print('Generación', gen, 'Hipervolumen:', hip)
    evolucion.append(hip)
    # Y ahora los quitamos de verdad
    for i in range((n_poblacion*2)-1, -1, -1):
       if hayQueQuitarlos[i]==1:
         del poblacion[i]
         del fitness[i]
         del rank[i]
         del crowdingdistance[i]

    #Y actualizar el tiempo, para poder comprobar en el bucle si hemos llegado al máximo
    tiempo_actual=time.time()

 return [poblacion, fitness, fitnesspoblacioninicial, evolucion]


# Calcula el hipervolumen
def hipervolumen(nodominadas,fitness, ref, origen=[0,0]):
   # Ordena el frente de menor a mayor según el objetivo
   frenteordenado=sorted(nodominadas, key=lambda x: fitness[x][0])
   # Primero añadimos el área dominada por el primer individuo del frente
   horizontal=(ref[0]-fitness[frenteordenado[0]][0])/(ref[0]-origen[0])
   vertical=(ref[1]-fitness[frenteordenado[0]][1])/(ref[1]-origen[1])
   hipervol=horizontal*vertical
   # Y luego el área nueva que dominan los demás
   for i in range(1,len(frenteordenado)):
      horizontal=(ref[0]-fitness[frenteordenado[i]][0])/(ref[0]-origen[0])
      vertical=(fitness[frenteordenado[i-1]][1]-fitness[frenteordenado[i]][1])/(ref[1]-origen[1])
      hipervol += horizontal*vertical
   return hipervol


# Dibuja el fitness de las soluciones de la población, y la evolución del hipervolumen
def DibujarResultados(fitness, rank, fitnessinicial, evolucion):
   plt.figure(figsize=(14,5))
   plt.subplot(121)
   x=[]
   y=[]
   for i in range(0,len(fitnessinicial)):
      x.append(fitnessinicial[i][0])
      y.append(fitnessinicial[i][1])
   plt.plot(x, y, 'go', markersize=4.0)
   plt.xlim(0, max(x)*1.1)
   plt.ylim(0, max(y)*1.1)
   x=[]
   y=[]
   for i in range(0,len(fitness)):
      x.append(fitness[i][0])
      y.append(fitness[i][1])
   plt.plot(x, y, 'bo', markersize=4.0)
   x=[]
   y=[]
   for i in range(0,len(fitness)):
      if rank[i]==0:
         x.append(fitness[i][0])
         y.append(fitness[i][1])
   plt.plot(x, y, 'ro', markersize=6.0)
   plt.legend(["Solución inicial", "Solución final dominada","Solución final no dominada"])     
   plt.xlabel("Objetivo 1")
   plt.ylabel("Objetivo 2")
   plt.title("Fitness de las soluciones en la población")
   plt.subplot(122)
   plt.plot(evolucion)
   plt.xlabel("Generación")
   plt.title("Evolución del hipervolumen")
   plt.show()


# ==============DEFINICIÓN DE LA INSTANCIA===================================
# Nombres de los ficheros de coordenadas del TSP (datos del problema a resolver)
nombre1 = "c:/Users/Usuario/Desktop/instanciasTSP/kroA100.tsp"
nombre2 = "c:/Users/Usuario/Desktop/instanciasTSP/kroB100.tsp"

# ==================COMO CREAR SOLUCIONES INICIALES========================
# ¿Crear soluciones iniciales utilizando vecino más cercano? Si no, serán aleatorias
utilizar_vecino_mas_cercano = True
# En caso afirmativo, ¿cuántos vecinos más cercanos considerar?
cuantos_vecinos_mas_cercanos = 2

# ==========PARÁMETROS PARA CONFIGURAR EL ALGORITMO GENÉTICO================
# Tamaño de la población
n_poblacion = 200
# Tamaño del torneo (operador de selección)
tam_torneo = 2
# Probabilidad de cruce
p_cruce = 0.9
# Probabilidad de mutación (probabilidad de mutar un cromosoma)
p_mut = 0.1
# Penalizar individuos repetidos
QuieroPenalizarRepetidos = True

# =======CRITERIOS DE PARADA PARA EL ALGORITMO GENÉTICO===================
# Tiempo máximo de ejecución en segundos
tiempo_maximo = 3600
# Número total de generaciones
max_gen = 200
# NOTA: si solo se quiere utilizar uno de los dos criterios, poner el otro valor muy grande

# ===========PUNTOS PARA CALCULAR EL HIPERVOLUMEN==================
# Punto de referencia
referencepoint = [250000,250000]
# Punto origen
originpoint = [0,0]

# ==============EJECUCIÓN DE LOS MÉTODOS====================================
# Leer los ficheros del problema y crear las matrices de distancias
coordenadas1=[]
leer_fichero_TSP(nombre1, coordenadas1)
matriz1=[]
minmatriz1,maxmatriz1 = crear_matriz_distancias(coordenadas1, matriz1)
coordenadas2=[]
leer_fichero_TSP(nombre2, coordenadas2)
matriz2=[]
minmatriz2,maxmatriz2 = crear_matriz_distancias(coordenadas2, matriz2)
# Ejecutar el método
tiempo_inicio=time.time()
poblacion, fitness, fitnessinicial, evolucion = algoritmo_genetico(TSP, max_gen, n_poblacion, p_cruce, p_mut)
tiempo_fin=time.time()
# Mostrar el tiempo y la población final
print('¡Ejecución finalizada! El tiempo de ejecución fue: %f segundos' % (tiempo_fin-tiempo_inicio))
rank, frentes = fast_nondominated_sort(fitness)
penaliza_repetidos(fitness, rank, frentes)
frenteordenado=sorted(frentes[0], key=lambda x: fitness[x][0])
for i in range(len(frenteordenado)):
   print('Solución:', i+1, 'Fitness:', fitness[frenteordenado[i]])
print('El hipervolumen (utilizando reference point =', referencepoint, ', origin point =', originpoint, ') es', hipervolumen(frentes[0], fitness, referencepoint, originpoint))
DibujarResultados(fitness, rank, fitnessinicial, evolucion)
