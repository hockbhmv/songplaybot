import motor.motor_asyncio
from info import DB 

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
        self.cache = {}
        
    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                song=True,
            ),
        )
 
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count 
      
    async def get_all_users(self):
        return self.col.find({})
    

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
        
    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    

    async def get_all_chats(self):
        return self.grp.find({})


    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    
    async def song(self, id):
        chat_status=dict(
            song =True,
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
     
    async def notsong(self, id):
        chat_status=dict(
            song=False,
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
        
    async def get_chat(self, chat):
        chat = await self.grp.find_one({'id':int(chat)})
        if not chat:
            return False
        else:
            return chat.get('chat_status')
        
    async def update_settings(self, id, settings):
        await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
        
    
    async def get_settings(self, id):
        default = {
            'song': True,
            'command': False
        }
        chat = await self.grp.find_one({'id':int(id)})
        if chat:
            return chat.get('settings', default)
        return default
    
    async def find_chat(self, chat: int):
        connections = self.cache.get(str(chat))
        if connections is not None:
            return connections
        connections = await self.grp.find_one({'id': chat})
        if connections:
            self.cache[str(chat)] = connections
            return connections
        else: 
            return self.new_group(None, None)
          
db= Database(DB, "song-bot")
