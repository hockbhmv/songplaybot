from os import environ


API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
SESSION = environ['SESSION']
PICS = (environ.get("PICS", "")).split()
DB = environ['DB']
