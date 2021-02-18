# Remember to pip install twitchio

import os, json, sys
from twitchio.ext import commands
import play_game

with open('gamebot_credentials.json', 'r', encoding='utf-8') as f:
    creds = json.load(f)

bot = commands.Bot(
    irc_token=creds['oauth'],
    client_id=creds['client'],
    nick=creds['user'],
    prefix='!',
    initial_channels=[creds['channel']]
)

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{creds['user']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(creds['channel'], f"/me starting now.")

@bot.event
async def event_message(ctx):
    # Runs every time a message is sent in chat.
    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == creds['user'].lower():
        return

    if 'are you ready' in ctx.content.lower():
        await ctx.channel.send("Yes I'm ready!")

    # await ctx.channel.send(ctx.content)
    await bot.handle_commands(ctx)

@bot.command(name='me')
async def about_me(ctx):
    attr_list = []
    if ctx.author.is_mod:
        attr_list.append('Channel mod')
    if ctx.author.is_subscriber:
        attr_list.append('Subscriber')
    if ctx.author.is_turbo:
        attr_list.append('Turbo User')
    message = 'User ' + ctx.author.name + ' is: ' + str(attr_list).replace('[','').replace(']','').replace("'",'')
    await ctx.send(message)

@bot.command(name='info')
async def info_help(ctx):
    message = 'Play !games and check your !wallet. Use !resetwallet get started or set your current balance to 500.'
    command_args = ctx.content.split(' ')
    if len(command_args) > 1:
        message = '@' + command_args[1] + ' ' + message
    await ctx.send(message)

@bot.command(name='games')
async def games_info(ctx):
    message = '!blackjack (more games coming soon™)'
    await ctx.send(message)

@bot.command(name='wallet')
async def wallet_status(ctx):
    message = ''
    command_args = ctx.content.split(' ')
    if len(command_args) == 1:
        message = '@' + ctx.author.name + ' ' + play_game.wallet_wrapper(ctx.author.name.lower(), 'status', 0)
    elif ctx.author.is_mod:
        if len(command_args) == 3:
            message = '@' + command_args[1] + ' ' + play_game.wallet_wrapper(command_args[1], 'mod transaction', int(command_args[2]))
        else:
            message = 'Usage: !wallet <user> <amount>'
    else:
        message = 'Must be a mod for advanced usage of !wallet command'
    await ctx.send(message)

@bot.command(name='resetwallet')
async def wallet_reset(ctx):
    play_game.wallet_wrapper(ctx.author.name.lower(), 'reset', 0)
    play_game.wallet_wrapper(ctx.author.name.lower(), 'deposit', 500)
    await ctx.send(play_game.wallet_wrapper(ctx.author.name.lower(), 'status', 0))

@bot.command(name='blackjack')
async def twitch_bj(ctx):
    #blackjack_wrapper(user, command, wager)
    command_args = ctx.content.split(' ')
    print(command_args)
    if len(command_args) == 1:
        result = play_game.blackjack_wrapper(ctx.author.name.lower() , 'status', 0, True)
    elif len(command_args) > 2:
        result = play_game.blackjack_wrapper(ctx.author.name.lower(), command_args[1], command_args[2], True)
    else:
        result = play_game.blackjack_wrapper(ctx.author.name.lower(), command_args[1], 0, True)
    await ctx.send(result)

@bot.command(name='shutdown')
async def shut_me_down(ctx):
    command_args = ctx.content.split(' ')
    message = ''
    approved_list = ['reaif','tranquilite']
    do_shutdown = False
    if ctx.author.name.lower() in approved_list:
        if len(command_args) > 1:
            if command_args[1].lower() == 'please':
                message = 'Goodbye :('
                do_shutdown = True
            else:
                message = "I don't know what you mean."
        else:
            message = "You didn't say the magic word."
    else:
        message = 'You must be very special to run this command.'
    await ctx.send(message)
    if do_shutdown:
        sys.exit('Received shutdown command')


# bot.py
if __name__ == "__main__":
    bot.run()
