import sys, getopt
import blackjack, world_events, gachaball

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

    if False: # Thank you, I hate it.
        print(args)

    return argsDict
    # End main

def wallet_wrapper(user, command, value):
    valid_commands = ['inquiry', 'status', 'reset']
    result = ''
    if value > 0:
        world_events.wallet_transaction(user, value, 'source:play_game')
        result = 'Successfully added ' + str(value) + ' to wallet.'
    if command in valid_commands:
        co_result = ''
        if command == 'reset':
            world_events.wallet_transaction(user, -999999999999999 , 'source:play_game, trashing all points')
            co_result = 'Removing value from wallet. '
        co_result += 'Current balance: ' + str(world_events.wallet_transaction(user, 0, 'user inquiry'))

        if result == '':
            result = co_result
        else:
            result += ' ' + co_result
    elif value < 0:
        world_events.wallet_transaction(user, value, 'source:play_game')
        result = 'Successfully withdrew ' + str(value) + ' from wallet.'
    return result

# Need to debug this a bit more. Doesn't seem to update the state or do any playing at all. Just returns the old data.
def blackjack_wrapper(user, command, wager, is_single_line):
    result = ''
    is_single = False
    if is_single_line:
        is_single = True
    # Come back to this. I rebuilt this code as part of the blackjack script.
    # session(user, command, wager)
    if command == 'help':
        result = '@' + user + ' Blackjack commands: help, status, hit, hit <wager>, doubledown, stand'
    else:
        current_state = blackjack.session(user, command, wager)
        result = blackjack.render_result(current_state, is_single)
    
    return result
    # return blackjack.render_result(blackjack.session(user, command, wager), is_single)

def gacha_wrapper(user, command, value):
    result = gachaball.play(user)
    return result



if __name__ == '__main__':
    # Run this with creds built in.
    settingsDict = main(sys.argv[1:])
    if settingsDict['game'] == 'blackjack':
        if settingsDict['value'] < 0:
            settingsDict['value'] = 0
        result = blackjack_wrapper(settingsDict['user'], settingsDict['command'], settingsDict['value'], True)
        print(result)

    elif settingsDict['game'] == 'wallet':
        result = wallet_wrapper(settingsDict['user'], settingsDict['command'], settingsDict['value'])
        print(result)

    elif settingsDict['game'] == 'gacha':
        result = gacha_wrapper(settingsDict['user'], settingsDict['command'], settingsDict['value'])
        print(result)
    # print(settingsDict)
