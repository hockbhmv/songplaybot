import os
from info import BOT_TOKEN, API_ID, API_HASH, SESSION
import pyromod.listen
from pyrogram import Client

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)



bot = Client(
    SESSION,
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH,
    plugins={"root": "MD_bot"},
    workers=100
  )


            
        
    
bot.run()
    
    
