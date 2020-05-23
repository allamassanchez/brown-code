#
## Part II: Connect Four Play
#

from board import Board
from hw07_1 import Player
import random
    
def connect_four(player1, player2):
    """ Plays a game of Connect Four between the two specified players,
        and returns the Board object as it looks at the end of the game.
        inputs: player1 and player2 are objects representing Connect Four
                  players (objects of the Player class or a subclass of Player).
                  One player should use 'X' checkers and the other should
                  use 'O' checkers.
    """
    # Make sure one player is 'X' and one player is 'O'.

    if player1.checker not in 'XO' or player2.checker not in 'XO' \
       or player1.checker == player2.checker:
        print('need one X player and one O player.')
        return None

    # Reset players
    player1.num_moves = 0
    player2.num_moves = 0

    print('Welcome to Connect Four!')
    print()
    board = Board(6, 7)
    print(board)
    
    while True:
        if process_move(player1, board):
            return board

        if process_move(player2, board):
            return board

def process_move(player, board):
    '''decides whether the game continues or not'''
    print('Player ' + player.checker + "'s turn")
    x = player.next_move(board)
    board.add_checker(player.checker, x)
    print('\n', board)
    if board.is_win_for(player.checker):
        print('Player ' + player.checker + ' wins in '+ str(player.num_moves) +' moves.')
        print('Congratulations!')
        return True
    elif board.is_full():
        print("It's a tie!")
        return True
    else:
        return False


class RandomPlayer(Player):
    """ a player that chooses at random from the available columns.
        RandomPlayer inherits from Player.
    """
    
    def next_move(self, board):
        '''chooses a random number for a column that a checker can be added to'''
        column_options = [number for number in range(board.width) if board.can_add_to(number)]
        self.num_moves += 1
        return random.choice(column_options)


''' TESTING '''
def process_move_test():
    '''tests process_move'''
    player = Player('O')
    player2 = Player('X')
    board = Board(2,4)
    board.add_checkers('0011223')
    x = 3
    assert process_move_helper(player, board, x) == True, 'win case failed'
    board.remove_checker(3)
    board.remove_checker(3)
    assert process_move_helper(player, board, x) == False, 'general case failed'
    assert process_move_helper(player2, board, x) == True, 'tie case failed'
def next_move_test():
    '''test next_move'''
    board = Board(2,4)
    player = RandomPlayer('X')
    x = player.next_move(board)
    assert board.can_add_to(x), 'general case failed'

def process_move_helper(player,board, x):
    '''used to test process_move'''
    ###added code from process_move to test it
    ### only removed next_move because I am inputting it manually
    print('Player ' + player.checker + "'s turn")
    board.add_checker(player.checker, x)
    print('\n', board)
    if board.is_win_for(player.checker):
        print('Player ' + player.checker + ' wins in '+ str(player.num_moves) +' moves.')
        print('Congratulations!')
        return True
    elif board.is_full():
        print("It's a tie!")
        return True
    else:
        return False


process_move_test()
next_move_test()