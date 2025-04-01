import math

class Circulo:
    """
    Clase que representa un círculo.
    Atributos:
    ----------
    __radio : float
        Radio del círculo (atributo privado).
    Métodos:
    --------
    __init__(self, radio=0):
        Inicializa un objeto Circulo con un radio dado (por defecto 0).
    get_radio(self):
        Devuelve el valor del radio del círculo.
    set_radio(self, radio):
        Establece el valor del radio del círculo. Lanza una excepción si el radio es negativo.
    perimetro(self):
        Calcula y devuelve el perímetro (circunferencia) del círculo.
    area(self):
        Calcula y devuelve el área del círculo.
    __str__(self):
        Devuelve una representación en cadena del objeto Circulo.
    """
    def __init__(self, radio=0):
        # Atributo privado radio (se usa el prefijo __ para indicar que es privado)
        self.__radio = radio
    
    # Método getter para el radio
    def get_radio(self):
        return self.__radio
    
    # Método setter para el radio
    def set_radio(self, radio):
        if radio < 0:
            raise ValueError("El radio no puede ser negativo")
        self.__radio = radio
    
    # Método para calcular el perímetro (circunferencia)
    def perimetro(self):
        return 2 * math.pi * self.__radio
    
    # Método para calcular el área
    def area(self):
        return math.pi * self.__radio ** 2
    
    # Representación en string del objeto (opcional)
    def __str__(self):
        return f"Círculo de radio {self.__radio}"


def main():
    # Separador para mejorar la lectura en consola
    def separador(titulo):
        print("\n" + "=" * 50)
        print(f" {titulo} ".center(50, "="))
        print("=" * 50)
    
    
    # Prueba de la clase Circulo
    separador("PRUEBAS DE LA CLASE CIRCULO")
    
    # Crear círculos
    c1 = Circulo(5)
    print(f"Círculo c1: {c1}")
    
    # Probar getters
    print(f"Radio de c1: {c1.get_radio()}")
    
    # Probar métodos de área y perímetro
    print(f"Perímetro de c1: {c1.perimetro():.2f}")
    print(f"Área de c1: {c1.area():.2f}")
    
    # Probar setters
    c1.set_radio(7)
    print(f"Círculo c1 después de modificar el radio: {c1}")
    print(f"Nuevo perímetro: {c1.perimetro():.2f}")
    print(f"Nueva área: {c1.area():.2f}")
    
    # Probar validación
    try:
        c1.set_radio(-3)
    except ValueError as e:
        print(f"Error capturado correctamente: {e}")
    

# Ejecutar la función main si este archivo se ejecuta directamente
if __name__ == "__main__":
    main()