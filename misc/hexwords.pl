
:- use_module(library(dcgs)).
:- use_module(library(lists)).
:- use_module(library(dif)).

hex --> "a"|"b"|"c"|"d"|"e"|"f".
l --> "1".

%?- phr[ase(l


% substitution: point mutation where an element A has been changed to B

substitution(_, _, [], []).
substitution(A, B, [A|T0], [B|T]) :- substitution(A, B, T0, T).
substitution(A, B, [C|T0], [C|T]) :- dif(A, C), substitution(A, B, T0, T).


%?- phrase(substitution("l", "1"), "laelia", Result).
% substitution(a, b, "abacadaba", O).