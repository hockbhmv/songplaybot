from pyrogram import Client, filters
from os import environ
import asyncio
import os
import time
import youtube_dl
import logging
from youtube_search import YoutubeSearch
from pytube import YouTube
import requests
from youtubesearchpython import VideosSearch 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
import re
id_pattern = re.compile(r'^.\d+$')
CUSTOM_CAPTION = environ.get("CUSTOM_CAPTION", "")

@Client.on_message(filters.command("start"))
async def start(bot, message):
  user = message.from_user.first_name
  await message.reply_text(text = f"<code>ഹായ് {user},\nനിലവിൽ എന്റെ അഡ്മിൻ എന്നെ ഉണ്ടാക്കുന്നു\n\n ദയവായി പിന്നീട് വരൂ</code>")



  

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
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])        
      
      
      
@Client.on_message(filters.command(["music", "song"]))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
 
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter a song name.\n\n **example:**\n<code>/song Clay Love Nwantiti</code>")
        return ""
    status = await message.reply("<code>processing...</code>")
    await asyncio.sleep(1)
    await status.edit("<code>🔎searching the song....\n  Please wait ⏳ for few seconds</code>")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("✖️ 𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐒𝐨𝐫𝐫𝐲.\n\n𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐤 𝐎𝐫 𝐌𝐚𝐲𝐛𝐞 𝐒𝐩𝐞𝐥𝐥.\n\nEg.`/song Faded`")
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
    btn = [
            [
                InlineKeyboardButton(
                    text="send me in pm",
                    callback_data=f"pm#{str(user_id)}.mp3",
                )
            ]
        ]
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await client.send_chat_action(message.chat.id, "upload_audio")
    await client.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        caption = cap,
        thumb=thumb_name,
        performer=f"[MD MUSIC BOT]",
        reply_to_message_id= message.message_id,
        reply_markup=InlineKeyboardMarkup(btn))
    
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
    
@Client.on_callback_query(filters.regex('^pm'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    i, movie = query.data.split('#')
    
    await bot.send_audio(
        chat_id=query.from_user.id,
        audio=movie, 
        caption = "testing",
        
        performer=f"[MD MUSIC BOT]",
        
    )
