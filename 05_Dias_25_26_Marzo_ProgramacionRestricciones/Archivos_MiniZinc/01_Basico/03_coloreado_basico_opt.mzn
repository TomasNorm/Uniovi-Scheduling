% 03_coloreado_basico_opt.mzn

% Parámetros / Datos
int: n = 5;  % tenemos n=5 vértices

set of int: COLORES = 1..n; % n colores posibles

% Variables de decisión
var COLORES: A;
var COLORES: B;
var COLORES: C;
var COLORES: D;
var COLORES: E;

% Restricciones
constraint A != B;
constraint A != C;
constraint A != E;
constraint B != C;
constraint B != D;
constraint B != E;
constraint C != E;
constraint D != E;


% Resolución
solve minimize max([A,B,C,D,E]);
