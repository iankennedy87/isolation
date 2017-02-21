"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score(game, player):
    return custom_deeper_partition(game, player)

def custom_partition(game, player):
    #increases value of moves on the larger side of partition and reduces value on smaller side
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    multiplier = 1 
    p = partition(game, player)
    if p[0]:
        if p[1]:
            multiplier = 100
        else: 
            multiplier = .01

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))        

    return float(multiplier*own_moves - (1/multiplier)*opp_moves)

def custom_deeper(game, player):
    """
    Takes the improved heuristic from class one level deeper by calculating 
    number of possible moves next turn for each possible move 
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")


    own_moves = game.get_legal_moves(player)
    own_score = 0
    for move in own_moves:
        newgame = game.forecast_move(move)
        newmoves = newgame.get_legal_moves(player)
        own_score = len(newmoves)

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_score = 0
    for move in opp_moves:
        newgame = game.forecast_move(move)
        newmoves = newgame.get_legal_moves(game.get_opponent(player))
        opp_score = len(newmoves)
    return float(own_score - opp_score)

def custom_middle(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    """Middle position is best move, assign it an infinite value"""
    middle = (int(game.height/2), int(game.width/2))    
    

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    if game.get_player_location(player) == middle and own_moves > opp_moves:
        return float("inf")
    return float(own_moves - opp_moves)

def custom_deeper_partition(game, player):
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    multiplier = 1 
    p = partition(game, player)
    if p[0]:
        if p[1]:
            multiplier = 100
        else: 
            multiplier = .01

    own_moves = game.get_legal_moves(player)
    own_score = 0
    for move in own_moves:
        newgame = game.forecast_move(move)
        newmoves = newgame.get_legal_moves(player)
        own_score = len(newmoves)

    opp_moves = game.get_legal_moves(game.get_opponent(player))
    opp_score = 0
    for move in opp_moves:
        newgame = game.forecast_move(move)
        newmoves = newgame.get_legal_moves(game.get_opponent(player))
        opp_score = len(newmoves)

    return float(multiplier*own_score - (1/multiplier)*opp_score)


def partition(game, player):
    """Determines whether there is a continuous partition of at least two squares, 
    and if so, whether the player is on the right side of the barrier"""
    height = game.height
    width = game.width
    blanks = game.get_blank_spaces()
    has_partition = False
    partition_col = int(game.width/2)
    partition_row = int(game.height/2)
    moves = game.get_legal_moves(player)
    if moves:
        player_location = game.get_player_location(player)
        for i in range(2, width - 3): #search for vertical partitions
            if (0,i) not in blanks and (0,i+1) not in blanks:
                j = 1
                while j < height and (j, i) not in blanks and (j, i + 1) not in blanks:
                    j += 1
                if j == height:
                    has_partition = True
                    pb = partition_blanks(game, (0,i))
                    if pb[0] > pb[1]: #more blanks on the left of the partition
                        for move in moves:
                            if move[1] < i:
                                return has_partition, True
                        return has_partition, False
                    else: #more blanks on right of partition
                        for move in moves:
                                if move[1] > i + 1:
                                    return has_partition, True
                        return has_partition, False

        for i in range(2, height - 3): #seach for horizontal partitions
            if (i,0) not in blanks and (i+1,0) not in blanks:
                j = 1
                while j < width and (i,j) not in blanks and (i+1, j) not in blanks:
                    j += 1
                if j == width:
                    has_partition = True
                    pb = partition_blanks(game, (i, 0))
                    if pb[0] > pb[1]: #more blanks on top of partition
                        for move in moves:
                                if move[0] < i:
                                    return has_partition, True
                        return has_partition, False
                    else: #more blanks below partition
                        for move in moves:
                            if move[0] > i + 1:
                                return has_partition, True
                        return has_partition, False

    return has_partition, False  
def partition_blanks(game, partition_line):
    #returns number of blank spaces on either side of a partition
    blanks = game.get_blank_spaces()

    if partition_line[0] == 0:
        partition_col = partition_line[1]
        left = 0
        right = 0
        for square in blanks:
            if square[1] < partition_col:
                left += 1
            else:
                right += 1 
        return (left, right)

    else:
        partition_row = partition_line[1]
        top = 0
        bottom = 0
        for square in blanks:
            if square[0] > partition_row:
                top += 1
            else:
                bottom += 1
        return (top, bottom)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=15.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        moves = game.get_legal_moves()
        best_move = (-1, -1)
        best_score = float("-inf")
        depth = 1
        if moves:
            best_move = moves[0]
        else :
            return best_move
    

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if not self.iterative:
                if self.method == 'minimax':
                    _, best_move = self.minimax(game, self.search_depth)
                elif self.method == 'alphabeta':
                    _, best_move = self.alphabeta(game, self.search_depth) 
            else:
                while self.time_left() > self.TIMER_THRESHOLD:
                    if self.method == 'minimax':
                        score, move = self.minimax(game, depth)
                    elif self.method == 'alphabeta':
                        score, move = self.alphabeta(game, depth)
                    if score > best_score:
                        best_move = move
                    depth += 1    


        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best_move
        

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.
(())
        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if game.get_legal_moves():
            scores = [(self.minvalue(game.forecast_move(move), depth), move) for move in game.get_legal_moves()]
        else:
            return (self.score(game, self), (-1,-1))    

        return max(scores)

    def maxvalue(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 1:
            return self.score(game, self)
        high_score = float("-inf")
        for move in game.get_legal_moves():
            high_score = max(high_score, self.minvalue(game.forecast_move(move), depth - 1))
        return high_score

    def minvalue(self, game, depth):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 1:
            return self.score(game, self)
        low_score = float("inf")
        for move in game.get_legal_moves():
            low_score = min(low_score, self.maxvalue(game.forecast_move(move), depth - 1))
        return low_score

    # def ab_maxvalue(self, game, depth, a, b):
    #     print(a,b)
    #     if depth == 0:
    #         # print(a,b)
    #         return self.score(game, self)
    #     high_score = float("-inf")
    #     for move in game.get_legal_moves():
    #         high_score = max(high_score, self.ab_minvalue(game.forecast_move(move), depth - 1, a, b))
    #         if high_score >= b:
    #             # print(a,b)
    #             return high_score
    #         a = max(a, high_score)
    #     # print(a,b)
    #     return high_score

    def ab_maxvalue(self, game, depth, a, b):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return (self.score(game, self), (-1, -1))
        high_score = float("-inf")
        high_move = None
        for move in game.get_legal_moves():
            score = self.ab_minvalue(game.forecast_move(move), depth - 1, a, b)
            if score > high_score:
                high_score = score
                high_move = move
            if score >= b:
                return (high_score, high_move) 
            a = max(a, score)
        return (high_score, high_move)    

    # def ab_minvalue(self, game, depth, a, b):

    #     if self.time_left() < self.TIMER_THRESHOLD:
    #         raise Timeout()

    #     if depth == 0:
    #         return (self.score(game, self), (-1, -1))
    #     low_score = float("inf")
    #     low_move = None
    #     for move in game.get_legal_moves():
    #         score = min(low_score, self.ab_maxvalue(game.forecast_move(move), depth - 1, a, b)[0])
    #         if score < low_score:
    #             low_score = score
    #             low_move = move
    #         if score <= a:
    #             return (score, move)
    #         b = min(b, score)
    #     return (low_score, low_move)

    def ab_minvalue(self, game, depth, a, b):

        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return self.score(game, self)
        low_score = float("inf")
        low_move = None
        for move in game.get_legal_moves():
            low_score = min(low_score, self.ab_maxvalue(game.forecast_move(move), depth - 1, a, b)[0])
            # if score < low_score:
            #     low_score = score
            #     low_move = move
            if low_score <= a:
                return low_score
            b = min(b, low_score)
        return low_score

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # if depth == 0:
        #     return(self.score(game,self), (-1,-1))

        if game.get_legal_moves():
            return self.ab_maxvalue(game, depth, alpha, beta)
        else:
            return (self.score(game, self), (-1, -1))
        # if maximizing_player:
        #     best_score = float("-inf")
        #     best_move = None    
        #     for move in game.get_legal_moves():
        #         score = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, False)[0]
        #         if score > best_score:
        #             best_score = score
        #             best_move = move
        #         if score >= beta:
        #             return (score, move)
        #         alpha = max(alpha, score)
        #     return (best_score, best_move)

        # else:
        #     low_score = float("inf")
        #     low_move = None
        #     for move in game.get_legal_moves():
        #         score = self.alphabeta(game.forecast_move(move), depth - 1, alpha, beta, True)[0]
        #         if score < low_score:
        #             low_score = score
        #             low_move = move
        #         if score <= alpha:
        #             return (score, move)
        #         beta = min(beta, score)
        #     return (low_score, low_move)
          

