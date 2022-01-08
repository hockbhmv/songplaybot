from os import environ


API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
photo = (environ.get("PHOTOS", "")).split()
DB = environ['DB']
