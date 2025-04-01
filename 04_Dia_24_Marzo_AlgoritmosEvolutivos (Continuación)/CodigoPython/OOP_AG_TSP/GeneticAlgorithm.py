from Solution import Solution # para la clase que representa los individuos
from Tiempo import Tiempo # para la clase que mide el tiempo




### ---------------------------------------------------------------------------
### CLASE ALGORITMO GENÉTICO
### ---------------------------------------------------------------------------

class GeneticAlgorithm:

    # prob: instancia del problema a resolver
    # cfg: configuracion del algoritmo genetico
    # evolucion_mejor_media_peor_fitness: mejor/media/peor fitness de cada generacion
    # pos_mejor_cromosoma: posicion del mejor cromosoma en la generacion actual
    # traza: indica si hay que mostrar la traza de cada generacion
    # creator: objeto operador de generacion de cromosomas
    # evaluator: objeto operador evaluador de cromosomas
    # selection: objeto operador de seleccion de cromosomas
    # replacement: objeto operador de reemplazo de cromosomas
    # crossover: objeto operador de cruce de cromosomas
    # mutation: objeto operador de mutacion de cromosomas
    def __init__(self, cfg, traza = True):
        self.prob = cfg.problem
        self.cfg = cfg
        self.__configure()
        self.traza = traza
        self.evolucion_mejor_media_peor_fitness = []
        self.pos_mejor_cromosoma = 0

    # Método que asigna los distintos operadores del GA: creacion (creator), 
    # evaluación (evaluator), seleccion (selector), remplazamiento (replacement), 
    # cruce (crossover) y mutación (mutation); procedentes del objeto de configuracion (cfg)  
    def __configure(self):
        # fijar los operadores concretos para el GA

        # operadores dependientes del problema y la respresentacion
        # creacion
        self.creator = self.cfg.creator
        # decodificacion 
        self.decoder = self.cfg.decoder
        # evaluacion
        self.evaluator = self.cfg.evaluator

        # operadores independientes del problema y la representacion
        # seleccion
        self.selection = self.cfg.selection
        # reemplazamiento
        self.replacement = self.cfg.replace
        
        # operadores dependientes de la representacion (y el problema)
        # cruce
        self.crossover = self.cfg.crossover
        # mutacion
        self.mutation = self.cfg.mutation

    # Método principal de ejecucion del GA
    def run(self):
        Tiempo.inicia()
        self.t_creator = 0
        self.t_evaluator = 0
        self.t_seleccion = 0
        self.t_cruce = 0
        self.t_mutacion = 0

        gen = 0
        self.__init_traza_evolucion()
        t = Tiempo.actual()
        poblacion = self.__genera_poblacion_inicial()
        self.t_creator += Tiempo.actual()-t
        t = Tiempo.actual()
        self.__evalua_poblacion(poblacion)
        self.t_evaluator += Tiempo.actual()-t
        self.__actualiza_evolucion(gen, poblacion)

        while gen<self.cfg.max_gen and Tiempo.actual() < self.cfg.tiempo_maximo:
            t = Tiempo.actual(); poblacion2 = self.__seleccion(poblacion)
            self.t_seleccion += Tiempo.actual()-t
            t = Tiempo.actual()
            poblacion2 = self.__cruce(poblacion2)
            self.t_cruce += Tiempo.actual()-t
            t = Tiempo.actual()
            poblacion2 = self.__mutacion(poblacion2)
            self.t_mutacion += Tiempo.actual()-t
            t = Tiempo.actual()
            self.__evalua_poblacion(poblacion2)
            self.t_evaluator += Tiempo.actual()-t
            t = Tiempo.actual()
            poblacion = self.__reemplazamiento(poblacion, poblacion2) # incluye elitismo
            self.t_replacement += Tiempo.actual()-t
            self.__actualiza_evolucion(gen, poblacion)
            
            gen += 1
            #print("Gen: " + str(gen))

        Tiempo.finaliza()

        # <!> tiempo empleado por el operador creator
        print ("Tiempos:")
        print (f"Creación: {self.t_creator:.08f}({self.t_creator/Tiempo.total()*100:.02f}%)")
        print (f"Selección: {self.t_seleccion:.08f}({self.t_seleccion/Tiempo.total()*100:.02f}%)")
        print (f"Reemplazamiento: {self.t_replacement:.08f}({self.t_replacement/Tiempo.total()*100:.02f}%)")
        print (f"Cruce: {self.t_cruce:.08f}({self.t_cruce/Tiempo.total()*100:.02f}%)")
        print (f"Mutación: {self.t_mutacion:.08f}({self.t_mutacion/Tiempo.total()*100:.02f}%)")
        print (f"Evaluación: {self.t_evaluator:.08f}({self.t_evaluator/Tiempo.total()*100:.02f}%)")
        
        # <!> Mostramos el individuo solución del genético
        print(poblacion[self.pos_mejor_cromosoma])

        return poblacion[self.pos_mejor_cromosoma].fenotipo, poblacion[self.pos_mejor_cromosoma].fitness, self.evolucion_mejor_media_peor_fitness
    
    # Método que genera la poblacion inicial utilizando el operador creator para 
    # cada individuo a generar: creator.create() -> <individuo>
    # Una poblacion es un array de tantos objetos Solution como individuos tenga la 
    # población (cgf.n_poblacion). 
    
    def __genera_poblacion_inicial(self):    
        poblacion = []
        for i in range(self.cfg.n_poblacion):
            poblacion.append(self.creator.create())

        return poblacion

    # Método que evalua una población, para ello utiliza los operadores:
    # decodificación: decoder.decode(<individuo>) 
    # evaluación: evaluator.evaluate(<individuo>)
    def __evalua_poblacion(self, poblacion):
        for i in range(len(poblacion)):
            self.decoder.decode(poblacion[i]) # genera fenotipo
            self.evaluator.evaluate(poblacion[i]) # genera fitness
   
    # Método que selecciona las parejas de individuos que serán los progenitores de la 
    # siguiente generación: section.apply(<poblacion_actual>) -> <poblacion_progenitores>
    def __seleccion(self, poblacion):
        return self.selection.apply(poblacion)
       
    # Método que, con una cierta probabilidad (cfg.p_cruce), cruza los cromosomas de cada par de 
    # progenitores de las pareja previamente seleccionadas:
    # crossover.apply(<cr_progenitor_1>, <cr_progenitor_2>)-> <cr_descendiente_1>, <cr_descendiente_2>
    # Devuelve la población de descendientes
    def __cruce(self, poblacion):
         # Crear la siguiente generación
        hijos = []
        for i in range(0, len(poblacion), 2):
            # Coger una pareja de padres
            p1, p2 = poblacion[i], poblacion[i+1]
            # Aplicar cruce y mutación a los cromosomas
            for c in self.crossover.apply(p1.genotipo, p2.genotipo):
                hijos.append(Solution(c))
        return hijos

    # Método que, con una cierta probabilidad (cfg.p_mutacion), muta cada individuo de la población
    # de descendientes:
    # mutation.apply(<cr_descendiente>)-> <cr_descendiente_mutado>
    # Devuelve la población de descendientes
    def __mutacion(self, poblacion):
        mutados = []
        for i in range(0, len(poblacion)):
            mutados.append(Solution(self.mutation.apply(poblacion[i].genotipo)))
        return mutados

    # Método que genera una población nueva escogiendo entre los individuos progenitores y descendientes
    # Si el elitismo está activo se incluye el mejor individuo encotrado hasta el momento (élite) a la
    # nueva población:  
    # replacement.apply(<poblacion_progenitores>, <poblacion_descendiente>)-> <nueva_poblacion> 
    def __reemplazamiento(self, poblacion1, poblacion2):
        pob = self.replacement.apply(poblacion1, poblacion2)
        
        if self.cfg.elitismo==True:
            self.__elitismo(pob, poblacion1[self.pos_mejor_cromosoma])
        return pob
    
    # Método que aplica el elitismo, sustituyendo el peor individuo de la población por el individuo élite,
    # siempre y cuando este último sea mejor que el peor de la población
    def __elitismo(self, poblacion, solucion_elite):
        peor_cromosoma, peor_fitness = 0, poblacion[0].fitness
        n_poblacion = len(poblacion)
        # identificamos al peor individuo de la población
        for i in range(n_poblacion):
            if poblacion[i].fitness > peor_fitness:
                peor_cromosoma, peor_fitness = i, poblacion[i].fitness
        # lo sustituimos por el élite si su fitness es peor
        if(poblacion[peor_cromosoma].fitness > solucion_elite.fitness):
            poblacion[peor_cromosoma] = solucion_elite
            


    # Método que inicializa la monitorización de la evolución: reinicia los arrays de mejor, 
    # promedio y peor fitness de cada generación            
    def __init_traza_evolucion(self):
        self.evolucion_mejor_media_peor_fitness = []
        self.pos_mejor_cromosoma = 0
        self.t_creator = 0;
        self.t_evaluator = 0;
        self.t_decoder = 0;
        self.t_selection = 0;
        self.t_replacement = 0;
        self.t_crossover = 0;
        self.t_mutation = 0;

    # Método que actualiza la monitorización de la evolución: registra para la generación especificada
    # cual es el mejor, promedio y peor fitness encontrado. 
    # Además actualiza el individuo élite si es necesario
    def __actualiza_evolucion(self, generacion, poblacion):
        mejor_cromosoma = 0
        mejor_fitness = poblacion[0].fitness
        peor_cromosoma = 0
        peor_fitness = poblacion[0].fitness
        media_fitness=0
        n_poblacion = len(poblacion)
        for i in range(n_poblacion):
            media_fitness+=poblacion[i].fitness
            if poblacion[i].fitness < mejor_fitness:
                mejor_cromosoma, mejor_fitness = i, poblacion[i].fitness
            if poblacion[i].fitness > peor_fitness:
                peor_cromosoma, peor_fitness = i, poblacion[i].fitness           
        media_fitness=media_fitness/n_poblacion
        if self.traza:
            print(">Generacion %d: Peor: %.3f Media: %.3f Mejor: %.3f" % (generacion, peor_fitness, media_fitness, mejor_fitness))

        self.evolucion_mejor_media_peor_fitness.append([mejor_fitness,media_fitness,peor_fitness])
        self.pos_mejor_cromosoma = mejor_cromosoma

