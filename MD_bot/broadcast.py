import asyncio 
import time, datetime
from pyrogram import Client, filters 
from .database import db
from db import total_users, total_groups, new_user, new_group
from info import MONGODB_URL, DB

@Client.on_message(filters.command("broadcast"))
async def verupikkals(bot, message):
    i, use = message.text.split(None, 1)
    if use=="users":
        total = await db.total_users_count()
        users = await db.get_all_users()
        ntotal = await total_users()
        total_users = total 
        name = "name"
        new_chat = new_user
    else:
        total = await db.total_chat_count()
        users = await db.get_all_chats()
        ntotal = await total_groups()
        total_users = total 
        name = "title"
        new_chat=new_group
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    
    done = 0
    old = 0
    new = 0
    async for user in users:
        i, use= await new_chat(int(user["id"]), user[name])
        if use=="in":
           old+=1
        else:
           new+=1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {new}\nalready: {old}\n\nnew added: {ntotal}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {new}\n\n: {old}\nnew added: {ntotal}")

    
