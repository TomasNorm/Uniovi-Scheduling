
% 03_arrays_2d.mzn

int: n = 3; % Tendremos n filas
int: m = 2; % Tendremos m columnas

% Matriz de enteros (n filas x m columnas)
array[1..n,1..m] of int: matriz = [| 1, 2, | 3, 4, | 5, 6|]; 

/*
Las filas se separan mediante |, y también se pone | al principio y al final del array
Se pueden emplear distintas líneas para que sea más cómodo
array[1..n,1..m] of int: matriz = [| 1, 2, 
                                   | 3, 4, 
                                   | 5, 6|]; 
*/

% Variables de decisión
% Matriz (n x m) de variables con dominio 1..6
array[1..n,1..m] of var 1..6: MRes; 


% Restricciones
% El elemento (1,1) de MRes es mayor que el (1,2);
constraint MRes[1,1] > MRes[1,2];

% En la última columna, el primer elemento es menor que el último
constraint MRes[1,m] < MRes[n,m];

% MRes[i,j] es distinto de matriz[i,j] para todo i y j
constraint forall(i in 1..n, j in 1..m)(MRes[i,j] != matriz[i,j]);

% La suma de los elementos de la primera fila es igual 10
constraint sum(j in 1..m)(MRes[1,j]) = 10;

% La suma de los elementos de la primera columna es igual a 12
constraint sum(i in 1..n)(MRes[i,1]) = 12;


% Resolución
solve satisfy;

% Salida
output[show(MRes[i,j]) ++ if j = m then "\n" else " " endif | i in 1..n, j in 1..m];
