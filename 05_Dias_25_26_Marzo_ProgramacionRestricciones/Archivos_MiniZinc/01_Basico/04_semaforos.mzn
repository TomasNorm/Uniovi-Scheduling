% 04_semaforos.mzn

% Parámetros / Datos
enum COLOR = {verde, rojo, ambar}; % tres colores

% Variables de decisión
var COLOR: S1;  % S1: color del primer semáforo
var COLOR: S2;  % S2: color del segundo semáforo
var COLOR: S3;  % S2: color del segundo semáforo


% Restricciones
% S1 está en verde o S3 está en rojo (o ambas cosas)
constraint S1 = verde \/ S3 = rojo;

% No es posible que S1 y S2 estén en rojo al mismo tiempo
constraint not(S1 = rojo /\ S2 = rojo);

% Si S2 está en verde, entonces S3 está en rojo
constraint S2 = verde -> S3 = rojo;

% S1 está en ámbar si y solo si S2 está en verde
constraint S1 = ambar <-> S2 = verde;


%Resolución
solve satisfy;