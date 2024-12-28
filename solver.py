from game import *
from copy import deepcopy
from functools import cache

INF = 999999 # just some absurdly high number as placeholder for infinity
DEBUG = True # debug flag for debugging the solver

def terminal_test(game_state:Game):
    """
    The terminal test would simply just be if all 9 slots are filled,
    but in this case it would also be if 9 moves were done in the game
    """
    return len(game_state.moves) == 9

def utility(game_state:Game):
    """
    For the case of Triple Triad, I've thought of just using the difference
    between the two players as the utility function. This makes it so that
    p1 winning would have a positive integer while p2 winning would have a
    negative integer. This also makes it so that draws are 0 and both players
    will be attempting to move away from the zero-sum game.
    """
    return game_state.check_win()

@cache
def alpha_beta_search(game_state:Game, player:int) -> Optional[List[Union[str, int]]]:
    """
    Start an alpha-beta search to find the most optimal move
    given that player <player> was the last move
    in the specified game state.
    
    Returns the move this method deems as the optimal move
    for the player specified.
    
    Returns None if the game state is already over
    """
    # If the game is already over, return None. There are no more moves to be done.
    if terminal_test(game_state):
        return None
    
    # Debug print
    if DEBUG:
        print(f"Attempting depth {9 - len(game_state.moves)} search")
    
    # The game isn't over. Go through the game tree.
    if player == 1:
        value, card_name, row, col = max_val(game_state, -INF, +INF)
    elif player == 2:
        value, card_name, row, col = min_val(game_state, -INF, +INF)
        
    # Return the best move for the player
    return [card_name, row, col]

@cache
def max_val(game_state:Game, alpha:int, beta:int) -> List[Union[int, str]]:
    """
    Calculates the "best" move for player 1
    
    Returns a list with the following format:
    [v, card_name, row, col]
    where
    v:int = utility value of the game state
    card_name:str = card name responsible for the utility value
    row:int = row where the card should be played
    col:int = col where the card should be played
    """
    # If it's a terminal action, return utility
    if terminal_test(game_state):
        return [utility(game_state)] + game_state.moves[-1]
    
    value = -INF
    card_name = ""
    row = -1
    col = -1
    p1_deck = game_state.p1_deck
    p2_deck = game_state.p2_deck
    
    # Generate actions
    for card in game_state.p1_deck.list_cards():
        for coords in game_state.get_available_spaces():
            # Generate new game state with appropriate card and coords
            new_game_state = Game(deepcopy(p1_deck), deepcopy(p2_deck), game_state.p1_first)
            new_game_state.board = deepcopy(game_state.board)
            new_game_state.moves = deepcopy(game_state.moves)
            new_game_state.play_card(1, card, coords[0], coords[1])
            
            # Pass the new game state to the next depth
            val, c_name, r, c = min_val(new_game_state, alpha, beta)
            
            # If the new value obtained is higher, then it should be our new best move
            if val > value:
                value, card_name, row, col = val, c_name, r, c
            
            # If this is higher or equal to beta, then stop going deeper
            if value >= beta:
                return [value, card_name, row, col]
            
            # Set alpha to the maximum value
            alpha = max(alpha, value)
    
    # Return the best found out of all possible moves
    return [value, card_name, row, col]

@cache
def min_val(game_state:Game, alpha:int, beta:int):
    """
    Calculates the "best" move for player 2
    
    Returns a list with the following format:
    [v, card_name, row, col]
    where
    v:int = utility value of the game state
    card_name:str = card name responsible for the utility value
    row:int = row where the card should be played
    col:int = col where the card should be played
    """
    # If it's a terminal action, return utility
    if terminal_test(game_state):
        return [utility(game_state)] + game_state.moves[-1]
    
    value = INF
    card_name = ""
    row = -1
    col = -1
    p1_deck = game_state.p1_deck
    p2_deck = game_state.p2_deck
    
    # Generate actions
    for card in game_state.p2_deck.list_cards():
        for coords in game_state.get_available_spaces():
            # Generate new game state with appropriate card and coords
            new_game_state = Game(deepcopy(p1_deck), deepcopy(p2_deck), game_state.p1_first)
            new_game_state.board = deepcopy(game_state.board)
            new_game_state.moves = deepcopy(game_state.moves)
            new_game_state.play_card(2, card, coords[0], coords[1])
            
            # Pass the new game state to the next depth
            val, c_name, r, c = max_val(new_game_state, alpha, beta)
            
            # If the new value obtained is lower, then it should be our new best move
            if val < value:
                value, card_name, row, col = val, c_name, r, c
            
            # If this is lower or equal to alpha, then stop going deeper
            if value <= alpha:
                return [value, card_name, row, col]
            
            # Set beta to the minimum value
            beta = min(beta, value)
    
    # Return the best found out of all possible moves
    return [value, card_name, row, col]