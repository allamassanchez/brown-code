##
## Part III: AI Player
##

import random 
from board import Board
from hw07_1 import Player 
from hw07_2 import connect_four
from hw07_2 import process_move
from hw07_2 import *

class AIPlayer(Player):
    '''creates an intelligent player for the user to play against'''
    def __init__(self, checker, tiebreak, lookahead):
        super().__init__(checker)
        self.tiebreak = tiebreak
        self.lookahead = lookahead
        
    def __repr__(self):
        return 'Player' + str(self.checker) + ' (' + str(self.tiebreak)+', '+ str(self.lookahead)+')'

    def max_score_column(self, scores):
        '''determines the best columns to add a checker to'''
        score_list = [number for number in range(len(scores)) if scores[number] == max(scores)]
        if self.tiebreak == 'LEFT':
            return score_list[0]
        elif self.tiebreak == 'RIGHT':
            return score_list[-1]
        elif self.tiebreak == 'RANDOM':
            return random.choice(score_list)

    def scores_for(self, board):
        '''calculates scores for the AIPlayer taking into account possible moves
        for the opponent'''
        scores = [0] * board.width
        for number in range(board.width):
            if board.can_add_to(number) == False:
                scores[number] = -1
            elif board.is_win_for(self.checker):
                scores[number] = 100
            elif board.is_win_for(self.opponent_checker()):
                scores[number] = 0
            elif self.lookahead == 0:
                scores[number] = 50
            else:
                board.add_checker(self.checker, number)
                AIopponent = AIPlayer(self.opponent_checker(), self.tiebreak, self.lookahead - 1)
                opponent_scores = AIopponent.scores_for(board)
                board.remove_checker(number)
                if max(opponent_scores) == 100:
                    scores[number] = 0
                elif max(opponent_scores) == 0:
                    scores[number] = 100
                elif max(opponent_scores) == 50:
                    scores[number] = 50
        return scores

    def next_move(self,board):
        '''calculates best move for the AIPlayer'''
        self.num_moves += 1
        scores = self.scores_for(board)
        return self.max_score_column(scores)
    