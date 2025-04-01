% 01_cuadrado_latino.mzn

% Parámetros / Datos
int: n = 3;  % el cuadrado será de nxn


% Variables de decisión
% Matriz de nxn variables con dominio 1..n
array[1..n,1..n] of var 1..n: Cuadrado; 


% Restricciones
% En cada fila, los valores son distintos dos a dos
constraint forall(i in 1..n)(
                  forall(j1,j2 in 1..n where j1 < j2)(
                        Cuadrado[i,j1] != Cuadrado[i,j2]
                  )
            );
            
% En cada columna, los valores son distintos dos a dos
constraint forall(j in 1..n)(
                  forall(i1,i2 in 1..n where i1 < i2)(
                        Cuadrado[i1,j] != Cuadrado[i2,j]
                  )
            );


% Resolución
solve satisfy;

% Salida
output[show(Cuadrado[i,j]) ++ if j = n then "\n" else " " endif| i,j in 1..n];

