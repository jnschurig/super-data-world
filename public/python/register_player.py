import argparse, json, os, psycopg2

print("hello world" )

# A comment?
helpText = "This program is designed to register a new player in the game."

parser = argparse.ArgumentParser(description = helpText)


# define arguments
# Needs the following:
# 1. the player name
# 2. bot ID 
# 3. channel ID

parser.add_argument("--player","-p", help="user name to register")
parser.add_argument("--bot","-b", help="a valid bot id (int)")
parser.add_argument("--channel","-c", help="the channel id to associate the user with (int)")

args = parser.parse_args()

if args.player:
    print("Player Name '" + args.player + "'")
if args.bot:
    print("bot ID " + args.bot)
if args.channel:
    print("Channel ID " + args.channel)

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "database_credentials.json")
with open(file_path, "r") as f:
    dbcred = json.load(f)

#print (dbcred["hostname"])

hostname = dbcred["hostname"]
username = dbcred["username"]
password = dbcred["password"]
database = dbcred["database"]

# write query


# execute query
def doQuery( conn ):
   cur = conn.cursor()

   cur.execute( "select 'Hi Molly' as current_timest")

   for current_timestamp in cur.fetchall() :
       print (current_timestamp)

print ("using psycopg2...")
#import psycopg2
myConnection = psycopg2.connect (host=hostname, user=username, password=password, dbname=database)
doQuery(myConnection)
myConnection.close()
