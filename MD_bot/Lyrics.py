import io
import os
from pyrogram import filters
from pyrogram import Client as pbot

API = "https://apis.xditya.me/lyrics?song="

def search(song):
        r = requests.get(API + song)
        find = r.json()
        return find
       
def lyrics(song):
        fin = search(song)
        text = f'**🎶 Successfully Extracte Lyrics Of {song} 🎶**\n\n\n\n'
        text += f'`{fin["lyrics"]}`'
        text += '\n\n\n💙 Thanks to you me'
        return text


@pbot.on_message(filters.command(["lyric", "lyrics"]) & filters.group)
async def _(client, message):
    k = await message.reply("Searching For Lyrics.....")
    query = message.text
    rpl = lyrics(query)
        await k.delete()
        try:
            await k.delete()
            await client.send_message(chat_id, text = rpl, reply_to_message_id = message.message_id)
        except Exception as e:
             await message.reply_text(f"I Can't Find A Song With `{query}`", quote = True)
