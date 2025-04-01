% 02_mochila_0-1.mzn

% Parámetros / Datos
int: n = 4;  % número de objetos
int: W = 20; % capacidad máxima de la mochila
array[1..n] of int: peso = [8,4,10,7];   % peso de los objetos
array[1..n] of int: valor = [10,8,12,9]; % valor de los objetos

% Variables de decisión
% ValorTotal (función objetivo)
% Dominio: desde 0 a una cota superior del valor óptimo
var 0..sum(valor): ValorTotal; % (observar dominio)

% Añadir array de variables con dominio 0..1 (una para cada objeto)
% Llamarlo Sel


% Restricciones
% El peso total de los objetos seleccionados no excede la capacidad máxima


% ValorTotal es la suma del valor de los objetos seleccionados


% Resolución: maximizar ValorTotal


output["Seleccion: " ++ show(Sel) ++ "\n" ++
       "Valor total: "++ show(ValorTotal)];
