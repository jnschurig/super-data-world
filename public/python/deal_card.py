import random, os, json, re
from pathlib import Path

deck = [
     'A-h'  ,'A-c'  ,'A-d'  ,'A-s' 
    ,'2-h'  ,'2-c'  ,'2-d'  ,'2-s'
    ,'3-h'  ,'3-c'  ,'3-d'  ,'3-s'
    ,'4-h'  ,'4-c'  ,'4-d'  ,'4-s'
    ,'5-h'  ,'5-c'  ,'5-d'  ,'5-s'
    ,'6-h'  ,'6-c'  ,'6-d'  ,'6-s'
    ,'7-h'  ,'7-c'  ,'7-d'  ,'7-s'
    ,'8-h'  ,'8-c'  ,'8-d'  ,'8-s'
    ,'9-h'  ,'9-c'  ,'9-d'  ,'9-s'
    ,'10-h' ,'10-c' ,'10-d' ,'10-s'
    ,'J-h'  ,'J-c'  ,'J-d'  ,'J-s'
    ,'Q-h'  ,'Q-c'  ,'Q-d'  ,'Q-s'
    ,'K-h'  ,'K-c'  ,'K-d'  ,'K-s'
]

pad_length = 2

def simple():
    # Assumes an infinite number of decks so never need to shuffle or reload.
    random_number = random.randrange(len(deck)-1)
    random_card = deck[random_number]
    return random_card

def from_deck(deck_count, instance_name):
    # This function is not ready for primetime. 
    # The main problem has to do with file contention.
    # If two peole request a card from the same source and ask for the same number of decks...
    # It will attempt to draw from the same file, causing resource contention.
    # Ths instance name would have to be someting like a session id, or a user name...
    # Remove file exension from instance name, if there is one.
    instance_name = re.sub('\\..*','',instance_name)
    deck_count = abs(int(deck_count))
    random_card = ''
    if deck_count == 0:
        random_number = random.randrange(len(deck)-1)
        random_card = deck[random_number]
    else:
        # Now do the crazy stuff like creating a deck and writing it to a file.
        deck_dir = os.path.dirname(os.path.realpath(__file__)) + '/data/decks'
        Path(deck_dir).mkdir(parents=True, exist_ok=True)
        # Example: "stack_blackjack_04_decks.json"
        file_name = 'stack_' + instance_name + '_' + str(deck_count.zfill(pad_length)) + '_decks.json'
        # Check if the file exists
            # If so, read the file and assign contents to variable
            # Are there enough cards in the deck?
                # Yes. draw a card from it.
                # Remove card from deck and write deck to file.
                # No, compile a new deck with n decks and draw a card from it.
            # If not, compile a new stack with n decks and draw a card from it.
            # Write deck contents to a file.
        # Return card.
        # 
        random_card = 'A-h' # ha ha.
    return random_card

if __name__ == '__main__':
    my_card = deal(0)
    print(my_card)
    my_card = from_deck(4, 'blackjack')
    print(my_card)