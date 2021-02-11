import sys, getopt
import blackjack, world_events

valid_games = [
    'blackjack'
]

validArgs =  "-h <game name> --help <game name>        | Information about the script. \n"
validArgs += "-u <user name> --user <user name>        | The name of the user who is playing. \n"
validArgs += "-g <game name> --game <game name>        | The name of the game the user will play. \n"
validArgs += "-c <command val> --command <command val> | (Optional) The command to do for the game, if appropriate. \n"

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
        'help': False # Not fully implemented
    }

    # get arguments
    try:
        opts, args = getopt.getopt(argv,'hu:g:c:',['help''user=','game=','command='])
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
    
    if argsDict['user'] == '':
        sys.exit('No user found. Use -u or --user')
    if argsDict['game'] == '':
        sys.exit('No password found. Use -g or --game')

    return argsDict
    # End main

# Need to debug this a bit more. Doesn't seem to update the state or do any playing at all. Just returns the old data.
def blackjack_wrapper(user, command):
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
                new_state = blackjack.play({'status':'none'}, command)
            world_events.save_state('blackjack', user, new_state)
            result = new_state
    else:
        # Give a hint...
        result = 'Valid blackjack commands:' + str(valid_commands) + '\n'
        result += 'user: ' + user + ' command: ' + command
    return result

if __name__ == '__main__':
    # Run this with creds built in.
    settingsDict = main(sys.argv[1:])
    if settingsDict['game'] == 'blackjack':
        result = blackjack_wrapper(settingsDict['user'], settingsDict['command'])
        print(result)
    # print(settingsDict)
