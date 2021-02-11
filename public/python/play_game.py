import sys, getopt
import blackjack, world_events

valid_games = [
    'blackjack',
    'wallet'
]

validArgs =  "-h --help                                | Information about the script. \n"
validArgs += "-u <user name> --user <user name>        | The name of the user who is playing. \n"
validArgs += "-g <game name> --game <game name>        | The name of the game the user will play. \n"
validArgs += "-c <command val> --command <command val> | (Optional) The command to do for the game, if appropriate. \n"
validArgs += "-v <numeric val> --value <numeric val>   | (Optional) The amount to spend on the command. Some commands can use a default value. \n"

helpInfo  = "Help Info: \n"
helpInfo += "The front end for command line games. \n"
helpInfo += "Valid games are: " + str(valid_games) + " \n"


defaultLoginTimeout = 20

# Main function is only for getting arguments and setting variables so this script can run independently.

def main(argv):

    argsDict = {
        'user': '',
        'game': '',
        'command': '',
        'value': 0,
        'help': False # Not fully implemented
    }

    # get arguments
    try:
        opts, args = getopt.getopt(argv,'hu:g:c:v:',['help''user=','game=','command=','value='])
    except getopt.GetoptError:
        print('Unknown argument. Valid arguments: ' + validArgs)
        sys.exit(2)
    for opt, arg in opts: # Set the arguments as usable variables.
        if opt in ('-h', '--help'): # Print the usage when receiving -h
            print('Valid arguments: \n' + validArgs)
            print(helpInfo)
            sys.exit()
        elif opt in ('-u', '--user'):
            argsDict['user'] = arg.lower()
        elif opt in ('-g', '--game'):
            argsDict['game'] = arg.lower()
        elif opt in ('-c', '--command'):
            argsDict['command'] = arg.lower()
        elif opt in ('-v', '--value'):
            argsDict['value'] = int(arg)
    
    if argsDict['user'] == '':
        sys.exit('No user found. Use -u or --user')
    if argsDict['game'] == '':
        sys.exit('No password found. Use -g or --game')

    return argsDict
    # End main

def wallet_wrapper(user, command, value):
    valid_commands = ['inquiry', 'status', 'trash']
    result = ''
    if value > 0:
        world_events.wallet_transaction(user, value, 'source:play_game')
        result = 'Successfully added ' + str(value) + ' to wallet.'
    if command in valid_commands:
        co_result = ''
        if command == 'trash':
            world_events.wallet_transaction(user, -999999999999999 , 'source:play_game, trashing all points')
            co_result = 'Removing value from wallet. '
        co_result += 'Current balance: ' + str(world_events.wallet_transaction(user, 0, 'source:play_game'))

        if result == '':
            result = co_result
        else:
            result += ' ' + co_result
    elif value <= 0:
        result = 'Not a valid amount. Must be a number > 0'
    return result

# Need to debug this a bit more. Doesn't seem to update the state or do any playing at all. Just returns the old data.
def blackjack_wrapper(user, command, wager):
    app_name = 'blackjack'
    result = ''
    valid_commands = ['hit', 'stand', 'doubledown', 'status', 'reset']
    if command in valid_commands:
        # Proceed
        if command == 'reset':
            # Do reset
            world_events.reset_state(app_name, user)
            command == 'status'

        current_state = world_events.get_state(app_name, user)

        if command == 'status':
            result = str(current_state)
        else: # play the game
            # print('help me Im stuck', current_state['result'])
            if current_state['result'] == '':
                # continue existing game
                # Check if command is doubledown
                if command == 'doubledown':
                    # Check if last action was not stand or doubledown
                    # Also check if card count is exactly one.
                    if not current_state['player_last_action'] in ['stand','doubledown'] and len(current_state['player_hand'].split(',')) == 1:
                        # Now confirm that they actually have enough to wager...
                        if wager > 0:
                            player_balance = world_events.wallet_transaction(user, 0, app_name + '-confirming wager')
                            if player_balance >= current_state['wager']:
                                # Now withdraw current wager amount.
                                confirm_wager = world_events.wallet_transaction(user, current_state['wager'] * -1, app_name + '-doubledown wager')
                                current_state['wager'] += confirm_wager
                            else:
                                # Not enough balance to double down. Change command to hit
                                command = 'hit'
                new_state = blackjack.play(current_state, command)
            else:
                # print('wager:', str(wager))
                if wager > 0:
                    confirm_wager = world_events.wallet_transaction(user, wager * -1, app_name + '-starting wager')
                else:
                    confirm_wager = 0
                # print('confirm_wager:', str(confirm_wager))
                new_state = blackjack.play({'status':'none', 'wager': confirm_wager}, command)
                # print('new_state[wager]:', str(new_state['wager']))
                # Withdraw the wager

            world_events.save_state(app_name, user, new_state)
            result = new_state

            match_result = new_state['result']
            if not match_result == '':
                # print('hi')
                # push
                if match_result == 'push':
                    # Person gets the wager back.
                    world_events.wallet_transaction(user, current_state['wager'], app_name + '-push return')
                # win
                elif match_result == 'win':
                    # Person gets wager + wager * bet_return.
                    winnings = current_state['wager'] + current_state['wager'] * current_state['bet_return']
                    # print('wager:', str(current_state['wager']))
                    # print('winnings:', str(winnings))
                    test_value = world_events.wallet_transaction(user, winnings, app_name + '-winnings')
                    # print('deposit result:', str(test_value))
                # lose
                else:
                    # Deposit wager in house wallet.
                    world_events.wallet_transaction(app_name + '-house', current_state['wager'], app_name + '-house gains from player ' + user)

    else:
        # Give a hint...
        result = 'Valid blackjack commands:' + str(valid_commands) + '\n'
        result += 'user: ' + user + ' command: ' + command
    # {'player_hand_val': 18, 'dealer_hand_val': 26, 'player_hand': 'A-h,2-c,J-d,5-d', 'dealer_hand': '5-d,5-s,6-d,K-c', 'player_last_action': 'stand', 'dealer_last_action': 'stand', 'result': 'win', 'bet_return': 1, 'status': ''}
    
    return result



if __name__ == '__main__':
    # Run this with creds built in.
    settingsDict = main(sys.argv[1:])
    if settingsDict['game'] == 'blackjack':
        if settingsDict['value'] < 0:
            settingsDict['value'] = 0
        result = blackjack_wrapper(settingsDict['user'], settingsDict['command'], settingsDict['value'])
        print(result)

    elif settingsDict['game'] == 'wallet':
        result = wallet_wrapper(settingsDict['user'], settingsDict['command'], settingsDict['value'])
        print(result)
    # print(settingsDict)
