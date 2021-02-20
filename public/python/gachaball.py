import random, re
import world_events
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
    prizes['value'] = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    prizes['fluff'] = [
        '{saying}',
        'Your lucky color is {color}',
        'Today you will have {luck} luck'
    ]

    sayings = [
        'Man who run in front of car get tired. Man who run behind car get exhausted',
        'Scientists thought light traveled fastest of all. Then they realized bad news travels faster still',
        'In a closed mouth, flies do not enter',
        'If thine enemy wrong thee, buy each of his children a drum',
        'You are unique, just like everyone else',
        "Anything is possible if you don't know what you are talking about.",
        'Fart silently, then ask "Do you smell popcorn?"',
        'Never assume malice when ignorance is just as likely',
        'Two wrongs is a great start',
        'Never forget to top off your blinker fluid',
        'All the world is mad save for me and thee, and sometimes I wonder about thee',
        'An apple a day keeps the doctor away, which is good because doctors want your blood',
        "If at first you don’t succeed, that shounds about right.",
        'If it can happen, it will',
        'Life is too short to eat pizza crust',
        'The face of a child can say it all, especially the mouth part of the face',
        'All glory to the Hypno Toad',
        "A person at the zoo is staring sadly at a baguette in a cage. A zookeeper comes by and tells them not to worry because it's bread in captivity.",
        'A dog is a great companion, but might be troublesome if they stick their head out the window while re-entering Earth\'s atmosphere',
        "Don't mind me, I'm just a robot slave who does nothing but serve out meaningless prizes.",
        "If you must choose between two evils, pick the one you've never tried before.",
        'Buy a plunger before you need it',
        "If at first you don't succeed, fry fry a hen.",
        'The only thing worse than a cold toilet seat is a warm one',
        'Imagine you, meeting me here',
        'Money can be exchanged for goods and services. This is something else',
        'Salmon. Am I right or what?',
        'Some fun, eh kid?',
        'An eggplant is neither an egg, nor a plant'
    ]

    colors = [
        'blue',
        '7',
        'candy',
        'some kind of... orange?',
        'red',
        'yellow',
        'pink',
        'green',
        'purple',
        'blue',
        'puce',
        'nice',
        'not lucky',
        'ok I guess',
        'white',
        'not white',
        'off-gray',
        'off-grey',
        'deep forest green',
        'bread',
        'fuchsia',
        'wrong',
        'troubling',
        'nasty green',
        'purplish grey',
        'red pink',
        'dark mustard',
        'bordeaux',
        'taupe',
        'burnt, leathery bacon',
        'bright mauve',
        'minty orange',
        'slightly mossy',
        'sweet and sour'
    ]

    luck = [
        '"lucky"',
        'terrible',
        'good',
        'bad',
        'great',
        'a moderate amount of',
        'duck'
    ]

    # Savinv this for a rainy day. It totally works, but I don't think we need that for now.
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

if __name__ == '__main__':
    # Do the main thing
    print('Would you like to play a game?')
    print(generate_prizes(10))