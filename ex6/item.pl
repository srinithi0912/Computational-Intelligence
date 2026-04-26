:- dynamic item/3.

% Add item with Price
add_item :-
    write('Enter item name: '),
    read(Name),
    write('Enter item Price: '),
    read(Price),
    write('Enter item Quantity: '),
    read(Qty),
    assertz(item(Name,Price,Qty)),
    write('Item added successfully!'), nl.

%display all items
show_items :-
    item(Name,Price,Qty),
    write('Item: '),write(Name),
    write(' Price: '),write(Price),
    write(' Quantity: '),write(Qty), nl,
    fail.
show_items.

% order items
order :-
    write('Enter item Name: '),
    read(Name),
    item(Name,Price,AvaQty),
    write('Enter Quantity: '),
    read(Qty),
    ( Qty =< AvaQty ->
      Cost is Price * Qty,
      NewQty is AvaQty - Qty,

      retract(item(Name,Price,AvaQty)),
      assertz(item(Name,Price,NewQty)),

      write('Cost for the '),write(Name),write(' : '),write(Cost), nl,
      more_order(Cost)
      ;
      write('Quantity exceeds available Stock ( '),write(AvaQty),write(' )'), nl
    ).

% If item not found
order :-
    write('Item not found!'), nl.

reset_items :-
    retractall(item(_,_,_)),
    write('All items cleared!'), nl.

more_order(Acc) :-
    write('Do you want to purchase items?(yes/no): '),
    read(Ans),
    (Ans == yes ->
       write('Enter item Name: '),
       read(Name),
       item(Name,Price,AvaQty),
       write('Enter item Quantity: '),
       read(Qty),
       ( Qty =< AvaQty ->
          Cost is Price * Qty,
          NewQty is AvaQty - Qty,

          retract(item(Name,Price,AvaQty)),
          assertz(item(Name,Price,NewQty)),

          NewAcc is Acc + Cost,
          write('Cost for this '),write(Name),write(' : '),write(Cost), nl,
          more_order(NewAcc)
          ;
          write('Quantity exceeds available Quantity ( '),write(AvaQty),write(' )'), nl,
          more_order(Acc)
       )
       ;
       write('Total Bill: '), write(Acc), nl    
    ).
