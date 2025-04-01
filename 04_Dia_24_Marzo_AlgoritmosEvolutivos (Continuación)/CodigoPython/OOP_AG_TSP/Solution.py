
### ---------------------------------------------------------------------------
### CLASE SOLUTION
### ---------------------------------------------------------------------------

class Solution:

    # genotipo: genotipo de la solucion, su cromosoma. La estructura del cromosoma 
    #           dependerá del problema y la representacion escogida para las variables 
    #           de la solución (los genes)
    # fenotipo: fenotipo de la solución (solucion decodificada)
    # fitness: fitness de la solución (un número real) 
    
    def __init__(self, genotipo = None, fenotipo = None, fitness = None):
        self.genotipo = genotipo
        self.fenotipo = fenotipo
        self.fitness = fitness

    def __str__(self) -> str:
        return "gen: " + str(self.genotipo) + "\n fen: " + str(self.fenotipo) + "\n fitness: " + str(self.fitness)
    
