% 02_cuadrado_latino_alldifferent.mzn

include "alldifferent.mzn"; % incluimos alldifferent.mzn

% Parámetros / Datos
int: n = 3;  % el cuadrado será de nxn


% Variables de decisión
% Matriz de nxn variables con dominio 1..n
array[1..n,1..n] of var 1..n: Cuadrado; 


% Restricciones
% En cada fila, los valores son distintos dos a dos
            
% En cada columna, los valores son distintos dos a dos


% Resolución
solve satisfy;

% Salida
output[show(Cuadrado[i,j]) ++ if j = n then "\n" else " " endif| i,j in 1..n];