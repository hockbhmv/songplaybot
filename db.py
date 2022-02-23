from motor.motor_asyncio import AsyncIOMotorClient as Bot
from info import MONGODB_URL as url 

db=url.program
dbusers = db.dbusers
groups = db.chatsettings

"""users"""
async def all_users():
    return dbusers.find({})
  
async def total_users():
    count = await dbusers.count_documents({})
    return count 

async def new_user(id :int, name):
    user = await dbusers.find_one({"id": id})
    if not user:
       data = {"id": id, "name": name} 
       await dbusers.insert_one(data)
       return True, "new"
    return True, "in"
  
"""groups"""

async def all_groups():
    return groups.find({})
  
async def total_groups():
    count = await groups.count_documents({})
    return count 

async def new_group(id :int, name):
    user = await groups.find_one({"id": id})
    if not user:
       data = {"id": id, "title": name} 
       await groups.insert_one(data)
       return True, "new"
    return True, "in"
