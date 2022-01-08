import asyncio 
import pyrogram
from pyrogram import Client, filters 
from .database import db 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
photo = "https://telegra.ph/file/7c987afbecbb3e9dcea5a.jpg"
log = -1001553356176
   
@Client.on_message(filters.command("start"))
async def gstart(bot, cmd):
   if cmd.chat.type in ['group', 'supergroup']:
       buttons = [[InlineKeyboardButton('🤖 Bot Updates', url='https://t.me/joinchat/MtD0j4FOqbFmYmE1')],[InlineKeyboardButton('ℹ️ Help', url=f"https://t.me/MD_songbot?start=help")]]
       reply_markup = InlineKeyboardMarkup(buttons)
       await cmd.reply(f"Hey,{cmd.chat.title}\ni am a song bot i can give song in your group", reply_markup=reply_markup)
       await asyncio.sleep(2) 
       if not await db.get_chat(cmd.chat.id):
            total=await bot.get_chat_members_count(cmd.chat.id)
            channel_id = cmd.chat.id
            group_id = cmd.chat.id
            title = cmd.chat.title
            Unknown = "Unknown"
            await db.add_chat(cmd.chat.id, cmd.chat.title)
            await bot.send_message(log, f"#new group:\nTitle - {cmd.chat.title}\nId - {cmd.chat.id}\nTotal members - {total} added by - {Unknown}")
       return
   if not await db.is_user_exist(cmd.from_user.id): 
        await db.add_user(cmd.from_user.id, cmd.from_user.first_name)
        await bot.send_message(log, f"#NEWUSER: \nName - [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id})\nID - {cmd.from_user.id}")
        buttons = [[InlineKeyboardButton('🤖 Bot Updates', url='https://t.me/joinchat/MtD0j4FOqbFmYmE1')],[InlineKeyboardButton('ℹ️ Help', url=f"https://t.me/MD_songbot?start=help")]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await cmd.reply_photo(
            photo=photo, 
            caption=f"Hi {cmd.from_user.first_name},\ni am a song bot i can give song in your group",
            parse_mode="html",
            reply_markup=reply_markup )
   return

@Client.on_message(filters.command("songwithcmd"))
async def withcmd(bot, message):
   if ' ' in message.text:
        k = await message.reply('updating your data')
        r, sts = message.text.split(None, 1)
        chat = cmd.chat.id
        await asyncio.sleep(1)
        if sts ==["True","true"]:
            await db.song(int(chat))
            await k.edit("successful")
        if sts ==["False","false"]:
            await db.notsong(int(chat))
            await k.edit("successful")
        
   
   
