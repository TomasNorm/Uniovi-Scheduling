import math

from Punto import Punto
from Circulo import Circulo


class CirculoConCentro(Circulo):
    """
    Clase que representa un círculo con un centro definido.
    Atributos:
    -----------
    __centro : Punto
        El centro del círculo.
    __radio : float
        El radio del círculo (heredado de la clase Circulo).
    Métodos:
    --------
    __init__(self, centro=None, radio=0):
        Inicializa un nuevo círculo con un centro y un radio dados.
    get_centro(self):
        Devuelve el centro del círculo.
    set_centro(self, centro):
        Establece el centro del círculo.
    distancia_entre_centros(self, otro_circulo):
        Calcula la distancia entre los centros de dos círculos.
    contiene_punto(self, punto):
        Verifica si un punto dado está dentro del círculo.
    intersecta_con(self, otro_circulo):
        Verifica si dos círculos se intersectan.
    __str__(self):
        Devuelve una representación en cadena del círculo.
    """
    def __init__(self, centro=None, radio=0):
        # Llamar al constructor de la clase padre
        super().__init__(radio)
        
        # Si no se proporciona un centro, crear uno en el origen
        if centro is None:
            self.__centro = Punto(0, 0)
        else:
            self.__centro = centro
    
    # Getter para el centro
    def get_centro(self):
        return self.__centro
    
    # Setter para el centro
    def set_centro(self, centro):
        self.__centro = centro
    
    # Método para calcular la distancia entre los centros de dos círculos
    def distancia_entre_centros(self, otro_circulo):
        return Punto.distancia(self.__centro, otro_circulo.get_centro())
    
    # Método para verificar si un punto está dentro del círculo
    def contiene_punto(self, punto):
        distancia = Punto.distancia(self.__centro, punto)
        return distancia <= self.get_radio()
    
    # Método para verificar si dos círculos se intersectan
    def intersecta_con(self, otro_circulo):
        distancia_centros = self.distancia_entre_centros(otro_circulo)
        suma_radios = self.get_radio() + otro_circulo.get_radio()
        return distancia_centros < suma_radios
    
    # Sobrescribir el método __str__
    def __str__(self):
        return f"Círculo con centro en {self.__centro} y radio {self.get_radio()}"


def main():
    # Separador para mejorar la lectura en consola
    def separador(titulo):
        print("\n" + "=" * 50)
        print(f" {titulo} ".center(50, "="))
        print("=" * 50)
    

    # Prueba de la clase CirculoConCentro
    separador("PRUEBAS DE LA CLASE CIRCULOCONCENTRO")
    
    # Crear puntos para los centros
    centro1 = Punto(0, 0)
    centro2 = Punto(8, 0)
    
    # Crear círculos con centro
    cc1 = CirculoConCentro(centro1, 4)
    cc2 = CirculoConCentro(centro2, 3)
    cc3 = CirculoConCentro(Punto(3, 0), 2)  # Círculo que intersecta con cc1
    
    print(f"Círculo con centro cc1: {cc1}")
    print(f"Círculo con centro cc2: {cc2}")
    print(f"Círculo con centro cc3: {cc3}")
    
    # Probar herencia (métodos de Circulo)
    print(f"Área de cc1: {cc1.area():.2f}")
    print(f"Perímetro de cc1: {cc1.perimetro():.2f}")
    
    # Probar métodos específicos de CirculoConCentro
    distancia_centros = cc1.distancia_entre_centros(cc2)
    print(f"Distancia entre centros de cc1 y cc2: {distancia_centros:.2f}")
    
    # Probar si los círculos se intersectan
    print(f"¿cc1 intersecta con cc2? {cc1.intersecta_con(cc2)}")
    print(f"¿cc1 intersecta con cc3? {cc1.intersecta_con(cc3)}")
    
    # Probar si un punto está dentro del círculo
    punto_test1 = Punto(2, 2)
    punto_test2 = Punto(10, 10)
    
    print(f"¿El punto {punto_test1} está dentro de cc1? {cc1.contiene_punto(punto_test1)}")
    print(f"¿El punto {punto_test2} está dentro de cc1? {cc1.contiene_punto(punto_test2)}")
    
    # Probar cambio de centro
    nuevo_centro = Punto(5, 5)
    cc1.set_centro(nuevo_centro)
    print(f"cc1 después de cambiar el centro: {cc1}")


# Ejecutar la función main si este archivo se ejecuta directamente
if __name__ == "__main__":
    main()