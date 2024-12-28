from game import *
from solver import *
from pprint import pprint
from os.path import exists
import json

def generate_cards(filepath:str) -> List[Card]:
    """
    Generates a list of cards from the filepath given
    Will return an empty list if the file isn't found
    Only works for JSON data from https://triad.raelys.com/
    """
    if exists(filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            resp = json.load(file)
            cards = []
            for card in resp["results"]:
                id = card["id"]
                name = card["name"]
                stars = card["stars"]
                
                left = card["stats"]["numeric"]["left"]
                right = card["stats"]["numeric"]["right"]
                up = card["stats"]["numeric"]["top"]
                down = card["stats"]["numeric"]["bottom"]
                
                cards.append(Card(name=name, id=id, stars=stars, left=left, right=right, up=up, down=down))
            return cards
    return []

def find_card(card_list:List[Card], card_name:str) -> Optional[Card]:
    for card in card_list:
        if card.name == card_name:
            return card
    return None

def main():
    card_list = generate_cards("cards.json")
    p1_deck = Deck(card_list[24:29])
    p2_deck = Deck(card_list[31:36])
    print(len(p1_deck))
    
    game = Game(p1_deck=p1_deck, p2_deck=p2_deck)
    game.print_p1_deck()
    game.print_p2_deck()
    
    game.play_card(1, "Chimera", 2, 2)
    game.draw_board_state()
    
    pprint(alpha_beta_search(game, 1))
    
    # game.play_card(2, "Biggs & Wedge", 1, 1)
    # game.draw_board_state()
    
    # game.play_card(1, "Blue Dragon", 0, 0)
    # game.draw_board_state()
    
    # game.play_card(2, "Gerolt", 2, 1)
    # game.draw_board_state()
    
    # game.play_card(1, "Momodi Modi", 0, 1)
    # game.draw_board_state()
    
    # pprint(alpha_beta_search(game, 2))
    
    # game.play_card(2, "Frixio", 0, 2)
    # game.draw_board_state()
    
    # pprint(alpha_beta_search(game, 1))
    
    # game.play_card(1, "Scarface Bugaal Ja", 2, 0)
    # game.draw_board_state()
    
    # game.play_card(2, "Mutamix Bubblypots", 1, 2)
    # game.draw_board_state()
    
    # game.play_card(1, "Baderon Tenfingers", 1, 0)
    # game.draw_board_state()

if __name__ == "__main__":
    main()
