import os
from info import BOT_TOKEN, API_ID, API_HASH
import pyromod.listen


import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)



bot = Client(
    'SongPlayRoBot',
    bot_token = BOT_TOKEN,
    api_id = API_ID,
    api_hash = API_HASH,
    workers=100
  )


            
        
    
bot.run()
    
    
