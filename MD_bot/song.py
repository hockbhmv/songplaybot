import os
import re
import time
import asyncio 
import logging 
import requests
import youtube_dl
from os import environ 
from pytube import YouTube 
from .database import db as database
from pyrogram import Client, filters
from youtube_search import YoutubeSearch 
from youtubesearchpython import VideosSearch
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
    status = await message.reply("ᴘʀᴏᴄᴇssɪɴɢ...")
    video_link = yt_search(args)
    await status.edit("🔄 ᴜᴘʟᴏᴀᴅɪɴɢ ▢▢▢")
    if not video_link:
        await status.edit(f"I couldn't find song with {args}")
        return ""
    yt = YouTube(video_link)
    await status.edit("🔄 ᴜᴘʟᴏᴀᴅɪɴɢ ▣▢▢")
    results = []
    count = 0
    while len(results) == 0 and count < 6:
        if count>0:
            time.sleep(1)
        results = YoutubeSearch(args, max_results=1).to_dict()
        count += 1
    await status.edit("🔄 ᴜᴘʟᴏᴀᴅɪɴɢ ▣▣▢")
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
        await status.edit("some error occurred, please try again")
        return ""
    rename = os.rename(download, f"{str(yt.title)}.mp3")
    await client.send_chat_action(message.chat.id, "upload_audio")
    try:
       xx = await client.send_audio(
           chat_id=message.chat.id,
           audio=f"{str(yt.title)}.mp3",
           duration=int(yt.length),
           title=str(yt.title),
           caption = cap,
           thumb=thumb_name,
           performer="[MD MUSIC BOT]",
           parse_mode="combined",
           reply_to_message_id= message.message_id)
       await status.edit("🔄 ᴜᴘʟᴏᴀᴅɪɴɢ ▣▣▣")
       db = message.chat.id  
       can = [[InlineKeyboardButton('♻️ sᴇɴᴅ ɪɴ ᴍʏ ᴘᴍ ♻️', callback_data=f"pm#{xx.message_id}#{db}")]]
       await xx.edit_reply_markup(InlineKeyboardMarkup(can))
       await status.delete()
       os.remove(f"{str(yt.title)}.mp3")
    except:
       await status.edit("some error occurred, please try again")
    
@Client.on_callback_query(filters.regex(r"^pm"))
async def pmquery(bot, message):
       i, msg, db = message.data.split('#')
       music = await bot.get_messages(db, int(msg))
       await message.answer("The song is sended to your pm", show_alert=True)
       await music.copy(int(message.from_user.id), reply_markup=None)
    
