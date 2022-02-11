import io
import os 
import requests
from pyrogram import filters
from lyricsgenius import genius
from pyrogram import Client as pbot

api = genius.Genius("OXaVabSRKQLqwpiYOn-E4Y7k3wj-TNdL5RfDPXlnXhCErbcqVvdCF-WnMR5TBctI",verbose=False)


def lyrics(song):
        lyric = api.search_song(song)
        lyrics = lyric.lyrics
        text = f'**🎶 Successfully Extracte Lyrics Of {song} 🎶**\n\n\n\n'
        text += f'{lyrics}'
        text += '\n\n\n💙 Thanks for using me'
        return text


@pbot.on_message(filters.command(["lyric", "lyrics"]))
async def lyric(client, message):
   if ' ' in message.text:
      i, query = message.text.split(None, 1)
      xx = await message.reply("Searching For Lyrics.....")
      lyric = lyrics(query)
      try:
         await xx.edit(lyric) 
      except Exception as e:
         await xx.edit(f"I Can't Find A Song With `{query}`")
         print(e)
      return       
