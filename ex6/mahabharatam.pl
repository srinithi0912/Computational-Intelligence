% --- Gender Facts ---
male(shantanu). male(vichitravirya). male(bheeshma). male(vyasa).
male(dhritarashtra). male(pandu). male(yudhishtra). male(bheema).
male(arjuna). male(nakula). male(sahadeva). male(duryodhana).
male(dushasana). male(abhimanyu). male(parikshit).

female(ganga). female(satyavati). female(ambika). female(ambalika).
female(gandhari). female(kunti). female(madri).
female(subhadra). female(draupadi). female(uttara).

% --- Parenthood Facts ---
parent(shantanu, bheeshma). parent(ganga, bheeshma). parent(ganga, vichitravirya).
parent(shantanu, vichitravirya). parent(satyavati, vichitravirya).
parent(vichitravirya, dhritarashtra). parent(ambika, dhritarashtra).
parent(vichitravirya, pandu). parent(ambalika, pandu).
parent(dhritarashtra, duryodhana). parent(gandhari, duryodhana).
parent(dhritarashtra, dushasana). parent(gandhari, dushasana).
parent(pandu, yudhishtra). parent(kunti, yudhishtra).
parent(pandu, arjuna). parent(kunti, arjuna).
parent(arjuna, abhimanyu). parent(subhadra, abhimanyu).
parent(abhimanyu, parikshit). parent(uttara, parikshit).

% --- Marriage Facts ---
married(shantanu, ganga). married(shantanu, satyavati).
married(dhritarashtra, gandhari). married(pandu, kunti).
married(pandu, madri). married(arjuna, subhadra).
married(arjuna, draupadi). married(abhimanyu, uttara).

% ==========================================
% RELATIONSHIP RULES
% ==========================================

% 1. Basic Parents & Children
father(F, C) :- male(F), parent(F, C).
mother(M, C) :- female(M), parent(M, C).
son(S, P) :- male(S), parent(P, S).
daughter(D, P) :- female(D), parent(P, D).

% 2. Spouses
wife(W, H) :- female(W), (married(H, W) ; married(W, H)).
husband(H, W) :- male(H), (married(H, W) ; married(W, H)).

% 3. Siblings
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.
brother(B, X) :- male(B), sibling(B, X).
sister(S, X) :- female(S), sibling(S, X).

% 4. Grandparents
grandfather(GF, GC) :- male(GF), parent(GF, X), parent(X, GC).
grandmother(GM, GC) :- female(GM), parent(GM, X), parent(X, GC).

% 5. Uncles and Aunts
uncle(U, N) :- male(U), parent(P, N), sibling(U, P).
uncle(U, N) :- male(U), parent(P, N), sister(S, P), husband(U, S).

aunt(A, N) :- female(A), parent(P, N), sibling(A, P).
aunt(A, N) :- female(A), parent(P, N), brother(B, P), wife(A, B).

% 6. In-Laws
father_in_law(FIL, X) :- male(FIL), (wife(X, S) ; husband(X, S)), father(FIL, S).
mother_in_law(MIL, X) :- female(MIL), (wife(X, S) ; husband(X, S)), mother(MIL, S).

brother_in_law(BIL, X) :- male(BIL), (wife(X, S) ; husband(X, S)), brother(BIL, S).
brother_in_law(BIL, X) :- male(BIL), sister(S, X), husband(BIL, S).

sister_in_law(SIL, X) :- female(SIL), (wife(X, S) ; husband(X, S)), sister(SIL, S).
sister_in_law(SIL, X) :- female(SIL), brother(B, X), wife(SIL, B).
