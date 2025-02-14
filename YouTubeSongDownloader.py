from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import youtube_dl
from youtube_search import YoutubeSearch
import requests
import os
import time
from config import Config

bot = Client(
    "YouTubeSongDownloader",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH
)

# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@bot.on_message(filters.command(["start"]))
def start(client, message):
    uday = "hi"
    message.reply_text(
        text=uday,
        quote=False,
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("Updates 👬", url="https://t.me/Animemusicarchive6"),
                InlineKeyboardButton("Support 🤗", url="https://t.me/Yeageristbots")
            ]
        ])
    )

@bot.on_message(filters.command(["s"]))
def a(client, message):
    query = " ".join(message.command[1:])
    print(query)
    m = message.reply("🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠...")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count > 0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        
        if not results:
            m.edit("𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐓𝐫𝐲 𝐂𝐡𝐚𝐧𝐠𝐢𝐧𝐠 𝐓𝐡𝐞 𝐒𝐩𝐞𝐥𝐥𝐢𝐧𝐠 𝐀 𝐋𝐢𝐭𝐭𝐥𝐞 😕")
            return
        
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        duration = results[0]["duration"]
        views = results[0]["views"]
        thumb_name = f"thumb{message.message_id}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
    
    except Exception as e:
        m.edit("✖️ 𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐒𝐨𝐫𝐫𝐲.\n\n𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐝 𝐎𝐫 𝐌𝐚𝐲𝐛𝐞 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲.")
        print(str(e))
        return
    
    m.edit("🔎 𝐅𝐢𝐧𝐝𝐢𝐧𝐠 𝐀 𝐒𝐨𝐧𝐠 🎶 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 ⏳️ 𝐅𝐨𝐫 𝐅𝐞𝐰 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 [🚀](https://telegra.ph/file/60b0489093120e762861f.mp4)")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        
        rep = (f"🎧 𝐓𝐢𝐭𝐥𝐞 : [{title[:35]}]({link})\n"
               f"⏳ 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧 : `{duration}`\n"
               f"🎬 𝐒𝐨𝐮𝐫𝐜𝐞 : [Youtube](https://youtu.be/3pN0W4KzzNY)\n"
               f"👁‍🗨 𝐕𝐢𝐞𝐰𝐬 : `{views}`\n\n"
               f"💌 A Bot 𝐁𝐲 : @Animemusicarchive6")
        
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        
        message.reply_audio(audio_file, caption=rep, parse_mode="md", quote=False, title=title, duration=dur, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("❌ 𝐄𝐫𝐫𝐨𝐫")
        print(e)
    
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
