:- use_module(library(random)).
:- use_module(library(clpz)).
:- use_module(library(lists)).
:- use_module(library(debug)).
:- use_module(library(dcgs)).



init_population(Size, Population) :-
    length(Population, Size),
    maplist(init_chromosome, Population).

init_chromosome(Seed, Chromosome) :-
    set_random(seed(Seed)),
    length(Chromosome, 10),
    maplist(random_gene, Chromosome).

random_gene(Gene) :-
    random_integer(0, 10, Gene).

%?- random_gene(23, G).
%?- init_chromosome(23, C).
%@    C = [1,4,4,2,1,8,4,4,2,1].

kexpr(Term) --> function(Term).
kexpr(Term) --> terminal(Term).

function(FuncTerm) --> ["+"], { FuncTerm =.. ['+', A, B] }, kexpr(A), kexpr(B).
function(FuncTerm) --> ["*"], { FuncTerm =.. ['*', A, B] }, kexpr(A), kexpr(B).
function(FuncTerm) --> ["sin"], { FuncTerm =.. ['sin', A] }, kexpr(A).

terminal(a) --> ["a"].
terminal(b) --> ["b"].

eval_expr(a, 1).
eval_expr(b, 2).
eval_expr(+(A, B), Result) :- eval_expr(A, RA), eval_expr(B, RB), Result is RA + RB.
eval_expr(*(A, B), Result) :- eval_expr(A, RA), eval_expr(B, RB), Result is RA * RB.
eval_expr(sin(A), Result) :- eval_expr(A, RA), Result is sin(RA).

%?- phrase("+*abab", Term)

, eval_expr(Term, Result).
%@    false.
