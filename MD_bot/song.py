import os
import re
import time
import asyncio 
import logging 
import requests
import youtube_dl
from os import environ 
from pytube import YouTube 
from pyrogram import Client, filters
from youtube_search import YoutubeSearch 
from youtubesearchpython import VideosSearch
from . import get_search_results, db as database, media
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 

logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
 

def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url
def get_arg(message):
    msg = message.text
    msg = msg.replace(" "," ",1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])        


@Client.on_message(filters.text & filters.group & filters.incoming)
async def song(client, message):
    msg = message
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    settings = await database.get_settings(chat_id)
    if not settings['song']:
       return
    if msg.text.startswith("/song"):
      args = get_arg(msg) + " " + "song"
      if args.startswith(" "):
         return await msg.reply_text("Enter a song name.\n\n **Example:**\n<code>/song panipalli 2</code>")
    else:
      if msg.text.startswith("/"): return
      elif settings['command']: return
      k = msg.text
      args = get_arg(msg) + k + "song"
      if not args:
         return await msg.reply("ℹ️ error occurred")
    status = await message.reply("<code>processing...</code>")
    video_link = yt_search(args)
    await status.edit("<code>🔄 uploading ▢▢▢</code>")
    if not video_link:
        await status.edit(f"I couldn't find song with {args}")
        return ""
    await status.edit("<code>🔄 uploading ▣▢▢</code>")
    yt = YouTube(video_link)
    await status.edit("<code>🔄 uploading ▣▣▢</code>")
    files, offset, total_results = await get_search_results(str(yt.title), offset=1, filter=True)
    if files:
       for file in files:
         song_name = re.sub(r"(_|\-|\.|\+|\(|\))", "", yt.title)
         if file.file_name in f"{song_name} mp3":
             xx = await client.send_cached_media(chat_id=message.chat.id,file_id=file.file_id, caption=file.caption, reply_to_message_id= message.message_id)
             can = [[InlineKeyboardButton('🔰 SEND IN MY PM 🔰', callback_data=f"pm#{xx.message_id}#{message.chat.id}")]]
             await xx.edit_reply_markup(InlineKeyboardMarkup(can))
             return await status.delete()
         else: 
             return await status.edit(f"{file.file_name}\n\n\n{song_name} mp3")
    results = []
    count = 0
    while len(results) == 0 and count < 6:
        if count>0:
            time.sleep(1)
        results = YoutubeSearch(args, max_results=1).to_dict()
        count += 1
   
    title = results[0]["title"]
    duration = results[0]["duration"]
    views = results[0]["views"]
    thumbnail = results[0]["thumbnails"][0]
    thumb_name = f'thumb{message.message_id}.jpg' 
    thumb = requests.get(thumbnail, allow_redirects=True)
    open(thumb_name, 'wb').write(thumb.content)
    cap =f"** ❍ Title :** <code>{title[:35]}</code>\n**❍ duration :** <code>{duration}</code>\n**❍ views :** <code>{views}</code>\n**❍ Link :** [Click here]({video_link})\n**❍ Uploaded by** [MD MUSIC BOT](https://t.me/MD_songbot)"
    try:
        audio = yt.streams.filter(only_audio=True).first()
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song 😶")
        return ""
    rename = os.rename(download, f"{str(yt.title)}.mp3")
    await client.send_chat_action(message.chat.id, "upload_audio")
    try:
       await status.edit("<code>🔄 uploading ▣▣▣</code>")
       song = await client.send_audio(
           chat_id=message.chat.id,
           audio=f"{str(yt.title)}.mp3",
           duration=int(yt.length),
           title=str(yt.title),
           caption = cap,
           thumb=thumb_name,
           performer="[MD MUSIC BOT]",
           parse_mode="combined",
           reply_to_message_id= message.message_id)
       db = message.chat.id  
       can = [[InlineKeyboardButton('🔰 SEND IN MY PM 🔰', callback_data=f"pm#{song.message_id}#{db}")]]
       await song.edit_reply_markup(InlineKeyboardMarkup(can))
       await status.delete()
       await media(client, song)
       os.remove(f"{str(yt.title)}.mp3")
    except:
       await status.edit("some error occurred, please try again")
    
@Client.on_callback_query(filters.regex(r"^pm"))
async def pmquery(bot, message):
       i, msg, db = message.data.split('#')
       msg = await bot.get_messages(db, int(msg))
       await message.answer("The song is sended to your pm", show_alert=True)
       await msg.copy(int(message.from_user.id), reply_markup=None)
    
