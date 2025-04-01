import time


### ---------------------------------------------------------------------------
### CLASE PARA MEDIR TIEMPOS
### ---------------------------------------------------------------------------

# La clase Tiempo se comporta como un cronómetro
# Todos sus atributos y métodos como estáticos, así que no es necesario 
# crear objetos, en su lugar se invocan directamente utilizando
# el nombre de la clase: Ej: Tiempo.total()
class Tiempo:

    # Instante en el que se inició el cronómetro
    tiempo_inicio = 0
    # Instante en el que se detuvo el cronómetro
    tiempo_fin = 0
    # indica si el cronómetro está activo
    activo = False

    # método estático que inicia el cronómetro
    @classmethod
    def inicia(cls):
        cls.activo = True
        cls.tiempo_inicio = time.time()
        
    # método estático que finaliza el cronómetro
    @classmethod
    def finaliza(cls):
        if cls.activo:
            cls.tiempo_fin=time.time()         
            cls.activo= False
        else:
            print('Tiempo:No puedes detener un tiempo no iniciado')

    # método estático que devuelve el tiempo actual del cronómetro sin detenerlo 
    # (si el cronómetro está activo)
    @classmethod
    def actual(cls):
        if cls.activo:
            return time.time() - cls.tiempo_inicio
        else:
            return cls.total()
    
    # método estático que devuelve el tiempo total del cronómetro
    @classmethod
    def total(cls):
        if cls.activo:
            raise Exception("<No puedes mostrar un tiempo no finalizado>") 
        else:
            return (cls.tiempo_fin - cls.tiempo_inicio)


