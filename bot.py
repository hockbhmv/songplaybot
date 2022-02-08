import os
from info import BOT_TOKEN, API_ID, API_HASH, SESSION
import pyromod.listen
from pyrogram import Client
from user import USER, USER_ID
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
        SESSION,
        bot_token = BOT_TOKEN,
        api_id = API_ID,
        api_hash = API_HASH,
        plugins={"root": "MD_bot"},
        workers=100
        )
    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.set_parse_mode("html")
        print(f'bot {usr_bot_me} started')
        self.USER, self.USER_ID = await User().start()
            
    async def stop(self, *args):
        await super().stop()
        
    
