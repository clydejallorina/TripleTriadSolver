from pprint import pprint
from typing import List, Optional, Union # type hinting
from PIL import Image, ImageDraw, ImageColor, ImageFont

# Classes needed for the game to work

class Card:
    id:int = 0
    name:str = ""
    owned_by:int = 0 # attribute only really used in the game module to set points
    stars:int = 0
    
    # Directional attack power
    left:int = 0
    right:int = 0
    up:int = 0
    down:int = 0
    
    def __init__(self, name:str="", **kwargs:int):
        self.id = kwargs['id']
        self.name = name
        self.stars = kwargs['stars']
        self.left = kwargs['left']
        self.right = kwargs['right']
        self.up = kwargs['up']
        self.down = kwargs['down']
        
    def __repr__(self) -> str:
        return f"{self.owned_by} - {self.name}({self.id}) - {self.stars} star/s - L{self.left} R{self.right} U{self.up} D{self.down}"
        
    def null_card(self):
        """
        Returns an empty card with all attributes set to 0
        """
        return Card()
    

class Deck:
    cards:List[Card] = [] # list of cards
    
    def __init__(self, cards:List[Card]=[]):
        self.cards = cards
        
    def __len__(self) -> int:
        return len(self.cards)
        
    def list_cards(self) -> List[str]:
        """
        Returns the names of all the cards in the deck
        Use list(Deck) to get this.
        """
        return [card.name for card in self.cards]
    
    def validate_deck(self):
        """
        Returns true if the deck is valid for FF14 Triple Triad
        Returns false otherwise
        
        A deck is valid if:
        - There is only 1 5-star card at most
        - There are two 4-stars or 1 4-star and 1 5-star at most
        - There are 5 cards in the deck (if just initialized)
        """
        if len(self.cards) > 5:
            return False
        five_stars = 0
        four_stars = 0
        for card in self.cards:
            if card.stars == 5:
                five_stars += 1
            if card.stars == 4:
                four_stars += 1
        
        if five_stars > 1:
            return False
        if five_stars + four_stars > 2:
            return False
        return True
    
    def get_card_by_id(self, id:int) -> Optional[Card]:
        """
        Returns the Card object corresponding to id
        Pops it from the internal cards list
        
        Returns None if card cannot be found in deck
        """
        for card in self.cards:
            if card.id == id:
                self.cards.remove(card) # "pop" the card from the deck
                return card
        return None
    
    def get_card_by_name(self, name:str) -> Optional[Card]:
        """
        Returns the Card object corresponding to name
        Pops it from the internal cards list
        
        Returns None if card cannot be found in deck
        """
        for card in self.cards:
            if card.name == name:
                self.cards.remove(card) # "pop" the card from the deck
                return card
        return None
    
    def add_card(self, card:Card):
        """
        Add a card to the internal cards list.
        This function does not check if the card is legal.
        Will not return anything.
        """
        self.cards.append(card)
        
