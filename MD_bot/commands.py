import asyncio 
import logging 
import pyrogram 
from info import PICS 
from .database import db
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
   
   buttons = [[InlineKeyboardButton('➕ ᗩᗪᗪ ᗰᗴ TO YOᑌᖇ ᘜᖇOᑌᑭ ➕', url='http://t.me/MD_songbot?startgroup=true')],[InlineKeyboardButton('ᕼᗴᒪᑭ', callback_data=f"start#help"),InlineKeyboardButton('ՏᑌᑭᑭOᖇT ᑕᕼᗩᑎᑎᗴᒪ', url=f"https://t.me/venombotupdates")]]
   reply_markup = InlineKeyboardMarkup(buttons)
   await cmd.reply_photo(
        photo=f"https://telegra.ph/file/156e945a81a2160012c2c.jpg", 
        caption=f"ʜɪ {cmd.from_user.first_name},\nɪ ᴀᴍ ᴀ sᴏɴɢ ʙᴏᴛ ɪ ᴄᴀɴ ɢɪᴠᴇ sᴏɴɢ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
        parse_mode="html",
        reply_markup=reply_markup )
   return

@Client.on_message(filters.command(["settings", "songwithcmd"]) & filters.group)
async def withcmd(bot, message):
   chat = message.chat.id
   user = message.from_user.id
   st = await bot.get_chat_member(chat, user)
   if not (st.status == "creator") or (st.status == "administrator"):
      k=await message.reply_text("your not group owner or admin")
      await asyncio.sleep(7)
      return await k.delete(True)
   settings = await db.get_settings(chat)
   if settings is not None:
      button=[[
         InlineKeyboardButton(f'Song', callback_data =f"done#song#{settings['song']}"), InlineKeyboardButton('OFF ❌' if settings['song'] else 'ON ✅', callback_data=f"done_#song#{settings['song']}")
         ],[ 
         InlineKeyboardButton(f'Video', callback_data =f"done#video#{settings['video']}"), InlineKeyboardButton('OFF ❌' if settings['video'] else 'ON ✅', callback_data=f"done_#video#{settings['video']}")
         ],[
         InlineKeyboardButton(f'Song Without Command', callback_data =f"done#command#{settings['command']}"), InlineKeyboardButton('OFF ❌' if not settings['command'] else 'ON ✅', callback_data=f"done_#command#{settings['command']}")
      ]]
      await message.reply_text("<b>change your group setting using below buttons</b>", reply_markup=InlineKeyboardMarkup(button))
      
@Client.on_message(filters.command(["refresh", "update"]) & filters.group)
async def refresh_db(bot, message):
   st = await bot.get_chat_member(message.chat.id, message.from_user.id)
   if not (st.status == "creator") or (st.status == "administrator"):
      k=await message.reply_text("your not group owner or admin")
      await asyncio.sleep(7)
      return await k.delete(True)
   default= dict(
      song=True,
      video=True,
      command=True)
   return await db.update_settings(message.chat.id, default)

@Client.on_message(filters.command(["stats", "status"]))
async def db_stats(bot, message): 
   users = await db.total_users_count()
   chats = await db.total_chat_count()
   await message.reply_text(f"★ Total users: <code>{users}</code>\n★ Total Chats: <code>{chats}</code>")

@Client.on_callback_query(filters.regex(r"^done"))
async def settings_query(bot, msg):
   int, type, value = msg.data.split('#')
   group = msg.message.chat.id
   st = await bot.get_chat_member(group, msg.from_user.id)
   if not (st.status == "creator") or (st.status == "administrator"):
      return await msg.answer("your not group owner or admin")
      
   if value=="True":
      done = await settings(group, type, False)
   else:
      done = await settings(group, type, True)
   settings = await db.get_settings(group)
   if done:
      if settings is not None:
         button=[[
            InlineKeyboardButton(f'Song', callback_data =f"done#song#{settings['song']}"), InlineKeyboardButton('OFF ❌' if settings['song'] else 'ON ✅', callback_data=f"done_#song#{settings['song']}")
            ],[
            InlineKeyboardButton(f'Video', callback_data =f"done#video#{settings['video']}"), InlineKeyboardButton('OFF ❌' if settings['video'] else 'ON ✅', callback_data=f"done_#video#{settings['video']}")
            ],[
            InlineKeyboardButton(f'Song Without Command', callback_data =f"done#command#{settings['command']}"), InlineKeyboardButton('OFF ❌' if not settings['command'] else 'ON ✅', callback_data=f"done_#command#{settings['command']}")
         ]]
         return await msg.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(button))
   
