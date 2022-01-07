import asyncio 
import pyrogram
from pyrogram import Client, filters 



@Client.on_message(filters.command("start"))
async def gstart(bot, cmd):
  
