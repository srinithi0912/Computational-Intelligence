start :-
    write('Enter a value: '), read(A),
    write('Enter b value: '), read(B),
    write('Enter Operation (add/subt/mul/div): '),read(Op),
    calc(A,B,Op).
calc(A,B,add) :-
    Res is A + B, 
    format('Result: ~w + ~w = ~w~n',[A,B,Res]).
calc(A,B,subt) :-
    Res is A - B,
    format('Result: ~w - ~w = ~w~n',[A,B,Res]).
calc(A,B,mul) :-
    Res is A * B,
    format('Result: ~w * ~w = ~w~n',[A,B,Res]).
calc(A,B,div) :-
    (B \= 0 -> Res is A / B,
    format('Result: ~w / ~w = ~w~n',[A,B,Res]);
    write('Error: Cannot divide by Zero.'), n1).
calc(A,B,mod) :-
    ( B =\= 0 ->
        Res is A mod B,
        format('Result: ~w mod ~w = ~w~n',[A,B,Res]);
        write('Error: Cannot perform mod with Zero.'), nl).
calc(A,B,pow) :-
    Res is A ** B,
    format('Result: ~w ^ ~w = ~w~n',[A,B,Res]).
calc(_,_,_) :- 
    write('Invalid Operation Name!!!'),n1.
