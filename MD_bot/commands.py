import asyncio 
import logging 
import pyrogram 
from .database import db 
from info import PICS 
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

log = -1001553356176
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

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
        photo=f"https://telegra.ph/file/156e945a81a2160012c2c.jpg", 
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
        await k.delete()
        await message.delete()
   return

@Client.on_callback_query()
async def startquery(bot, message):
   if message.data =="pmm":
       i, msg, db = message.data.split('#')
       msg = await bot.get_messages(db, int(msg))
       await message.answer("The song is sended to your pm", show_alert=True)
       await msg.copy(int(message.from_user.id))
      
   if message.data =="start":
       buttons = [[InlineKeyboardButton('➕ Add to your group ➕', url='http://t.me/MD_songbot?startgroup=true')],[InlineKeyboardButton('ℹ️ Help', callback_data="help"),InlineKeyboardButton('📢 Support channel', url=f"https://t.me/venombotupdates")]]
       await message.message.edit_text(
          text= f"Hi {message.from_user.first_name},\ni am a song bot i can give song in your group",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
      
   if message.data =="help":
       buttons = [[InlineKeyboardButton('Music', callback_data='song'),InlineKeyboardButton('lyrics', callback_data='lyric')],[InlineKeyboardButton('⬅️ Back', callback_data='start')]]
       await message.message.edit_text(
          text="please add me in your group and send a song name i will give that song in group",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
      
   if message.data =="song":
       buttons = [[InlineKeyboardButton('⬅️ Back', callback_data='help')]]
       await message.message.edit_text(
         text="<b>MODULE FOR SONG 🎧:</b>\n\n\n📚available commands:\n\n- /song <code>{youtubeurl or Search Query}</code> <code>- download the particular query in audio format</code>\n- /video <code>{youtubeurl or search Query}</code> <code>- download the particular query in video format</code>\n\n<b>example:</b>\n<code>/song Ckay Love Nwantiti\n/song nadan vibe - ribin</code>\n\n<b>📖 other commands:</b>\n<code>/songwithcmd True</code>  <code>- This command for bot will give reply only with above command</code>\n<code>/songwithcmd False</code>  <code>- This command for bot will give song not video without any above command</code>\n\n<b>example:-</b>\n<code>panipalli 2</code>\n<code>Ckay Love Nwantiti</code>",
         reply_markup = InlineKeyboardMarkup(buttons),
         parse_mode='html')
         
   if message.data =="lyric":
       buttons = [[InlineKeyboardButton('⬅️ Back', callback_data='help')]]
       await message.message.edit_text(
          text="<b>MODULE LYRICS</b>\n\n📚 available command:\n<code>/Lyrics {Music name}</code>-<code>search lyrics of your query</code>\n\n<b>example:</b>\n<code>/lyrics Alone - Marshmallow</code>\n<code>/lyrics Nj panipali</code>\n",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
  
   
