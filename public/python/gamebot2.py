'''
Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance with the License. A copy of the License is located at
    http://aws.amazon.com/apache2.0/
or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
'''

import sys, json, re
import irc.bot
import requests
import play_game

with open('gamebot_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)


class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, client_id, token, channel):
        self.client_id = client_id
        self.token = token
        self.channel = channel

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel.replace('#','')
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        # print(r)
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 6667
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, token)], username, username)
        

    def on_welcome(self, c, e):
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):

        # If a chat message starts with an exclamation point, try to run it as a command
        if e.arguments[0][:1] == '!':
            cmd = e.arguments[0].split(' ')[0][1:]
            msg = e.arguments[0]
            print('Received command: ' + cmd + msg.replace('!'+cmd,''))
            # print(e)
            self.do_command(e, cmd, msg)
        return

    def do_command(self, e, cmd, msg):
        c = self.connection

        # chat_user = re.sub('!.*','',re.sub('.*?source: ','',str(e)))
        chat_user = re.sub('!.*','',str(e.source))
        local_args = msg.split(' ')
        # print(str(self))

        # Poll the API to get current game.
        if cmd == "game":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])

        # Poll the API the get the current status of the stream
        elif cmd == "title":
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])

        elif cmd == "test":
            c.privmsg(self.channel, 'User=' + chat_user + ' command=' + cmd + ' msg=' + msg)

        elif cmd == "blackjack":
            while len(local_args) < 3:
                local_args.append(0)
            game_result = play_game.blackjack_wrapper(chat_user.lower(), local_args[1], local_args[2], True)
            c.privmsg(self.channel, game_result)

        # The command was not recognized
        else:
            c.privmsg(self.channel, "Did not understand command: " + cmd)

def main():
    # if len(sys.argv) != 5:
    #     print("Usage: twitchbot <username> <client id> <token> <channel>")
    #     sys.exit(1)

    # username  = sys.argv[1]
    # client_id = sys.argv[2]
    # token     = sys.argv[3]
    # channel   = sys.argv[4]

    username  = creds['user']
    client_id = creds['client']
    token     = creds['oauth']
    channel   = creds['channel']


    bot = TwitchBot(username, client_id, token, channel)
    bot.start()

if __name__ == "__main__":
    main()