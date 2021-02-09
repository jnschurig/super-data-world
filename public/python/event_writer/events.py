import os, re, json, hashlib
import sys
from datetime import datetime
from pathlib import Path

dataDirName = 'data'

osSlash = ''
if os.name == 'nt': # Windows
    osSlash = '\\'
if os.name == 'posix':
    osSlash = '/'

# print(os.path.realpath(__file__))

scriptDir = os.path.dirname(os.path.realpath(__file__))

def create_append(event_name, event_data):
    # Date related variables
    now = datetime.now()
    dirDate = now.strftime('%Y%m%d')
    hashSalt = now.strftime('%Y%m%d_%H%M%S_%f')
    eventDate = now.strftime('%Y-%m-%d %H:%M:%S.%f %z').strip()
    
    # Create event ID
    preHash = event_name + ' ' + hashSalt
    eventid = hashlib.md5(preHash.encode()).hexdigest()
    
    # Get the data and figure out what to do with it.
    dataPart = {}
    dataPart['id'] = eventid
    dataPart['event'] = event_name
    dataPart['eventdate'] = eventDate
    iterator = event_data.split(',')
    
    for i in iterator:
        j = i.split('=')
        # print('Pair: ' + j[0] + ': ' + j[1])
        dataPart[j[0]] = j[1]
    
    # print('dataPart: ' + str(dataPart))


    # Get file name and make path.
    fileName = event_name
    fileName = re.sub('\\s','_',fileName) # Replace whitespace with underscores.
    fileName = re.sub('\\W','',fileName) # Remove non-word characters.
    fileName = re.sub('_*$','',fileName) # Remove trailing underscores.
    fileName = re.sub('^_*','',fileName) # Remove preceeding underscores.
    
    dataDir = scriptDir + osSlash + dataDirName + osSlash + dirDate
    longFile = dataDir + osSlash + fileName+'.json'
    Path(dataDir).mkdir(parents=True, exist_ok=True)
    
    # Use this for reference: https://www.geeksforgeeks.org/append-to-json-file-using-python/
    # There might be a better way using this ^

    #------------ Better IDEA -------------------
    # Just write parts to their own files. Don't bother appending. It's ok!... maybe?
    # -------------------------------------------
    # We have the data, now worry about writing it out.
    if os.path.exists(longFile):
        with open(longFile) as infile:
            data = json.load(infile)
        # Janky solution converting json to a string and appending the data. 
        # Could definitely do with a better way.
        strjson = str(data)
        strjson = re.sub('^{','[{',strjson)
        strjson = re.sub(']$','',strjson)
        strjson += ',\n' + str(dataPart) + ']'
        strjson = re.sub("'",'"',strjson)
        data = json.loads(strjson)
        
        with open(longFile, 'w') as outfile:
            json.dump(data, outfile)

    else: # New file, just output data.
        with open(longFile, 'w') as outfile:
            json.dump(dataPart, outfile)

    return dataPart
    
    

if __name__ == "__main__":
#    main(sys.argv[1:])
    myEventData = create_append('my Event is a good event. 123 %$^%', 'user=my_user,type=my type')
    print(myEventData)