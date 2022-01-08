import asyncio 
import pyrogram
from pyrogram import Client, filters 
from .database import db 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import photo 
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
        buttons = [[InlineKeyboardButton('➕ Add to your group ➕', url='http://t.me/MD_songbot?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data=f"help"),InlineKeyboardButton('📢 Support channel', url=f"https://t.me/venombotupdates")]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await cmd.reply_photo(
            photo=photo, 
            caption=f"Hi {cmd.from_user.first_name},\ni am a song bot i can give song in your group",
            parse_mode="html",
            reply_markup=reply_markup )
   return

@Client.on_message(filters.command("songwithcmd") & filters.group)
async def withcmd(bot, message):
   chat = message.chat.id
   user = message.from_user.id
   st = await bot.get_chat_member(chat, user)
   if not (st.status == "creator") or (st.status == "administrator"):
      return
   if ' ' in message.text:
        r, sts = message.text.split(None, 1)
        if sts =="True":
            await db.song(int(chat))
            k =await message.reply("successfull, Now bot send song only with using command /song")
        if sts =="False":
            await db.notsong(int(chat))
            k =await message.reply("successfull, Now bot send song without any commands")
        await asyncio.sleep(3)
        await k and message.delete()
   return

@Client.on_callback_query()
async def delete_all_index_confirm(bot, message):
   if message.data =="start":
       buttons = [[InlineKeyboardButton('➕ Add to your group ➕', url='http://t.me/MD_songbot?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data="help"),InlineKeyboardButton('📢 Support channel', url=f"https://t.me/venombotupdates")]]
       await message.message.edit_text(
          text= f"Hi {message.from_user.first_name},\ni am a song bot i can give song in your group",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
      
   elif message.data =="help":
       buttons = [[InlineKeyboardButton('⬅️ Back', callback_data='start')]]
       await message.message.edit_text(
          text="please add me in your group and send a song name i will give that song in group",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
          
