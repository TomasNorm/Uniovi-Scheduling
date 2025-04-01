% 05_menu.mzn

% Parámetros / Datos
% Un tipo enumerado para cada plato (ENTRANTES, PRINCIPALES, POSTRES)
enum ENTRANTES = {calamares, croquetas, ensalada};
enum PRINCIPALES = {entrecot, lubina, menestra};
enum POSTRES = {fruta, helado};


% Variables de decisión
var ENTRANTES: Entrante;     % Entrante será uno de los entrantes
var PRINCIPALES: Principal;  % Principal será un plato principal
var POSTRES: Postre;         % Postre será uno de los postres


% Restricciones
% El entrante es croquetas o el postre helado (o las dos cosas)

% Si el entrante es ensalada, el plato principal es lubina

% Si el entrante es croquetas, el plato principal es entrecot o menestra

% El postre es helado si y solo si el plato principal es entrecot

% No puede ser que el entrante sea calamares y el plato principal entrecot


% Resolución
solve satisfy;

