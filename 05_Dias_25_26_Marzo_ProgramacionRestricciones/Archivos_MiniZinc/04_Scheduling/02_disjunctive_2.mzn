% 02_disjunctive_2.mzn

include "disjunctive.mzn";

% H: Horizonte de planificación
int: H;

% n_tareas: Número de tareas
int: n_tareas;

% n_recursos: Número de recursos
int: n_recursos;

% p: Array de duraciones
array[1..n_tareas] of int: p;

% r: Array de recursos requeridos por cada tarea
array[1..n_tareas] of int: r;

% start: array de variables de decisión start
array[1..n_tareas] of var 0..H: start;

% end: array de variables de decisión end
array[1..n_tareas] of var 0..H: end;

% Hay que relacionar start y end (start[i] + p[i] = end[i])
constraint forall(i in 1..n_tareas)(start[i] + p[i] = end[i]);

% Tan solo puede haber una tarea de cada recurso ejecutándose en cada momento
% COMPLETAR

% Objetivo: minimización del makespan
solve minimize max(i in 1..n_tareas)(start[i]+p[i]);
