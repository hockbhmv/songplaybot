import io
import os 
import requests
from pyrogram import filters
from lyricsgenius import genius
from pyrogram import Client as pbot

#API = "https://apis.xditya.me/lyrics?song="
API = genius.Genius("LTjINTL7fUCR16PdCLVHK339v4vxPtC8Pe70aDW7_vA7BlSbABKcnddm5ZxdomB2",verbose=False)

def search(song):
        r = requests.get(API + song)
        find = r.json()
        return find
       
def lyrics(song):
        fin = search(song)
        text = f'**🎶 Successfully Extracte Lyrics Of {song} 🎶**\n\n\n\n'
        text += f'`{fin["lyrics"]}`'
        text += '\n\n\n💙 Thanks for using me'
        return text


@pbot.on_message(filters.command(["lyric", "lyrics"]) & filters.group)
async def _(client, message):
   if ' ' in message.text:
      r, query = message.text.split(None, 1)
      k = await message.reply("Searching For Lyrics.....")
      rpl = lyrics(query)
      try:
         await k.delete()
         await client.send_message(chat_id, text = rpl, reply_to_message_id = message.message_id)
      except Exception as e:
         await message.reply_text(f"I Can't Find A Song With `{query}`", quote = True)
