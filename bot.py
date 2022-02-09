import os
from user import User
import pyromod.listen
from MD_bot import Media
from pyrogram import Client
from info import BOT_TOKEN, API_ID, API_HASH

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)



class Bot(Client):
    USER: User = None
    USER_ID: int = None
    
    def __init__(self):
        super().__init__(
        "song bot",
        bot_token = BOT_TOKEN,
        api_id = API_ID,
        api_hash = API_HASH,
        plugins={"root": "MD_bot"},
        workers=50
        )
    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        usr_bot_me = await self.get_me()
        self.set_parse_mode("html")
        self.USER, self.USER_ID = await User().start()
        print(f'bot {usr_bot_me.username} started')  
        
    async def stop(self, *args):
        await super().stop()
            
        
    
Bot().run()
    
    
