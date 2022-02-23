import asyncio 
import time, datetime
from pyrogram import Client, filters
from .db import total_users, total_groups, all_users, all_groups
from info import MONGODB_URL, DB

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# https://t.me/GetTGLink/4178
async def verupikkals(bot, message):
    i, use = message.text.split(None, 1)
    if use=="users":
        total = await total_users()
        users = await all_users()
        total_users = total
    else:
        total = await total_groups()
        users = await all_groups()
        total_users = total
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")
