import sys
import deal_card, world_events

valid_actions = [
    'hit',
    'stand',
    'doubledown',
    'split'
]

default_board_state = {
    "player_hand_val": 0,
    "dealer_hand_val": 0,
    "player_hand": "",
    "dealer_hand": "",
    "player_last_action": "",
    "dealer_last_action": "",
    "result": "",
    "bet_return": 1,
    "status": "",
    "wager": 0
}

default_return = 1

dealer_max = 17

deck_count = 8

test_hand = '2-h,7-s,A-d,A-s' # should return 13

# Dealer max hand is 17
def card_value(card, hand_total):
    card_pair = card.strip().split('-')

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

def hand_value(hand):
    total_val = 0
    hand_list = hand.split(',')
    # print(hand_list)
    # print(hand_list.sort())
    ace_count = 0
    ace_done = 0
    # Hold aces and add them in last.
    for i in hand_list:
        if 'a'.upper() in i.upper():
            ace_count += 1
        else:
            total_val += card_value(i, total_val)
    while ace_done < ace_count:
        total_val += card_value('A-h', total_val)
        ace_done += 1
    # Now we know if there is an ace in the hand.
    return total_val
    
    

def play(board_state, player_action):
    # To start, all that is needed is the bet
    # the user will be
    wager = board_state['wager']

    if board_state['status'] == 'none':
        board_state = default_board_state
        board_state['wager'] = wager
    dealer_action = 'hit'

    board_state["bet_return"] = 1
    board_state["result"] = ''

    if player_action == 'doubledown':
        # Check to see if it's ok to do doubledown.
        if not len(board_state["player_hand"].split(',')) == 1:
            # Can only use doubledown if and only if they have one card.
            player_action = 'hit'

    if board_state["player_last_action"] in ['stand', 'doubledown']:
        player_action = 'stand'

    # Beginning state. Always happens if the player hand or dealer hand have no cards.
    if board_state["player_hand"] == '' or board_state["dealer_hand"] == '':
        board_state["player_hand"] = deal_card.simple(deck_count)
        board_state["dealer_hand"] = deal_card.simple(deck_count)
        board_state["player_hand_val"] = hand_value(board_state["player_hand"])
        board_state["dealer_hand_val"] = hand_value(board_state["dealer_hand"])
        board_state["player_last_action"] = 'hit'
        board_state["dealer_last_action"] = 'hit'

    # Do player action. Dealer only takes an action if player action is valid.
    elif player_action in valid_actions:
        # Do something good
        if player_action in ['hit', 'doubledown', 'split'] and board_state["player_hand_val"] < 21:
            board_state["player_hand"] += ',' + deal_card.simple(deck_count)
            board_state["player_hand_val"] = hand_value(board_state["player_hand"])
            if board_state["player_hand_val"] >= 21:
                player_action = 'stand'
            if player_action == 'doubledown':
                player_action = 'stand'
        
        board_state["player_last_action"] = player_action
        
        # Dealer logic. 
        # Need to allow the dealer to loop through draws if the player is set to "stand"
        # 1. Dealer and player both already have a card. We need to only do this section after the player has switched to "stand"
        if player_action == 'stand':
            do_loop = True
            while do_loop:
                do_loop = False # By default, run through loop once.
                if board_state["dealer_hand_val"] < dealer_max:
                    board_state["dealer_hand"] += ',' + deal_card.simple(deck_count)
                    board_state["dealer_hand_val"] = hand_value(board_state["dealer_hand"])
                    board_state["dealer_last_action"] = 'hit'
                    # dealer_action = 'stand'
                else:
                    board_state["dealer_last_action"] = 'stand'
                    dealer_action = 'stand'
                # if player_action == 'stand' and not dealer_action == 'stand':
                if not dealer_action == 'stand':
                    # Player is done, but dealer is not. Let's loop
                    do_loop = True
                
    else:
        print('Invalid action. Choose: ' + str(valid_actions))
        # sys.exit()

    # Evaluate board state.
    player_bust = False
    if board_state["player_hand_val"] > 21:
        player_bust = True
    dealer_bust = False
    if board_state["dealer_hand_val"] > 21:
        dealer_bust = True
        
    if player_action == 'stand' and dealer_action == 'stand':
        # Check if both are bust
        if player_bust and dealer_bust:
            board_state["result"] = 'push'
        # both players are not bust. Check if they are equal...
        elif board_state["player_hand_val"] == board_state["dealer_hand_val"]:
            board_state["result"] = 'push'
        # Someone is going to win...
        elif player_bust:
            board_state["result"] = 'lose'
        # Player is not bust. Check for blackjack
        elif board_state["player_hand_val"] == 21:
            board_state["result"] = 'win'
            board_state["bet_return"] = 1.5
        # Player is still not bust. Check for dealer bust
        elif dealer_bust:
            board_state["result"] = 'win'
        # Neither player nor dealer is bust. Neither is the same.
        elif board_state["player_hand_val"] > board_state["dealer_hand_val"]:
            board_state["result"] = 'win'
        else:
            board_state["result"] = 'lose'

    return board_state
    
def session(user, command, wager):
    print('start session I guess')
    if wager < 0:
        wager = 0
    # Get session
    is_new = False
    current_session = world_events.get_state('blackjack', user)
    if not current_session['status'] == 'saved':
        # session does not exist. Set deafult board state.
        is_new = True
        current_session = default_board_state
    elif not current_session['result'] == '':
        # last session is done.
        is_new = True
        current_session = default_board_state

    if command == 'reset':
        # Save "blank" board state as current state.
        current_session = default_board_state
        world_events.save_state('blackjack', user, current_session)
    elif not command == 'status':
        if is_new:
            if wager > 0:
                # Only withdraw from wallet if wager > 0
                wager = world_events.wallet_transaction(user, wager * -1, 'blackjack-wager')
            current_session['wager'] = wager
        # Play the game
        # play(board_state, player_action)
        current_session = play(current_session, command)
        # Evaluate result.
        if not current_session['result'] == '':
            # The match has ended. Check win, push, lose.


    # else:
    #     current_session['wager'] = wager


    return current_session



if __name__ == '__main__':
    myCard = deal_card.simple(deck_count)
    myVal = card_value(myCard, 12)
    # print('hand value: ', hand_value(test_hand))
    # sys.exit('temp breaking point')
    # print(myCard, '=', myVal)
    print('trying out the new loop')
    current_state = session('noob','hit',10)
    print(current_state)
    sys.exit()
    current_state = play({'state': 'blackjack', 'user': 'moo', 'status': 'none', 'result': ''}, '')
    while current_state['result'] == '':
        print(current_state)
        player_action = input('Action: ')
        while player_action not in valid_actions:
            print('Valid actions:', valid_actions)
            player_action = input('Action: ')
        current_state = play(current_state, player_action)
    print(current_state)
    