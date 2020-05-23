##
## Part I: Connect Four Setup
##
from board import Board

class Player:
    def __init__(self, checker):
        '''creates player with checker X or O'''
        
        self.checker = checker
        self.num_moves = 0

    def __repr__(self):
        '''returns a string with Player name'''
        return 'Player('+str(self.checker)+')'
    
    def opponent_checker(self):
        '''designates a checker for the players opponents'''
        if self.checker == 'X':
            return 'O'
        elif self.checker == 'O':
            return 'X'

    def next_move(self, board):
        '''asks user inputed to decide where to ass the next checker'''
        x = input('Enter a column:')
        while board.can_add_to(int(x)) == False:
            print('Try Again!')
            x = input('Enter a column:')
        if board.can_add_to(int(x)):
            self.num_moves += 1
            print(x)
            return int(x)


