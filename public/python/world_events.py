import os, re, json, hashlib
# import sys
from datetime import datetime
from pathlib import Path

data_dir_name = 'data'
event_dir_name = 'events'
state_dir_name = 'state'

# print(os.path.realpath(__file__))

scriptDir = os.path.dirname(os.path.realpath(__file__))
data_dir = scriptDir + os.sep + data_dir_name

def create(event_name, event_data):
    # Date related variables
    now = datetime.now()
    dirDate = now.strftime('%Y%m%d')
    hashSalt = now.strftime('%Y%m%d_%H%M%S_%f')
    eventDate = now.strftime('%Y-%m-%d %H:%M:%S.%f %z').strip()

    clean_event = event_name
    clean_event = re.sub('\\s','_', clean_event) # Replace whitespace with underscores.
    clean_event = re.sub('\\W','' , clean_event) # Remove non-word characters.
    clean_event = re.sub('_*$','' , clean_event) # Remove trailing underscores.
    clean_event = re.sub('^_*','' , clean_event) # Remove preceeding underscores.

    file_name = clean_event
    if not event_data['user'] == '':
        file_name += '_' + event_data['user']
    file_name += '_' + hashSalt + '.json'

    output_file = data_dir + os.sep + event_dir_name + os.sep + clean_event + os.sep + dirDate + os.sep + file_name
    
    # Create event ID
    preHash = event_name + ' ' + hashSalt
    event_id = hashlib.md5(preHash.encode()).hexdigest()
    event_data['id'] = event_id
    event_data['event_name'] = event_name
    event_data['event_date'] = eventDate

    # output the file
    Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(event_data, f, ensure_ascii=False, indent=4)
    return output_file

def get_state(state_name, user_name):
    # print('get_state')
    input_file = data_dir + os.sep + state_dir_name + os.sep + state_name + os.sep + state_name + '_' + user_name + '.json'

    default_state = {
        "state": state_name,
        "user": user_name,
        "status": "none"
    }
    current_state = default_state
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            current_state = json.load(f)
    return current_state

def save_state(state_name, user_name, state_data):
    state_data['state'] = state_name
    state_data['user'] = user_name
    output_file = data_dir + os.sep + state_dir_name + os.sep + state_name + os.sep + state_name + '_' + user_name + '.json'

    Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(state_data, f, ensure_ascii=False, indent=4)
    return output_file
    

if __name__ == "__main__":
#    main(sys.argv[1:])
    # myEventData = create('wallet', {"user": "james", "status": "winnings", "amount": 20})
    # print(myEventData)
    # myState = {
    #     'player_hand_val': 19, 'dealer_hand_val': 17, 'player_hand': '9-c,2-s,8-d', 'dealer_hand': '9-s,8-d', 'player_last_action': 'stand', 'dealer_last_action': 'stand', 'result': 'win', 'bet_return': 1
    # }
    # result = save_state('blackjack', 'james', myState)
    # print(result)
    result_two = get_state('wallet','james')
    print(result_two)