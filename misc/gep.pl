:- use_module(library(random)).
:- use_module(library(clpz)).
:- use_module(library(lists)).
:- use_module(library(debug)).

gep_base(plus).
gep_base(minus).
gep_base(sqrt).
gep_base(times).

gep_base_arity(plus, 2).
gep_base_arity(minus, 2).
gep_base_arity(sqrt, 1).
gep_base_arity(times, 2).


% head_body(H, []).
% head_body(H, [C|Cs]).

% wrap in once to remove choice point
list_n_sample(Seed, Xs, N, S) :-
	set_random(seed(Seed)),
	list_n_sample_(Xs, N, S).

list_n_sample_(_, 0, []).
list_n_sample_([], _, []).
list_n_sample_(Xs, N0, [S|Ts]) :-
	#N0 #> 0,
	length(Xs, Len),
	random_integer(0, Len, R),
	nth0(R, Xs, S),
	N #= #N0 - 1,
	list_n_sample_(Xs, N, Ts).

