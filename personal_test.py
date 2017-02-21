import isolation
import game_agent
import sample_players

from isolation import Board
from sample_players import RandomPlayer
from sample_players import null_score
from sample_players import open_move_score
from sample_players import improved_score
from game_agent import CustomPlayer
from game_agent import custom_score
from game_agent import partition
from game_agent import partition_blanks

if __name__ == '__main__':
    # BLANK = 0
    # height = 7
    # width = 7
    # board = [[BLANK for i in range(width)] for j in range(height)]
    # for i in range(7):
    #     board[i][3] = "x"
    #     board[i][4] = "x"
    # print(board)
    player1 = CustomPlayer()
    player2 = CustomPlayer()
    board = Board(player1, player2)
    for i in range(7):
        # board.__board_state__[2][i] = "x"
        board.__board_state__[3][i] = "x"
        board.__board_state__[4][i] = "x"
        board.__board_state__[i][2] = "x"
        board.__board_state__[i][3] = "x"
        # board.__board_state__[i][4] = "x"
    board.apply_move((2,5))    
    print(board.to_string())
    print(partition(board, player1))
    print(partition_blanks(board, (0,3)))