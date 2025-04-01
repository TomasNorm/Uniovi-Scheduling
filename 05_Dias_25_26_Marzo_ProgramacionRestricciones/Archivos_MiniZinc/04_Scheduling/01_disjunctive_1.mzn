% 01_disjunctive_1.mzn

% H: Horizonte de planificación
int: H = 250;

% pi: Duración de la tarea i
int: pA = 25;
int: pB = 22;
int: pC = 50;
int: pD = 37;
int: pE = 13;
int: pF = 20;
int: pG = 45;

% starti: Tiempo de inicio de la tarea i
var 0..H-pA: startA;
var 0..H-pB: startB;
var 0..H-pC: startC;
var 0..H-pD: startD;
var 0..H-pE: startE;
var 0..H-pF: startF;
var 0..H-pG: startG;

% Tenemos 2 recursos unarios, M1 y M2

%  - Las tareas C, D y G necesitan hacer uso de M1 durante su ejecución
constraint startC + pC <= startD \/ startD + pD <= startC;
constraint startD + pD <= startG \/ startG + pG <= startD;
constraint startC + pC <= startG \/ startG + pG <= startC;

%  - Las tareas A, B, E y F necesitan hacer uso de M2 durante su ejecución
% COMPLETAR

% CSP
solve satisfy;
