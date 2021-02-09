import sys
import deal_card

valid_actions = [
    'hit',
    'stand',
    'doubledown',
    'split'
]

default_board_state = {
    "player_hand": 0,
    "dealer_hand": 0,
    "player_last_action": "",
    "dealer_last_action": "",
    "result": "",
    "bet_multiplier": 1.5
}

default_multiplier = 1.5

dealer_max = 17

# Dealer max hand is 17
def card_value(card, hand_total):
    card_pair = card.split('-')

    value = 0
    if card_pair[0].lower() in ['j','q','k']:
        value = 10
    elif card_pair[0].lower() == 'a':
        if hand_total <= 10:
            value = 11
        else:
            value = 1
    else:
        value = int(card_pair[0])
    return value

def play(board_state, player_action):
    # To start, all that is needed is the bet
    # the user will be
    if board_state == "":
        board_state = default_board_state

    board_state["bet_multiplier"] = 1.5
    board_state["result"] = ''

    if board_state["player_last_action"] in ['stand', 'doubledown']:
        player_action = 'stand'

    # Beginning state. Always happens if the player hand or dealer hand is 0.
    if board_state["player_hand"] == 0 or board_state["dealer_hand"] == 0:
        board_state["player_hand"] = card_value(deal_card.deal(0), 0)
        board_state["dealer_hand"] = card_value(deal_card.deal(0), 0)
        board_state["player_last_action"] = 'hit'
        board_state["dealer_last_action"] = 'hit'

    # Do player action. Dealer only takes an action if player action is valid.
    elif player_action in valid_actions:
        # Do something good
        if player_action in ['hit', 'doubledown', 'split']:
            board_state["player_hand"] += card_value(deal_card.deal(0), board_state["player_hand"])
        
        board_state["player_last_action"] = player_action
        
        # Dealer logic. Need to add one that lets the dealer "check" for blackjack
        if board_state["dealer_hand"] < dealer_max:
            board_state["dealer_hand"] += card_value(deal_card.deal(0), board_state["dealer_hand"])
            board_state["dealer_last_action"] = 'hit'
        else:
            board_state["dealer_last_action"] = 'stand'
    else:
        sys.exit('Invalid action. Choose: ' + str(valid_actions))

    # Evaluate board state.
    if board_state["player_hand"] == 21 and board_state["dealer_hand"] != 21:
        board_state["result"] = 'win'
        board_state["bet_multiplier"] = 2
    
    # Bust conditions for dealer and player

    # Compare dealer and player where not bust.


    return board_state
    # get first card




if __name__ == '__main__':
    myCard = deal_card.deal(0)
    myVal = card_value(myCard, 12)
    print(myCard, '=', myVal)