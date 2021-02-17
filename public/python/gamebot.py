# Remember to pip install twitchio

import os, json
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
    await ws.send_privmsg(creds['channel'], f"/me is open for business!")

@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == creds['user'].lower():
        return

    # await ctx.channel.send(ctx.content)
    await bot.handle_commands(ctx)

@bot.command(name='test')
async def test(ctx):
    await ctx.send('test passed!')

@bot.command(name='blackjack')
async def twitch_bj(ctx):
    #blackjack_wrapper(user, command, wager)
    command_args = ctx.content.split(' ')
    print(command_args)
    if len(command_args) > 2:
        result = play_game.blackjack_wrapper(ctx.author.name.lower(), command_args[1], command_args[2], True)
    else:
        result = play_game.blackjack_wrapper(ctx.author.name.lower(), command_args[1], 0, True)
    await ctx.send(result)

# @bot.command(name='blackjack')
# async def twitch_bj(ctx):
#     #blackjack_wrapper(user, command, wager)
#     command_args = ctx.content.split(' ')
#     print(command_args)
#     if len(command_args) > 2:
#         await ctx.send(play_game.blackjack_wrapper(ctx.author.name.lower(), command_args[1], command_args[2], True))
#     else:
#         await ctx.send(play_game.blackjack_wrapper(ctx.author.name.lower(), command_args[1], 0, True))
#     # await ctx.send(result)


# bot.py
if __name__ == "__main__":
    bot.run()
