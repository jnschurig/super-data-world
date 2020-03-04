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
botStatus="Active"

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
    print("botName= " + botName)
    print("botDesc= '" + botDesc + "'")
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

# write query
registerQuery=""
registerQuery+="with \n"
registerQuery+="    parms as (select 'active' bot_status_name, 'botName' bot_name, 'botDesc' bot_description)\n"
registerQuery+=" select current_timestamp  created_date \n"
registerQuery+="       ,current_timestamp  modified_date\n"
registerQuery+="       ,a.entity_status_id bot_status_id\n"
registerQuery+="       ,x.bot_name\n"
registerQuery+="       ,x.bot_description\n"
registerQuery+="   from game.entity_status a \n"
registerQuery+="   cross join parms x\n"
registerQuery+="  where a.status_name = x.bot_status_name\n"


print(registerQuery)
# # execute query
# def doQuery( conn ):
#    cur = conn.cursor()

#    cur.execute( "select 'Hi Molly' as current_timest")

#    for current_timestamp in cur.fetchall() :
#        print (current_timestamp)

# print ("using psycopg2...")
# #import psycopg2
# myConnection = psycopg2.connect (host=hostname, user=username, password=password, dbname=database)
# doQuery(myConnection)
# myConnection.close()
