import math

class Punto:
    """
    Clase que representa un punto en un plano cartesiano.
    Atributos:
    ----------
    __x : float
        Coordenada x del punto (privada).
    __y : float
        Coordenada y del punto (privada).
    Métodos:
    --------
    __init__(self, x=0, y=0):
        Inicializa un nuevo punto con coordenadas x e y.
    get_x(self):
        Devuelve la coordenada x del punto.
    get_y(self):
        Devuelve la coordenada y del punto.
    set_x(self, x):
        Establece la coordenada x del punto.
    set_y(self, y):
        Establece la coordenada y del punto.
    distancia(punto1, punto2):
        Calcula la distancia euclidiana entre dos puntos.
    __str__(self):
        Devuelve una representación en string del objeto Punto.
    """
    def __init__(self, x=0, y=0):
        # Atributos privados x e y
        self.__x = x
        self.__y = y
    
    # Getters
    def get_x(self):
        return self.__x
    
    def get_y(self):
        return self.__y
    
    # Setters
    def set_x(self, x):
        self.__x = x
    
    def set_y(self, y):
        self.__y = y
    
    # Método estático para calcular la distancia euclidiana entre dos puntos
    @staticmethod
    def distancia(punto1, punto2):
        dx = punto1.get_x() - punto2.get_x()
        dy = punto1.get_y() - punto2.get_y()
        return math.sqrt(dx**2 + dy**2)
    
    # Representación en string del objeto (opcional)
    def __str__(self):
        return f"Punto({self.__x}, {self.__y})"


def main():
    # Separador para mejorar la lectura en consola
    def separador(titulo):
        print("\n" + "=" * 50)
        print(f" {titulo} ".center(50, "="))
        print("=" * 50)
    
    # Prueba de la clase Punto
    separador("PRUEBAS DE LA CLASE PUNTO")
    
    # Crear puntos
    p1 = Punto(3, 4)
    p2 = Punto(7, 1)
    
    print(f"Punto 1: {p1}")
    print(f"Punto 2: {p2}")
    
    # Probar getters
    print(f"Coordenadas de p1: ({p1.get_x()}, {p1.get_y()})")
    
    # Probar setters
    p1.set_x(5)
    p1.set_y(6)
    print(f"Punto 1 después de modificar: {p1}")
    
    # Probar método estático de distancia
    distancia = Punto.distancia(p1, p2)
    print(f"Distancia entre p1 y p2: {distancia:.2f}")
    


# Ejecutar la función main si este archivo se ejecuta directamente
if __name__ == "__main__":
    main()