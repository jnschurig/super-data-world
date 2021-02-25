import random, re

def generate_prize(length, height):
    values = [10, 100, 500]
    multiplier_range = [1, 5]
    prize = {
        'x': random.randint(1, length-1),
        'y': random.randint(1, height-1),
        'value': values[random.randint(1, len(values)) - 1] * multiplier_range[random.randint(1, len(multiplier_range)) - 1]
    }
    return prize

def generate_board(length, height, density):
    
    board = {}
    board['length'] = length
    board['height'] = height 
    board['prizes'] = []

    i = 0
    while i <= density:
        #random.randint(1, len(prizes['fluff'])) - 1
        prize = generate_prize(length, height)

        j = 0
        while j < len(board['prizes']):
            # Check this prize against the others.
            while prize['x'] == board['prizes'][j]['x'] and prize['y'] == board['prizes'][j]['y']:
                # If this prize has the same dimensions, re-generate until it no longer does.
                prize = generate_prize(length, height)

            j += 1
        # Done checking prize. Assign to the list.
        
        board['prizes'].append(prize)

        i += 1
    # Done making prizes. Add a boss?


    return board

def render_map(board):
    result = ''
    char = {
            'br': '┘',
            'bl': '└',
            'tr': '┐',
            'tl': '┌'
        }
    
    x = 0
    y = 0

    render = []
    # make first row with nothing
    row = []
    row.append(char['tl'])
    while x < board['length']:
        row.append('--')
        x += 1
    row.append(char['tr'])
    render.append(row)
    # First row done. Now fill an empty grid inside.
    
    while y <= board['height']:
        x = 0
        row = []
        row.append('|')
        while x < board['length']:
            row.append('  ')
            x += 1
        row.append('|')
        render.append(row)
        y += 1
    
    # Do the last row like the first.    
    row = []
    row.append(char['bl'])
    x = 0
    while x < board['length']:
        row.append('--')
        x += 1
    row.append(char['br'])
    render.append(row)
    # First row done. Now fill an empty grid inside.
    

    # Iterate through the rows and columns and replace empty characters with a circle.
    for i in board['prizes']:
        render[i['y']][i['x']] = '[]'

    for i in render:
        # now in a row
        for j in i:
            # now looking at a column in that row
            result += j
        result += '\n'
    # print('hi')


    return result

if __name__ == '__main__':
    # Do the main thing
    my_board = generate_board(50, 15, 10)
    print(my_board)
    print(render_map(my_board))