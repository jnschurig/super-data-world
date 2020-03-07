import argparse, json, os, psycopg2, sys

# A comment?
helpText = "This program is designed to register (or deregister) a bot to help with the game."

parser = argparse.ArgumentParser(description = helpText)

parser.add_argument("--botname","-b", help="a valid bot name (required)")
parser.add_argument("--desc","-d", help="description of the bot (optional)")
parser.add_argument("--disable","-x", help="'True' to deactivate")
parser.add_argument("--verbose","-v",help="'True' to turn on verbose logging")

args = parser.parse_args()

# Setting some defaults
isVerbose=False
botName="Null"
botDesc=args.desc
enableBot=True
botStatus="active"
botStatusID=0

if args.verbose:
    isVerbose=args.verbose
    print("Verbose logging enabled")

# decide whether to stop now or continue.
if not args.botname:
    if isVerbose: print("No bot name provided. Exiting...")
    sys.exit()

botName=args.botname

if not args.desc:
    botDesc=args.botname

if args.disable:
    enableBot=False
    botStatus="disabled"

if isVerbose: 
    print("botName = " + botName)
    print("botDesc = '" + botDesc + "'")
    print("enableBot = " + str(enableBot))


script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "database_credentials.json")
with open(file_path, "r") as f:
    dbcred = json.load(f)

# #print (dbcred["hostname"])

hostname = dbcred["hostname"]
username = dbcred["username"]
password = dbcred["password"]
database = dbcred["database"]
port     = dbcred["port"]

statusQuery="select a.entity_status_id bot_status_id from game.entity_status a where a.status_name = '"+botStatus+"'"
if isVerbose: print ("statusQuery = \n" + statusQuery)

# execute query
conn = psycopg2.connect(user=username, password=password, host=hostname, port=port, database=database)
cur = conn.cursor()
cur.execute( statusQuery )
bot_status_id = cur.fetchone()
botStatusID = int(bot_status_id[-1])
if isVerbose: print ("botStatusID = " + str(botStatusID))

if(conn):
    cur.close()
    conn.close()
    if isVerbose: print("Connection to DB is closed...")


# write query
registerQuery = ""
registerQuery += "insert into game.bot_registration \n"
registerQuery += "  (created_date \n"
registerQuery += "  ,modified_date \n"
registerQuery += "  ,bot_status_id \n"
registerQuery += "  ,bot_name\n"
registerQuery += "  ,bot_description\n"
registerQuery += "  )\n"
registerQuery += "values\n"
registerQuery += "  (current_timestamp\n"
registerQuery += "  ,current_timestamp\n"
registerQuery += "  ," + str(botStatusID) + "\n"
registerQuery += "  ,'" + botName + "'\n"
registerQuery += "  ,'" + botDesc + "'\n"
registerQuery += "  )\n"
registerQuery += "on conflict on constraint AK_bot_registraton\n"
registerQuery += "do update set \n"
registerQuery += "   modified_date   = current_timestamp\n"
registerQuery += "  ,bot_status_id   = " + str(botStatusID) + "\n"
registerQuery += "  ,bot_name        = '" + botName + "'\n"
registerQuery += "  ,bot_description = '" + botDesc + "'\n"
registerQuery += "returning bot_status_id\n"
# registerQuery += "; commit\n"

if isVerbose: print ("registerQuery = \n" + registerQuery)

conn2 = psycopg2.connect(user=username, password=password, host=hostname, port=port, database=database)
regCur = conn2.cursor()
regCur.execute( registerQuery )
registerResult = regCur.fetchone()
botRegistrationID=int(registerResult[-1])
if isVerbose: print("botRegistrationID = " + str(botRegistrationID))
print(botRegistrationID)


