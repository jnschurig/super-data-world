import sys
import deal_card, world_events

valid_actions = [
    'hit',
    'stand',
    'doubledown'
    # 'reset',
    # 'status'
]

deck_count = 8

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
    # wager = board_state['wager']

    # if board_state['status'] == 'none':
    #     board_state = default_board_state
    #     board_state['wager'] = wager
    dealer_max = 17
    default_return = 1
    
    dealer_action = 'hit'

    board_state["bet_return"] = default_return
    board_state["result"] = ''
    # if not board_state['result'] == '':
    #     board_state = default_board_state

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
        # For now, true blackjack is only two cards.
        elif board_state["player_hand_val"] == 21 and len(board_state["player_hand"].split(',')) == 2:
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
    app_name = 'blackjack'

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

    wager = int(wager)
    if wager < 0:
        wager = 0
    # Get session
    current_session = []
    current_session = world_events.get_state(app_name, user)
    # 'none' status indicates no save data.
    # result != '' indicates a previously finished game.
    if current_session['status'] == 'none' or not current_session['result'] == '':
        # Reset board state
        current_session = default_board_state
        current_session['user'] = user 
        current_session['status'] = ''

    if current_session['player_hand'] == '':
        if wager > 0:
            # wallet_transaction(user_name, transaction_amount, transaction_comment)
            wager = world_events.wallet_transaction(user, wager * -1, app_name + '-initial wager')
        current_session['wager'] = wager

        # This is the only time we reset the wager.
        # Otherwise we only carry it through from the loaded state.

    if command == 'reset':
        # Reset to default. Don't play the game.
        current_session = world_events.save_state(app_name, user, default_board_state)
    elif command == 'status':
        print('status')
    else:
        # Check if command is double down and if the card count == 1. Then double the wager if so.
        if command == 'doubledown' and len(current_session['player_hand'].split(',')) == 1:
            current_session['wager'] += world_events.wallet_transaction(user, current_session['wager'] * -1, app_name + '-doubledown wager')
        # Play the game
        current_session = play(current_session, command)

    # Finished playing. Set 
    if not current_session['result'] == '':
        # The match has ended. Check win, push, lose.
        # Also deposite winnings.
        session_result = current_session['result']
        winnings = 0
        if session_result == 'win':
            winnings = current_session['wager'] + (current_session['wager'] * current_session['bet_return'])
        elif session_result == 'push':
            winnings = current_session['wager']
        world_events.wallet_transaction(user, winnings, app_name + '-winnings')
        current_session['winnings'] = winnings
    # All done here
    # save_state(state_name, user_name, state_data)
    if command in valid_actions:
        world_events.save_state(app_name, user, current_session)
    return current_session

def render_result(board_state, is_single_line):
    is_single = False
    if is_single_line:
        is_single = True
    render = ''
    if board_state['player_hand'] == '':
        render = 'Dealer: [] = 0 | '
        render += '@' + board_state['user'] + ' [] = 0'
    elif is_single:
        char = {
            'h': '♥️',
            'd': '♦️',
            'c': '♣️',
            's': '♠️'
        }

        render += 'Dealer: '
        # Start assembling cards...
        for i in board_state['dealer_hand'].split(','):
            card = i.split('-')
            use_card = '[' + card[0] + char[card[1]] + ']'
            render += use_card
        
        render += ' = ' + str(board_state['dealer_hand_val'])

        render += ' | @' + board_state['user'] + ': '

        for i in board_state['player_hand'].split(','):
            card = i.split('-')
            use_card = '[' + card[0] + char[card[1]] + ']'
            render += use_card
        
        render += ' = ' + str(board_state['player_hand_val'])


        if board_state['result'] == 'win':
            render += ' | Win!'
            if not board_state['winnings'] == 0:
                render += ' wager + winnings = ' + str(board_state['winnings'])
        elif board_state['result'] == 'lose':
            render += ' | Lose...'
            if not board_state['wager'] == 0:
                render += ' lost wager = ' + str(board_state['wager'])
        elif board_state['result'] == 'push':
            render += ' | Push.'
            if not board_state['wager'] == 0:
                render += ' wager returned = ' + str(board_state['wager'])

    else:
        char = {
            'h': '♥',
            'd': '♦',
            'c': '♣',
            's': '♠',
            'br': '┘',
            'bl': '└',
            'tr': '┐',
            'tl': '┌'
        }
        
        row_count = 11 # Max number of rows of text
        idx = 0
        row = []
        while idx < row_count:
            row.append('')
            idx += 1
        
        # Assign values to each row.

        row[1] = 'Dealer - ' + str(board_state['dealer_hand_val'])
        for i in board_state['dealer_hand'].split(','):
            card = i.split('-')
            row[2] += char['tl'] + '---' + char['tr']
            row[3] += '|' + card[0].ljust(2) + char[card[1]] + '|'
            row[4] += char['bl'] + '---' + char['br']
        
        row[6] = board_state['user'] + ' - ' + str(board_state['player_hand_val'])
        
        for i in board_state['player_hand'].split(','):
            card = i.split('-')
            row[7] += char['tl'] + '---' + char['tr']
            row[8] += '|' + card[0].ljust(2) + char[card[1]] + '|'
            row[9] += char['bl'] + '---' + char['br']
        
        
        result = board_state['result']
        if result == 'win':
            result = 'Win!'
        elif result == 'push':
            result = 'Push'
        elif result == 'lose':
            result = 'Lose'
        row[10] = result 

        # Center align every row of text.
        longest_line = max(len(row[2]), len(row[7]))
        row[0] = ''.rjust(longest_line, '-')
        
        idx = 0
        for i in row:
            row[idx] = i.rjust(int(longest_line/2) + int(len(i)/2))
            idx += 1
        
        # Add new lines to each row and assign to the render.
        for i in row:
            render += i + '\n'
            
    return render



if __name__ == '__main__':
    myCard = deal_card.simple(deck_count)
    myVal = card_value(myCard, 12)
    # print('hand value: ', hand_value(test_hand))
    # sys.exit('temp breaking point')
    # print(myCard, '=', myVal)
    
    clean_board_state = {
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

    # print('trying out the new loop')
    # current_state = session('noob','hit',10)
    # print(current_state)
    # sys.exit()
    play_mode = input('session, play, or render: ').lower()
    if play_mode == 'play':
        current_state = clean_board_state
        current_state = play(clean_board_state, 'hit')
        while current_state['result'] == '':
            print(current_state)
            player_action = input('Action: ')
            while player_action not in valid_actions:
                print('Valid actions:', valid_actions)
                player_action = input('Action: ')
            current_state = play(current_state, player_action)
        print(current_state)
    elif play_mode == 'render':
        current_state = world_events.get_state('blackjack', 'noob')
        # print(current_state)
        print(render_result(current_state, True))
    else:
        wager = input('wager? ')
        current_state = session('my user', 'reset', wager)
        while current_state['result'] == '':
            command = input('Command? ')
            current_state = session('my user', command, wager)
            print(current_state)
    
    