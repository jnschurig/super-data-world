import random, re
import world_events

app_name = 'scramble'



def generate_prize(length, height):
    values = [10, 100, 500]
    multiplier_range = [1, 5]
    prize = {
        'x': random.randint(2, length-1),
        'y': random.randint(2, height-1),
        'value': values[random.randint(1, len(values)) - 1] * multiplier_range[random.randint(1, len(multiplier_range)) - 1]
    }
    return prize

def generate_board(length, height, density):
    
    board = {}
    board['length'] = length
    board['height'] = height 
    board['prizes'] = []
    board['players'] = []

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

def play(user, move):
    
    current_state = world_events.get_persistence(app_name, 'system')
    if current_state['result'] in ['', 'finished']:
        # Start a new state.
        current_state = generate_board(15, 15, 10)
        current_state['result'] = 'in progress'
    world_events.save_state(app_name, 'system', current_state)
    
def register_player(user):
    current_state = world_events.get_persistence(app_name, 'system')
    if current_state['result'] == 'in progress':
        # Check if user is in the list of users.
        if user not in current_state['players']:
            current_state['players'].append(user)
            # Calculate distance between x and either wall, and y and either floor / ceiling
            # right wall
            # 1 = left, 2 = top, 3 = right, 4 = bottom
            surface_index = random.randint(1, 4)
            if surface_index % 2 == 1:
                # Set random vertical position
                starting_y = random.randint(1, current_state['height'])
                if surface_index <= 2:
                    # is left wall
                    starting_x = 1
                else:
                    # is right wall
                    starting_x = current_state['length']
            else:
                # set horizontal position
                starting_x = random.randint(1, current_state['length'])
                if surface_index <= 2:
                    # is top wall
                    starting_y = 1
                else:
                    # is bottom wall
                    starting_y = current_state['height']
            starting_position = [starting_x, starting_y]
            print(starting_position)


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
    
    while y < board['height']:
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
    

    # Iterate through the rows and columns and replace empty characters with an item.
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
    my_board = generate_board(10, 10, 10)
    print(my_board)
    print(render_map(my_board))
    play('james', 'u')
    register_player('james')