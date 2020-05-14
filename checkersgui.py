#!/usr/bin/python
from tkinter import *
from checkers import *
""" for testing """
import time

""" global variables """
root = None
buttons = []
frames = []
count = 0
player = ""
result = None
loc = (0,0)
des = (0,0)
move = ( (0,0) , (0,0) ) 
aimove = ( (0,0) , (0,0) ) 
firstclick = True
ckrs = checkers()
curState = ckrs.initial
lastState = None

def create_frames(root):
    """ This function creates the necessary structure of the game """
    """ creates frames for the each row of buttons """
    frame = [None] * 8
    for i in range(8):
        frame[i] = Frame(root)
        create_buttons(frame[i])
    for i in range(8):
        frame[7-i].pack(side=BOTTOM)
    for i in range(8):
        frames.append(frame[i])
    
    """ appends buttons to frames """
    for x in frames:
        buttons_in_frame = []
        for y in x.winfo_children():
            buttons_in_frame.append(y)
        buttons.append(buttons_in_frame)

    """creates control frame for exiting game or reset """
    controlframe = Frame(root)
    buttonReset = Button(controlframe, height=1, width=2, text="Reset", command=lambda: reset_game())
    buttonReset.pack(side=LEFT)
    buttonExit = Button(controlframe, height=1, width=2, text="Exit", command=lambda: exit_game(root))
    buttonExit.pack(side=LEFT)
    controlframe.pack(side=BOTTOM)
    frames.append(controlframe)


def create_buttons(frame):
    """ This function creates the buttons to be pressed/clicked during the game. """
    button1 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button1))
    button1.pack(side=LEFT)
    button2 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button2))
    button2.pack(side=LEFT)
    button3 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button3))
    button3.pack(side=LEFT)
    button4 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button4))
    button4.pack(side=LEFT)
    button5 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button5))
    button5.pack(side=LEFT)
    button6 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button6))
    button6.pack(side=LEFT)
    button7 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button7))
    button7.pack(side=LEFT)
    button8 = Button(frame, height=2, width=2, text=" ", command=lambda: on_click(button8))
    button8.pack(side=LEFT)


def draw_board(state):
    """ draws board on to the buttons """
    global buttons, ckrs
    board = state.board
    for i in range(len(buttons)):
        for k in range(len(buttons[i])):
            #print(i, k)
            button = buttons[i][k]
            if( board[i][k] == "_" ):
                tex = " "# + str(k) + "," + str(i)
                button.config(text=tex)
            else:
                tex = board[i][k]# + str(k) + "," + str(i)
                button.config(text=tex)
            if( board[i][k] == "#"):
                button.config(text = " ", bg="black", state="disabled")
    """ writes it to console """ 
    ckrs.printboard(board)


def on_click(button):
    """ This function handles action of getting a player move and ai move as well as 
        updates board after move. Pretty cool right?!!??!?!"""
    global ckrs, move, count, player, result, loc, des, firstclick, curState, aimove, lastState

    x, y = get_coordinates(button)
    board = curState.board
    if( board[y][x].lower() == 'b' ):
        firstclick = False
        loc = (x, y)
    else:
        des = (x, y)
        move = (loc, des)
        print("player move:", move)
        player = 'w'
        firstclick = True

    if (firstclick and move in curState.moves):
        curState = copy.deepcopy( ckrs.result(curState, move) )
        #check for winner 
        get_winner(curState)
        if( player == 'w' or curState != lastState ):
            player = 'b'
            count += 1 
            """ AI algo here, change the algo here """
            aimove = alpha_beta_cutoff_search(state=curState, game=ckrs, d=2, cutoff_test=None, eval_fn= ckrs.evaluation_function )
            """set the state based on move """
            print(curState.to_move, curState.moves)
            print("aimove:", aimove)
            curState = copy.deepcopy( ckrs.result(curState, aimove) )
            #check for winner
            get_winner(curState)
            lastState = curState
        #need to change firstclick back to true
        print(curState.to_move, curState.moves)
        firstclick = True


def get_winner(state):
    """ function gets the winner and set the result string """ 
    global count
    draw_board(state)
    if(state.utility == -1):
        result.set("WINNER: HUMAN")
        disable_game()
    elif(state.utility == 1 ):
        result.set("WINNER: AI")
        disable_game()
    else:
        print("\n *** " + state.to_move + " TURN *** ")
        result.set(state.to_move + " turn! With " + str(count) + " turns.")


def get_coordinates(button):
    """ This function returns the coordinates of the button clicked. """
    global buttons
    for x in range(len(buttons)):
        for y in range(len(buttons[x])):
            if buttons[x][y] == button:
                return y, x


def reset_game():
    """ This function will reset all the tiles to the initial null value. """
    global count, player, result, loc, des, move, aimove, firstclick, ckrs, curState, lastState, frames
    count = 0
    player = ""
    loc = (0,0)
    des = (0,0)
    move = ( (0,0) , (0,0) ) 
    aimove = ( (0,0) , (0,0) ) 
    firstclick = True
    curState = ckrs.initial
    lastState = None
    draw_board(curState)
    result.set("Your Turn!")
    for x in frames[0:8]:
        for y in x.winfo_children():
            y.config(state='normal')


def disable_game():
    """ This function deactivates the game after a win, loss or draw. """
    global frames
    for x in frames[0:8]:
        for y in x.winfo_children():
            y.config(state='disabled')


def exit_game(root):
    """ This function will exit the game by killing the root. """
    root.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("checkers")
    root.geometry("400x450")  # Improved the window geometry
    #root.resizable(0, 0)  # To remove the maximize window option
    result = StringVar()
    result.set("Your Turn!")
    w = Label(root, textvariable=result)
    w.pack(side=BOTTOM)
    create_frames(root)
    #init stuff
    draw_board(curState)
    print("\n *** b TURN *** ")
    print(curState.to_move, curState.moves)

    root.mainloop()


#extracode
""" timing stuff
start=time.time()
end=time.time()
print(end-start)
"""
""" mcts_player works but slow"""
#aimove = mcts_player(ckrs, curState)
""" alpha_beta_cutoff_search testing """
#aimove = alpha_beta_cutoff_search(state=curState, game=ckrs, d=6, cutoff_test=None, eval_fn=ckrs.evaluation_function)
""" alpha_beta_player or min_max doesn't work because of recursive deep limit """
#aimove = alpha_beta_player(ckrs, curState)
#aimove = expect_min_max_player(ckrs, curState)
