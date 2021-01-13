import random
from tkinter import *
from tkinter import messagebox

#random.seed(0)

#initialization
x = "X"
o = "O"
_ = " "
lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
rows = [[0, 3, 6], [1, 4, 7], [2, 5, 8]]
diagonals = [[0, 4, 8], [2, 4, 6]]
wins = (lines + rows + diagonals)

def new_game():
    global board
    global i
    board = list(_ * 9)
    i = -1
    show_board(board)

#to printing, (not tkinter)
def print_board(board):
    print("-+-+-")
    for i in range(0,3):
        print("|".join(board[i*3:(i+1)*3]))
        print("-+-+-")


def show_board(board):
    for i in range(0, 9):
        b[i].config(text = board[i])

def list_of_empty_corner (board):
    return list(filter(lambda x: board[x] == _, [0, 2, 6, 8]))

def first_turn(board):
    if board[4] == x:
        return random.choice(list_of_empty_corner (board))
    else:
        return 4

"אולי לעיגול לא יוצא אף פעם מצב כזה"
def fork(board):
    for line in lines:
        for row_or_diagonal in (rows + diagonals):
            Intersection_point = next(iter(set(line).intersection(set(row_or_diagonal))))
            if board[Intersection_point] == {_} and line.count(o) == 1 and row_or_diagonal.count(o) == 1 and line.count(_) == 2 and row_or_diagonal.count(_) == 2:
                return next(iter(set(line).intersection(set(row_or_diagonal))))
    for row in rows:
        for diagonal in (diagonals):
            Intersection_point = next(iter(set(row).intersection(set(diagonal))))
            if board[Intersection_point] == _ and row.count(o) == 1 and diagonal.count(o) == 1 and row.count(_) == 2 and diagonal.count(_) == 2:
                return next(iter(set(row).intersection(set(diagonal))))
    return None

def win_or_block(board):
    list_of_wins_xo = []
    for win in wins:
        win_xo = "".join([board[a] for a in win])
        list_of_wins_xo.append(win_xo)
    for index, win in enumerate(list_of_wins_xo):
        if win.count(o) == 2 and win.count(_) == 1:
            return wins[index][win.index(_)]
    for index, win in enumerate(list_of_wins_xo):
        if win.count(x) == 2 and win.count(_) == 1:
            return wins[index][win.index(_)]
    return None

assert win_or_block([x, x, o, _, x, _, _, _, o]) == 5
assert win_or_block([_, x, x, x, x, o, o, _, o]) == 7
assert win_or_block([x, _, o, _, x, _, x, _, o]) == 5
assert win_or_block([x, _, x, _, x, _, o, _, o]) == 7
assert win_or_block([x, _, x, x, o, x, o, _, o]) == 7

def Blocking_fork (board):
    options = list_of_empty_corner(board)
    forks = [(3,1,8), (1,5,6), (7,5,0), (3,7,2), (0,7,2), (2,3,8), (8,1,6), (6,5,0)]
    for b0,b1,loc in forks:
        if board[b0] == x and board[b1] == x and loc in options:
            options.remove(loc)
    if not options:
        return None
    return random.choice(options)

def else_ (board):
    if list_of_empty_corner(board) != []:
        return random.choice(list_of_empty_corner(board))
    else:
        return random.choice([i for i,b in enumerate(board) if b == _])

"יכול להיות שצריך לשנות את המיקום של פורק "
def computer_player (board):
    if win_or_block(board) != None:
        return win_or_block(board)
    elif board.count(x) == 1:
        return first_turn(board)
    elif fork(board) != None:
        return fork(board)
    elif (board[0] == x and board[8] == x) or (board[2] == x and board[6] == x):
        return random.choice([1, 3, 5, 7])
    elif Blocking_fork(board) != None:
        return Blocking_fork(board)
    else:
        return else_ (board)

def resolt_who_win(board):
    a = None
    for win in wins:
        if board[int(win[0])]==board[int(win[1])]==board[int(win[2])]=='O':
            a = ("The O has won!")
        elif board[int(win[0])]==board[int(win[1])]==board[int(win[2])]=='X':
            a = ("The X has won!")
        elif board.count(_) == 0:
            a = ("Tie")
    if a == None:
        return None
    messagebox.showinfo("showinfo" , a)
    new_game()
    return ""

def is_not_standard(board, numbutton):
    try:
        if board[numbutton] != _:
            raise ValueError
    except ValueError:
        raise ValueError("This Checker has already been marked.")

def one_turn (board, i,user_chosen):
    board[int(user_chosen)] = x
    show_board(board)
    if resolt_who_win(board) != None:
        return
    board[computer_player(board)] = o
    show_board(board)
    if resolt_who_win(board) != None:
        return

#to printing, (not tkinter)
def main(board):
     for i in range(5):
         user_chosen = input("")
         if is_not_standard(board, user_chosen) != None:
                print(is_not_standard(board, user_chosen))
                return
         one_turn(board, i, user_chosen)
         if resolt_who_win(board) != None:
             return resolt_who_win
#main(board)


master = Tk()
window = Canvas(master, width=100, height=100)
master.title('Tic-Tac-Toe')

i = 0

def userplay(numbutton):
    global i
    global board
    is_not_standard(board, numbutton)
    one_turn(board, i, numbutton)
    i=i+1
    return

b = []
for row in range(0,3):
    for column in range(0,3):
        b.append(Button(window, text=_, command=lambda rc=(row, column): userplay(rc[0] * 3 + rc[1])))
        b[-1].grid(row = row, column = column)

new_game()
window.pack()
mainloop()