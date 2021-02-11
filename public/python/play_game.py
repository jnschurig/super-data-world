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
    result = ''
    valid_commands = ['hit', 'stand', 'doubledown', 'status']
    if command in valid_commands:
        # Proceed
        current_state = world_events.get_state('blackjack', user)
        if command == 'status':
            result = str(current_state)
        else: # play the game
            # print('help me Im stuck', current_state['result'])
            if current_state['result'] == '':
                # continue existing game
                new_state = blackjack.play(current_state, command)
            else:
                new_state = blackjack.play({'status':'none', 'wager': wager}, command)
                # Spend the wager
            world_events.save_state('blackjack', user, new_state)
            result = new_state

            match_result = new_state['result']
            if not match_result == '':
                print('hi')
                # push
                    # Person gets the wager back.
                # win
                    # Withdraw wager * bet_return from house wallet.
                    # Person gets wager + wager * bet_return.
                # lose
                    # Deposit wager in house wallet.

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
        result = blackjack_wrapper(settingsDict['user'], settingsDict['command'], settingsDict['value'])
        print(result)

    elif settingsDict['game'] == 'wallet':
        result = wallet_wrapper(settingsDict['user'], settingsDict['command'], settingsDict['value'])
        print(result)
    # print(settingsDict)
