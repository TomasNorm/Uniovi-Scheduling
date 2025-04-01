% 01_arrays_ejemplo.mzn

% Parámetros / Datos
int: n = 5;  % Tendremos 5 elementos

% array de n enteros
% se indexa desde 1: a[1], a[2],..., a[n]
array[1..n] of int: a = [5, 12, 8, 9, 10];


% Variables de decisión
% array de variables de decisión con dominios {0,...,25}
array[1..n] of var 0..25: Res;


% Restricciones
% El primer elemento de Res debe ser mayor que el último
constraint Res[1] > Res[n];

% La suma de los elementos 2 y 3 debe ser igual al penúltimo
constraint Res[2] + Res[3] = Res[n-1];

% Res[i] debe ser mayor o igual que a[i], para todo i
constraint forall(i in 1..n)(Res[i] >= a[i]);

% Todos los elementos deben ser diferentes entre sí
constraint forall(i,j in 1..n where i < j)(Res[i] != Res[j]);

% Resolución
solve satisfy;

% Descomentar para ver el efecto
% output["Resultado: " ++ show(Res)];