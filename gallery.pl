:- use_module(library(format)).
:- use_module(library(error)).
:- use_module(library(files)).
:- use_module(library(dcgs)).
:- use_module(library(reif)).
:- use_module(library(lists)).
:- use_module(library(clpz)).
:- use_module(library(pairs)).
:- use_module(library(time)).
:- use_module(library(debug)).
:- use_module(library(os)).
:- use_module(library(http/http_server)).
:- use_module(library(charsio)).

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
python -m http.server --cgi
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */

pic_ext       --> "webp"|"jpg"|"png"|"gif"|"jpeg"|"jifi"|"bmp".
pic_file_name --> ...,".", pic_ext.
vid_file_name --> ...,".",("mp4"|"mov").
pic_or_vid    --> pic_file_name | vid_file_name.

phrap(NT, Ls, T) :- 
    (   phrase(NT, Ls) ->
        T = true
    ;   T = false
    ).

%?- tfilter(phrap(pic_file_name), ["foo.webp", "bar.jifi"], Pics).

list_slice(List, Offset, SliceLen, Slice) :- 
    length(Skip, Offset),
    append(Skip, Rest, List),
    length(Rest, RestLen),
    Max #= min(RestLen, SliceLen),
    length(Slice, Max),
    append(Slice, _, Rest).
%?- L = [0,1,2,3,4,5,6,7,8,9], list_slice(L, 3, 10, Slice).
%?- L = [0,1,2,3,4,5,6,7,8,9], list_slice(L, 3, 6, Slice).

directory_slice(Absdir, Offset, Num, Imgs) :- 
    working_directory(_, Absdir),
    directory_files(Absdir, Fs),
    tfilter(phrap(pic_file_name), Fs, Ps),
    list_slice(Ps, Offset, Num, Imgs).

directory_num_images(Absdir, Offset, Num, Imgs) :- 
    working_directory(_, Absdir),
    directory_files(Absdir, Fs),
    tfilter(phrap(pic_file_name), Fs, Ps),
    maplist(file_modification_time, Ps, Ts), % slow
    pairs_keys_values(TPs0, Ts, Ps),
    keysort(TPs0, TPs),
    pairs_values(TPs, Imgs0),
    list_slice(Imgs0, Offset, Num, Imgs).

%?- time(directory_num_images("/home/rainbowtwigs/data/faker_imgs", 10, 5, I)).
%@    % CPU time: 6.345s
%@    I = ["road.png","base.bmp","piece.gif","top.png","side.jpeg ..."]
%@ ;  % CPU time: 0.090s
%@    false.


/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
script
    src "https://unpkg.com/htmx.org@1.7.0"
    integrity "sha384-EzBXYPt0/T6gxNp0nuPtLkmRpmDBbjg6WmCUZRLXBBwYYmwAUxzlSGej0ARHX0Bo"
    crossorigin "anonymous"

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */

tag(T, Body)      --> tag(T, Body, []).
tag(T, Body, AVs) -->
    format_("<~w", [T]),
    attrs(AVs),
    ">", Body,
    format_("</~w>", [T]).

attrs([])             --> [].
attrs([A-[]|AVs])     -->
    " ", A, attrs(AVs).
attrs([A-[V|Vs]|AVs]) -->
    " ", A, "=", "\"", attr_vals([V|Vs]), "\"",
    attrs(AVs).

attr_vals([]) --> [].
attr_vals([V])      --> { must_be(chars, V) }, V.
attr_vals([V,W|Vs]) -->
    { must_be(chars, V) },
    V, " ", attr_vals([W|Vs]).

%?- phrase(tag(a, "click here", []), Html).
%?- phrase(tag(a, "click here", ["foo"-[]]), Html).
%?- phrase(tag(a, "click here", ["href"-["example.com"]]), Html).
%?- phrase(tag(a, "click here", ["class"-["blue", "leave"]]), Html).

format_names([]).
format_names([N|Ns]) :-
    format("~s", [N]),
    format_names(Ns).

img(Path, Tag) :-
    phrase(tag(img, "", ["src"-[Path]]), Tag).

%?- img("ffoo", T).

%?- maplist(img, ["a", "b"], L).
%?- maplist(phrase(img(Path), Tag), ["a", "b"], L).

/* - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   Handle URL parameters
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - */

% XXX: norel, hack: need a library for handling urls
%?- P = "foo=42&bar=n%20m", cgi_query_kvs_decode(P, Kvs).
%@    P = "foo=42&bar=n%20m", Kvs = ["foo"-"42","bar"-"n m"].
cgi_query_kvs_decode(Q, KVs) :-
    chars_utf8bytes(Q, B),
    Hs = ["content-type"-"application/x-www-form-urlencoded"],
    Req = http_request(Hs, binary(B), _),
    http_body(Req, form(KVs)),
    !.

%query_skip_num(Q, S, N) :- false.
%?- K = ["skip"-"42", num="23"], query_skip_num(K, S, N).
%?- K = ["skip"-"42", num="23"], member("skip"-S0, K).

run :-
    format("Content-type: text/html\n\n", []),
    directory_slice("/home/rainbowtwigs/data/faker_imgs", 0, 50, Imgs),
    maplist(append("/data/faker_imgs/"), Imgs, ImgPs),
    maplist(img, ImgPs, ImgTs),
    format_names(ImgTs).
