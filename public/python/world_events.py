import os, re, json, hashlib
# import sys
from datetime import datetime
from pathlib import Path

data_dir_name = 'data'
event_dir_name = 'events'
state_dir_name = 'state'
wallet_dir_name = 'wallet'


# print(os.path.realpath(__file__))

scriptDir = os.path.dirname(os.path.realpath(__file__))
data_dir = scriptDir + os.sep + data_dir_name

def create(event_name, event_data):
    # Date related variables
    now = datetime.now()
    dirDate = now.strftime('%Y%m%d_%H00')
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
    # input_file = data_dir + os.sep + state_dir_name + os.sep + state_name + os.sep + state_name + '_' + user_name + '.json'
    input_dir = data_dir + os.sep + event_dir_name + os.sep + state_name

    default_state = {
        "state": state_name,
        "user": user_name,
        "status": "none",
        "result": ""
    }

    latest_file = ''
    latest_timestamp = 0

    with os.scandir(input_dir) as entries:
        for entry in entries:
            # This is one level down, which I know is empty of actual files.
            # Moving to subdirectories.
            if not os.path.isfile(entry.path):
                # Scan sub directories...
                with os.scandir(entry.path) as sub_entries:
                    for entry in sub_entries:
                        # Check if the statename and the user name are both in the file name.
                        if state_name in entry.name and user_name in entry.name:
                            # Iterate through each file looking for the latest modified time and setting the file if so.
                            if entry.stat().st_mtime > latest_timestamp:
                                latest_timestamp = entry.stat().st_mtime
                                latest_file = entry.path
    
    current_state = default_state
    if not latest_file == '': # We have a valid file...
        with open(latest_file, 'r', encoding='utf-8') as f:
            current_state = json.load(f)
            f.close()
    return current_state

def get_persistence(state_name, user_name):
    # print('get_state')
    input_file = data_dir + os.sep + state_dir_name + os.sep + state_name + os.sep + state_name + '_' + user_name + '.json'

    default_state = {
        "state": state_name,
        "user": user_name,
        "status": "none",
        "result": ""
    }
    current_state = default_state
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8') as f:
            current_state = json.load(f)
            f.close()
    return current_state

def save_state(state_name, user_name, state_data):
    state_data['state'] = state_name
    state_data['user'] = user_name
    state_data['status'] = 'saved'
    output_file = data_dir + os.sep + state_dir_name + os.sep + state_name + os.sep + state_name + '_' + user_name + '.json'

    Path(os.path.dirname(output_file)).mkdir(parents=True, exist_ok=True)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(state_data, f, ensure_ascii=False, indent=4)
            f.close()
    except:
        state_data['status'] = 'error'

    create(state_name, state_data)
    return state_data

def reset_state(state_name, user_name):
    default_state = {
        "state": state_name,
        "user": user_name,
        "status": "reset",
        "result": ""
    }

    reset_file = data_dir + os.sep + state_dir_name + os.sep + state_name + os.sep + state_name + '_' + user_name + '.json'
    if os.path.exists(reset_file):
        with open(reset_file, 'r', encoding='utf-8') as f:
            current_state = json.load(f)
        current_state['file_name'] = reset_file
        print('removing state file...', reset_file)
        os.remove(reset_file)
    else:
        current_state = default_state
    create('reset-' + state_name, current_state)
    return reset_file

# def delete_state(state_name, user_name):
#     delete_file = data_dir + os.sep + state_dir_name + os.sep + state_name + os.sep + state_name + '_' + user_name + '.json'
#     if os.path.exists(delete_file):
#         os.remove(delete_file)
#     return delete_file
    
def wallet_transaction(user_name, transaction_amount, transaction_comment):
    # returns the balance on deposits and inqueries (0 transactions).
    # returns the amount withdrawn on withdrawls.
    
    result = 0
    
    transaction_type = ''
    if transaction_amount > 0:
        transaction_type = 'deposit'
    elif transaction_amount < 0:
        transaction_type = 'withdrawl'
    else:
        transaction_type = 'inquiry'

    wallet_file = data_dir + os.sep + wallet_dir_name + os.sep + user_name + '-wallet.txt'

    Path(os.path.dirname(wallet_file)).mkdir(parents=True, exist_ok=True)
    file_mode = 'w+'
    if os.path.isfile(wallet_file):
        file_mode = 'r+'
    with open(wallet_file, file_mode) as f:
        file_data = f.read()
        # print(file_data)
        if file_data == '':
            balance = float(0)
        else:
            balance = float(file_data.strip())
        balance = int(balance)
        if transaction_type == 'withdrawl':
            if abs(transaction_amount) > balance:
                transaction_amount = balance * -1
                balance = 0
            else:
                balance += int(transaction_amount)
            result = abs(int(transaction_amount))
        else:
            balance += int(transaction_amount)
            result = balance

        f.seek(0)
        f.write(str(balance))
        f.truncate()
    
    event_data = {
        'user':user_name, 
        'wallet_transaction': transaction_type, 
        'transaction_amount': int(transaction_amount), 
        'balance': balance, 
        'transaction_comment': transaction_comment
    }
    create('wallet', event_data)
    return result

    

if __name__ == "__main__":
#    main(sys.argv[1:])
    # myEventData = create('wallet', {"user": "james", "status": "winnings", "amount": 20})
    # print(myEventData)
    # myState = {
    #     'player_hand_val': 19, 
    #     'dealer_hand_val': 17, 
    #     'player_hand': '9-c,2-s,8-d', 
    #     'dealer_hand': '9-s,8-d', 
    #     'player_last_action': 'stand', 
    #     'dealer_last_action': 'stand', 
    #     'result': 'win', 
    #     'bet_return': 1,
    #     'status': ''
    # }
    # result = save_state('blackjack', 'james', myState)
    # print(result)
    result_two = get_state('blackjack','reaif')
    print(result_two)
    # print(result_two['event_date'])
    # result_three = wallet_transaction('james', 100 * -1, 'blackjack wager')
    # print('wallet:', str(result_three))
    # result_four = reset_state('blackjack','james')
    # print(result_four)