from os import environ


API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
CHANNEL = int(environ.get('CHANNEL', '-1001662995429'))
PICS = (environ.get("PICS", "")).split()
MONGODB_URL = environ['MONGODB_URL']
DB = environ['DB']
