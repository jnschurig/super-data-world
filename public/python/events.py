import os, re, json
from pathlib import Path

dataDirName = 'data'

osSlash = ''
if os.name == 'nt': # Windows
    osSlash = '\\'
if os.name == 'posix':
    osSlash = '/'

print(os.path.realpath(__file__))

scriptDir = os.path.dirname(os.path.realpath(__file__))
dataDir = scriptDir + '/' + dataDirName

print(dataDir)

def create_append(event_name, event_data):
    print('hello world')
    fileName = event_name
    print(fileName)
    fileName = re.sub('\\s','_',fileName) # Replace whitespace with underscores.
    fileName = re.sub('\\W','',fileName) # Remove non-word characters.
    fileName = re.sub('_*$','',fileName) # Remove trailing underscores.
    fileName = re.sub('^_*','',fileName) # Remove preceeding underscores.
    print(fileName)

    longFile = dataDir + '/' + fileName+'.json'

    Path(dataDir).mkdir(parents=True, exist_ok=True)
    
    if os.path.exists(longFile):
        writeMode = 'a'
    else:
        writeMode = 'w'

    data = {}
    data["event"] = []

    # Need to approach this a little differently...
    # 1. Check if file exists.
    # 2. If not exists, dump to file.
    # 3. If it does exist, read the file into a data object
    #   a. "update" the data object with new data.
    #   b. overwrite the existing file with all data.
    # Use this for reference: https://www.geeksforgeeks.org/append-to-json-file-using-python/

    iterator = event_data.split(',')

    for i in iterator:
        j = i.split('=')
        data["event"].append({j[0]:j[1]})

    print(data)
    with open(longFile, writeMode) as outfile:
        if writeMode == 'a':
            # Add a comma to the end...
            print('Cycle...')
        json.dump(data, outfile)
    

if __name__ == "__main__":
#    main(sys.argv[1:])
    create_append('my Event is a good event. 123 %$^%', 'user=my_user,type=my type')