% 01_primer_ejemplo.mzn

% Parámetros / Datos
int: n = 4;  % n es un entero
 
set of int: Dx = 1..n;    % Dx es el conjunto {1,...,n}
set of int: Dy = {2,3,5}; % Dy es el conjunto {2,3,5}

% Variables de decisión
var Dx: x;     % x es una variable con dominio {1,...,n}
%var 1..n: x:  % alternativa
var Dy: y;     % y es una variable con dominio {2,3,5} 
var {1,4}: z;  % z es una variable con dominio {1,4}

% Restricciones
constraint x != y;
constraint x >= y * z;
%constraint x < y-z; 	% restricción extra

% Resolución
solve satisfy;
%solve minimize x+y;
%solve maximize x+y;
