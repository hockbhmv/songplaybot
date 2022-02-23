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
  
"""groups"""

async def all_groups():
    return groups.find({})
  
async def total_groups():
    count = await groups.count_documents({})
    return count 
