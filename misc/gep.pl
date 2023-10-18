:- use_module(library(random)).
:- use_module(library(clpz)).
:- use_module(library(lists)).
:- use_module(library(debug)).



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
%?- init_chromosome(23, C)