# Game class that performs game functions
class Game:
    p1_deck = Deck([]) # player deck
    p2_deck = Deck([]) # enemy deck
    
    p1_first = True # will p1 play first?
    
    board:List[List[Optional[Card]]] = [[None, None, None],[None, None, None],[None, None, None]]
    moves:List[List[Union[Card, int]]] = [] # move list format: [[Card1, row, col], [Card2, row, col], ...]
    
    def __init__(self, p1_deck:Deck, p2_deck:Deck, p1_first:bool=True):
        if not p1_deck.validate_deck():
            raise Exception("Player 1 Deck is not validated")
        
        if not p2_deck.validate_deck():
            raise Exception("Player 2 Deck is not validated")
        
        self.p1_deck = p1_deck
        self.p2_deck = p2_deck
        self.p1_first = p1_first
        
        self.board = [[None, None, None],[None, None, None],[None, None, None]]
        self.moves = []
        
    def check_win(self) -> Optional[int]:
        """
        Checks if the current board state has a win condition.
        If the board state is a draw, it will return 0.
        If the board state is won by P1, it will return a positive int showing by how much P1 won.
        If the board state is won by P2, it will return a negative int instead.
        If the board state is not at a terminal state, it will return None.
        """
        p1 = len(self.p1_deck)
        p2 = len(self.p2_deck)
        for row in self.board:
            for card in row:
                if card == None: # oh wait, the game's not yet done
                    return None
                if card.owned_by == 1: # card is owned by p1
                    p1 += 1
                if card.owned_by == 2: # card is owned by p2
                    p2 += 1
        return p1 - p2
    
    def print_board_state(self):
        pprint(self.board)
        
    def draw_board_state(self, size_x=512, size_y=512):
        """
        Generate a 512x512 (by default) image of the current board state
        """
        # Color palette and font
        black = ImageColor.getcolor("black", "RGBA")
        red = ImageColor.getcolor("lightcoral", "RGBA")
        blue = ImageColor.getcolor("lightblue", "RGBA")
        font = ImageFont.truetype("arial.ttf", 24)
        
        # Create the canvas
        base_im = Image.new("RGBA", (size_x, size_y), "gray")
        
        # Draw grid
        im = ImageDraw.Draw(base_im)
        im.line([(size_x // 3, 0), (size_x // 3, size_y)], fill=black, width=2)
        im.line([(2 * size_x // 3, 0), (2 * size_x // 3, size_y)], fill=black, width=2)
        im.line([(0, size_y // 3), (size_x, size_y // 3)], fill=black, width=2)
        im.line([(0, 2 * size_y // 3), (size_x, 2 * size_y // 3)], fill=black, width=2)
        
        # Color backgrounds of occupied spaces
        occupied = self.get_occupied_spaces()
        for card in occupied:
            # This is why I should never do front-end stuff
            x_left = ((card[2] * size_x) // 3) + (min(card[2], 1) * 2)
            x_right = (((card[2] + 1) * size_x) // 3) - 1
            y_up = ((card[1] * size_y) // 3) + (min(card[1], 1) * 2)
            y_down = (((card[1] + 1) * size_y) // 3) - 1
            inner_fill = [None, blue, red]
            im.rectangle([(x_left, y_up), (x_right, y_down)], outline=inner_fill[card[0]], fill=inner_fill[card[0]])
        
            # Draw card stats on occupied spaces
            c = self.board[card[1]][card[2]]
            
            # Calculate coordinates
            up_coord = (((x_left + x_right) / 2), (y_up + 5))
            down_coord = (((x_left + x_right) / 2), (y_down - 5))
            left_coord = ((x_left + 5), ((y_up + y_down) / 2))
            right_coord = ((x_right - 5), ((y_up + y_down) / 2))
            
            # Place text in coordinates
            im.text(up_coord, f"{c.up}", anchor="ma", fill=black, font=font)
            im.text(down_coord, f"{c.down}", anchor="md", fill=black, font=font)
            im.text(left_coord, f"{c.left}", anchor="lm", fill=black, font=font)
            im.text(right_coord, f"{c.right}", anchor="rm", fill=black, font=font)
        
        # Show the image
        base_im.show()
        
    def print_p1_deck(self):
        pprint(self.p1_deck.list_cards())
    
    def print_p2_deck(self):
        pprint(self.p2_deck.list_cards())
        
    def print_owners(self):
        board = []
        for row in self.board:
            r = []
            for col in row:
                if col != None:
                    r.append(col.owned_by)
                else:
                    r.append(0)
            board.append(r)
        pprint(board)
        
    def get_occupied_spaces(self) -> List[List[int]]:
        """
        Returns all the cells occupied by a card
        Output Format is as follows:
        [ [owner, row, col], ...]
        """
        ret = []
        for r, row in enumerate(self.board):
            for c, col in enumerate(row):
                if col != None:
                    ret.append([col.owned_by, r, c])
        return ret
        
    def get_available_spaces(self) -> List[List[int]]:
        available_spaces:List[List[int]] = []
        for r, row in enumerate(self.board):
            for c, col in enumerate(row):
                if col == None:
                    available_spaces.append([r, c])
        return available_spaces
        
    def play_card(self, player:int, card_name:str, row:int, col:int):
        # Check if the appropriate player is making the move (if it's the first move)
        if len(self.moves) == 0:
            if (player == 2 and self.p1_first) or (player == 1 and not self.p1_first):
                raise Exception(f"p1_first is set to {self.p1_first}")
        # Check if the player id matches with the last move
        if row > 3 or col > 3 or row < 0 or col < 0:
            raise IndexError("row or col must be between 0 to 2 inclusive")
        if self.board[row][col] != None:
            raise Exception("Player attempting to play a card where a card is already in play!")
        if len(self.moves) > 0 and self.moves[-1][0] == player:
            raise Exception(f"Player {player} attempting to play two cards in a row!")
        
        # Get the card from the decks
        if player == 1:
            card = self.p1_deck.get_card_by_name(card_name)
        elif player == 2:
            card = self.p2_deck.get_card_by_name(card_name)
        else:
            raise Exception(f"Unknown player ID {player} attempting to play!")
        if card == None: # card was not found in deck
            raise Exception(f"Card {card_name} not found in player {player}'s deck")
        
        # Play the card at the appropriate row and column
        card.owned_by = player
        self.moves.append([card_name, row, col]) # append to the move list
        self.board[row][col] = card
        
        # Calculate the cards getting taken over
        # Check above
        if row > 0 and self.board[row-1][col] != None and self.board[row-1][col].down < card.up:
            self.board[row-1][col].owned_by = player
            
        # Check below
        if row < 2 and self.board[row+1][col] != None and self.board[row+1][col].up < card.down:
            self.board[row+1][col].owned_by = player
            
        # Check left
        if col > 0 and self.board[row][col-1] != None and self.board[row][col-1].right < card.left:
            self.board[row][col-1].owned_by = player
        
        # Check right
        if col < 2 and self.board[row][col+1] != None and self.board[row][col+1].left < card.right:
            self.board[row][col+1].owned_by = player
        