@Client.on_callback_query(filters.regex(r"^start"))
async def startquery(bot, message):
   i, k = message.data.split('#')
   if k =="start":
       buttons = [[InlineKeyboardButton('➕ ᗩᗪᗪ ᗰᗴ TO YOᑌᖇ ᘜᖇOᑌᑭ ➕', url='http://t.me/MD_songbot?startgroup=true')],[InlineKeyboardButton('ᕼᗴᒪᑭ', callback_data="start#help"),InlineKeyboardButton('ՏᑌᑭᑭOᖇT ᑕᕼᗩᑎᑎᗴᒪ', url=f"https://t.me/venombotupdates")]]
       await message.message.edit_text(
          text= f"ʜɪ {message.from_user.first_name},\nɪ ᴀᴍ ᴀ sᴏɴɢ ʙᴏᴛ ɪ ᴄᴀɴ ɢɪᴠᴇ sᴏɴɢ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
      
   elif k =="help":
       buttons = [[InlineKeyboardButton('ᗰᑌՏIᑕ', callback_data='start#song'),InlineKeyboardButton('ᒪYᖇIᑕՏ', callback_data='start#lyric')],[InlineKeyboardButton('⬅️ ᗷᗩᑕK', callback_data='start#start')]]
       await message.message.edit_text(
          text="ᴘʟᴇᴀsᴇ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ sᴇɴᴅ ᴀ sᴏɴɢ ɴᴀᴍᴇ ɪ ᴡɪʟʟ ɢɪᴠᴇ ᴛʜᴀᴛ sᴏɴɢ ɪɴ ɢʀᴏᴜᴘ",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
      
   elif k =="song":
       buttons = [[InlineKeyboardButton('⬅️ ᗷᗩᑕK', callback_data='start#help')]]
       await message.message.edit_text(
         text="<b>MODULE FOR SONG 🎧:</b>\n\n\n📚available commands:\n\n- /song <code>{youtubeurl or Search Query}</code> <code>- download the particular query in audio format</code>\n- /video <code>{youtubeurl or search Query}</code> <code>- download the particular query in video format</code>\n\n<b>example:</b>\n<code>/song Ckay Love Nwantiti\n/song nadan vibe - ribin</code>\n\n<b>📖 other commands:</b>\n<code>/songwithcmd True</code>  <code>- This command for bot will give reply only with above command</code>\n<code>/songwithcmd False</code>  <code>- This command for bot will give song not video without any above command</code>\n\n<b>example:-</b>\n<code>panipalli 2</code>\n<code>Ckay Love Nwantiti</code>",
         reply_markup = InlineKeyboardMarkup(buttons),
         parse_mode='html')
         
   elif k =="lyric":
       buttons = [[InlineKeyboardButton('⬅️ ᗷᗩᑕK', callback_data='start#help')]]
       await message.message.edit_text(
          text="<b>MODULE LYRICS</b>\n\n📚 available command:\n<code>/Lyrics {Music name}</code>-<code>search lyrics of your query</code>\n\n<b>example:</b>\n<code>/lyrics Alone - Marshmallow</code>\n<code>/lyrics Nj panipali</code>\n",
          reply_markup = InlineKeyboardMarkup(buttons),
          parse_mode='html')
      
async def settings(group_id, key, value):
    current = await db.get_settings(group_id)
    current[key] = value
    await db.update_settings(group_id, current)  
    return True

