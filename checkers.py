#!/usr/bin/python
from games4e import *
import copy
import sys
#sys.setrecursionlimit(10000) # changing the recursion limit for the system


class checkers(Game):


    def __init__(self):
        #"""#full game board
        board = [
        ['#','b','#','b','#','b','#','b'],
        ['b','#','b','#','b','#','b','#'],
        ['#','b','#','b','#','b','#','b'],
        ['_','#','_','#','_','#','_','#'],
        ['#','_','#','_','#','_','#','_'],
        ['w','#','w','#','w','#','w','#'],
        ['#','w','#','w','#','w','#','w'],
        ['w','#','w','#','w','#','w','#'] ]
        """#test board
        board = [
        ['#','_','#','_','#','_','#','_'],
        ['_','#','_','#','_','#','_','#'],
        ['#','_','#','_','#','_','#','_'],
        ['_','#','b','#','_','#','_','#'],
        ['#','_','#','_','#','_','#','_'],
        ['_','#','_','#','w','#','_','#'],
        ['#','_','#','_','#','_','#','_'],
        ['_','#','_','#','_','#','_','#'] ]
        #"""
        self.initial = GameState(to_move='b', utility=0, board=board, moves=copy.deepcopy(self.get_all_moves(board,'b')) )


    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        if( player == 'b'):
            return state.utility
        else:
            return -state.utility
    

    def actions(self, state):
         """Return a list of the allowable moves at this point."""
         return state.moves


    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        if move not in state.moves:
            return state  # Illegal move has no effect
        nboard = copy.deepcopy(state.board)
        ( (x,y), (nx,ny) ) = move
        nboard[ny][nx] = nboard[y][x]
        nboard[y][x] = '_'
        if(nx == x+2 or nx == x-2 and ny == y+2 or ny == y-2):
            if(nx == x+2):
                newx = x+1
            if(nx == x-2):
                newx = x-1
            if(ny == y+2):
                newy = y+1
            if(ny == y-2):
                newy = y-1
            nboard[newy][newx] = '_'
        for i in range(8): # crowning checkers
            if( nboard[7][i] == 'b' ):
                nboard[7][i] = 'B'
            if( nboard[0][i] == 'w' ):
                nboard[0][i] = 'W'
        if(state.to_move == 'w'):
            nextplayer='b'
        else:
            nextplayer='w'
        return GameState(to_move=copy.deepcopy(nextplayer), utility=self.compute_utility(nboard, move, state.to_move), board=nboard, moves=copy.deepcopy(self.get_all_moves(nboard, nextplayer)) )


    def terminal_test(self, state):
        """A state is terminal if one player wins or there are no other possible moves."""
        return state.utility != 0 or len(state.moves) == 0


    def printboard(self, board):
        print(end="   ")
        for x in range(8):
            print(x, end=" ")
        print()
        for y in range(8):
            print(y, end=" |")
            for x in range(8):
                ckr = board[y][x]
                print(ckr, end="|")
            print()
        print()


    def compute_utility(self, board, move, player):
        """If 'b' wins with this move, return 1; if 'w' wins return -1; else return 0."""
        blackcount, whitecount = 0, 0
        board = copy.deepcopy(board)
        for y in range(8):
            for x in range(8):
                if(board[y][x].lower() == 'b'):
                    blackcount = 1
                if(board[y][x].lower() == 'w'):
                    whitecount = 1
                    if( blackcount > 0 ):
                        return 0
        if (blackcount == 0):
            return 1
        if (whitecount == 0):
            return -1

    def evaluation_function(self, state):
        """used in alpha beta pruning cut off search to reduce search times while still moving towards a solution """ 
        blackcount, whitecount = 0, 0
        board = copy.deepcopy(state.board)
        for y in range(8):
            for x in range(8):
                if(board[y][x].lower() == 'b'):
                    blackcount += 1
                if(board[y][x].lower() == 'w'):
                    whitecount += 1
        return whitecount - blackcount


    def get_all_moves(self, board, player):
        moves = set()
        if( player == 'b'):
            opposite = 'w'
        else:
            opposite = 'b'
        for y in range(8):
            for x in range(8):
                """ moves for black """
                if( board[y][x].lower() == player == 'b' or board[y][x] == player.upper() == 'W'): 
                    try:
                        if( board[y+1][x+1] == '_' and x+1 < 8 and y+1 < 8):
                            moves.add( ( (x,y), (x+1,y+1) ) )
                    except:
                        None
                    try:
                        if( board[y+1][x-1] == '_' and x-1 > -1 and y+1 < 8):
                            moves.add( ( (x,y), (x-1,y+1) ) )
                    except:
                        None
                    try:
                        if( board[y+1][x+1].lower() == opposite and board[y+2][x+2] == '_' and x+2 < 8 and y+2 < 8):
                            moves.add( ( (x,y), (x+2,y+2) ) )
                    except:
                        None
                    try:
                        if( board[y+1][x-1].lower() == opposite and board[y+2][x-2] == '_' and x-2 > -1 and y+2 < 8):
                            moves.add( ( (x,y), (x-2,y+2) ) )
                    except:
                        None
                """ Moves for white """
                if( board[y][x].lower() == player == 'w' or board[y][x] == player.upper() == 'B' ): 
                    try:
                        if( board[y-1][x-1] == '_' and x-1 > -1 and y-1 > -1):
                            moves.add( ( (x,y), (x-1,y-1) ) )
                    except:
                        None
                    try:
                        if( board[y-1][x+1] == '_' and x+1 < 8 and y-1 > -1):
                            moves.add( ( (x,y), (x+1,y-1) ) )
                    except:
                        None
                    try:
                        if( board[y-1][x+1].lower() == opposite and board[y-2][x+2] == '_' and x+2 < 8 and y-2 > -1):
                            moves.add( ( (x,y), (x+2,y-2) ) )
                    except:
                        None
                    try:
                        if( board[y-1][x-1].lower() == opposite and board[y-2][x-2] == '_' and x-2 > -1 and y-2 > -1):
                            moves.add( ( (x,y), (x-2,y-2) ) )
                    except:
                        None
                """ capital moves """
                """
                if( board[y][x] == 'B' or board[y][x] == 'W' ):
                    try:
                        if( board[y+1][x+1] == '_' and x+1 < 8 and y+1 < 8):
                            moves.add( ( (x,y), (x+1,y+1) ) )
                    except:
                        None
                    try:
                        if( board[y+1][x-1] == '_' and x-1 > -1 and y+1 < 8):
                            moves.add( ( (x,y), (x-1,y+1) ) )
                    except:
                        None
                    try:
                        if( board[y-1][x+1] == '_' and x+1 < 8 and y-1 > -1):
                            moves.add( ( (x,y), (x+1,y-1) ) )
                    except:
                        None
                    try:
                        if( board[y-1][x-1] == '_' and x-1 > -1 and y-1 > -1):
                            moves.add( ( (x,y), (x-1,y-1) ) )
                    except:
                        None
                    try:
                        if( board[y+1][x+1].lower() == opposite and board[y+2][x+2] == '_' and x+2 < 8 and y+2 < 8):
                            moves.add( ( (x,y), (x+2,y+2) ) )
                    except:
                        None
                    try:
                        if( board[y+1][x-1].lower() == opposite and board[y+2][x-2] == '_' and x-2 > -1 and y+2 < 8):
                            moves.add( ( (x,y), (x-2,y+2) ) )
                    except:
                        None
                    try:
                        if( board[y-1][x+1].lower() == opposite and board[y-2][x+2] == '_' and x+2 < 8 and y-2 > -1):
                            moves.add( ( (x,y), (x+2,y-2) ) )
                    except:
                        None
                    try:
                        if( board[y-1][x-1].lower() == opposite and board[y-2][x-2] == '_' and x-2 > -1 and y-2 > -1):
                            moves.add( ( (x,y), (x-2,y-2) ) )
                    except:
                        None
                #"""
        return moves
