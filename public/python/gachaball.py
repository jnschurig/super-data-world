import random, re
import world_events, constants
import urllib.request

# Check for gacha list existence.
# If exists, load it.
# If not exists, generate it.
# Take n amount of wallet monies, return m number of gachas.
# Write gacha state to disk.

def generate_prizes(count):
    # Here we go.
    # prize_cost = 50
    # starting_number = 50
    prizes = {}
    prizes['value'] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 115, 135]
    prizes['fluff'] = [
        '{saying}',
        'Your lucky color is {color}',
        'Today you will have {luck} luck'
    ]
    sayings = constants.GACHA_SAYINGS
    colors = constants.GACHA_COLORS
    luck = constants.GACHA_LUCK

    # Saving this for a rainy day. It totally works, but I don't think we need that for now.
    # color_url = 'https://xkcd.com/color/rgb.txt'
    # contents = urllib.request.urlopen(color_url).read()
    # contents = str(contents)
    # contents = re.sub('#......','',contents.replace('\\t\\n',',').replace('\\t',''))
    # color_list = contents.split(',')
    # print(color_list)


    prize_list = []
    
    i = 0
    while i < count:
        offset = random.randint(-4, 5) 
        random_val = random.randint(1, len(prizes['value'])) - 1
        random_fluff = random.randint(1, len(prizes['fluff'])) - 1
        random_color = colors[random.randint(1, len(colors)) - 1]
        random_luck = luck[random.randint(1, len(luck)) - 1]
        random_saying = sayings[random.randint(1, len(sayings)) - 1]
        # print(random_val)
        # print(random_fluff)
        # print(prizes['fluff'][27].format(color = random_color)) # 27, 28
        one_prize = [
            prizes['value'][random_val] + offset, 
            prizes['fluff'][random_fluff].format(luck = random_luck, color = random_color, saying = random_saying)
        ]
        prize_list.append(one_prize)

        i += 1
    
    return prize_list

def play(user):
    default_gacha_count = 50
    default_gacha_cost = 50
    app_name = 'gacha'
    prize_text = '@' + user
    # If the user has enough in their account, proceed.
    if default_gacha_cost <= world_events.wallet_transaction(user, 0, app_name):
        world_events.wallet_transaction(user, default_gacha_cost * -1, app_name)
        current_session = world_events.get_persistence(app_name, 'system')
        if current_session['status'] == 'none':
            # Generate a new list.
            current_session['pool'] = generate_prizes(default_gacha_count)
        elif len(current_session['pool']) == 0:
            current_session['pool'] = generate_prizes(default_gacha_count)

        # Random number
        prize_number = random.randint(1, len(current_session['pool'])) - 1
        # Assign prize from pool
        prize = current_session['pool'][prize_number]
        # Remove prize from current pool
        current_session['pool'].remove(prize)
        world_events.save_state(app_name, 'system', current_session)

        world_events.wallet_transaction(user, prize[0], app_name)

        prize_text += ' you get ' + str(prize[0]) + '! ' + prize[1]
    else:
        prize_text += " you don't have enough in your wallet..."
    return prize_text

        # length of current_pool...


if __name__ == '__main__':
    # Do the main thing
    # print('Would you like to play a game?')
    # print(generate_prizes(10))
    user_name = input('User: ')
    print(play(user_name))