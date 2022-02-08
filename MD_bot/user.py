from pyrogram import Client
from info import API_HASH, API_ID, SESSION
    

class User(Client):
    def __init__(self):
        super().__init__(
            SESSION,
            api_hash=API_HASH,
            api_id=API_ID,
            workers=4
        )
        
    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        return (self, usr_bot_me.id)

    async def stop(self, *args):
        await super().stop()
