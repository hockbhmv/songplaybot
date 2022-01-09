import os
import re
import time
import asyncio 
import logging 
import requests
import youtube_dl
from os import environ 
from .database import db 
from pytube import YouTube 
from pyrogram import Client, filters
from youtube_search import YoutubeSearch 
from youtubesearchpython import VideosSearch 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
database =db

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
    if msg.text.startswith("/song"):
      args = get_arg(msg) + " " + "song"
      if args.startswith(" "):
         return await msg.reply_text("Enter a song name.\n\n **Example:**\n<code>/song panipalli 2</code>")
    else:
      configs = await database.get_chat(int(chat_id))
      if msg.text.startswith("/"):
         return
      if configs['song']:
         return
      k = msg.text
      args = get_arg(msg) + k + "song"
      if not args:
         return await msg.reply("ℹ️ error occurred")
      
    
    status = await message.reply("<code>processing...</code>")
    await asyncio.sleep(1)
    await status.edit("<code>🔄 uploading..</code>")
    video_link = yt_search(args)
    if not video_link:
        await status.edit(f"I couldn't find song with {args}")
        return ""
    yt = YouTube(video_link)
    results = []
    count = 0
    while len(results) == 0 and count < 6:
        if count>0:
            time.sleep(1)
        results = YoutubeSearch(args, max_results=1).to_dict()
        count += 1
   # caps = none
    title = results[0]["title"]
    duration = results[0]["duration"]
    views = results[0]["views"]
    thumbnail = results[0]["thumbnails"][0]
    audio = yt.streams.filter(only_audio=True).first()
    thumb_name = f'thumb{message.message_id}.jpg' 
    thumb = requests.get(thumbnail, allow_redirects=True)
    open(thumb_name, 'wb').write(thumb.content)
    cap =f"** ❍ Title :** <code>{title[:35]}</code>\n**❍ duration :** <code>{duration}</code>\n**❍ views :** <code>{views}</code>\n\n❍ by @MD_songbot"
    try:
        
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song 😶")
        
        return ""
    
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await client.send_chat_action(message.chat.id, "upload_audio")
    k = await client.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        caption = cap,
        thumb=thumb_name,
        performer=f"[MD MUSIC BOT]",
        reply_to_message_id= message.message_id)
    db = message.chat.id  #-1001553356176
    m = await k.copy(int(db))
    can = [[InlineKeyboardButton('🔰 send in pm 🔰', callback_data=f"pm#{k.message_id}#{db}")]]
    reply = InlineKeyboardMarkup(can)
    await k.edit_reply_markup(InlineKeyboardMarkup(can))
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
    
