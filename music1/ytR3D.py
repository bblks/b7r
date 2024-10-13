import yt_dlp, os, re, time, random , redis, json
from yt_dlp import YoutubeDL
from kvsqlite.sync import Client as Database
from youtube_search import YoutubeSearch as Y88F8
from pyrogram import *
from pyrogram.types import *

r = redis.Redis('localhost', decode_responses=True)
ytdb = Database("YouTube-SQL.sqlite")
ZAID = 7085943284   #ايدي المطور
TOKEN = "7117654702:AAGbwqlPBovaLzaW05cS9MIzISSolEesfco"
YTchannel = "ngd_2" #  يوزر قناة التخزين  بدون @
Dev_Zaid = TOKEN.split(":")[0]
client = Client(
  "ytZAID", 17954744, "7ad6189ad04c5d3a698b1b541e62c42b", bot_token=TOKEN,
  in_memory=True
)

client.start()
def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":")))
    )
 
@client.on_message(filters.regex("^تعطيل اليوتيوب$") & filters.group)
async def dis_yt(c,m):
     e = "• من {}\n• تم تعطيل اليوتيوب مسبقاً"
     d = "• من {}\n• ابشر عطلت اليوتيوب"
     if m.from_user.id == ZAID:
        if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}'):
           return await m.reply(e.format(m.from_user.mention))
        else:
           r.set(f'{m.chat.id}:disableYT:{Dev_Zaid}',1)
           return await m.reply(d.format(m.from_user.mention))
     member = await m.chat.get_member(m.from_user.id)
     if not member.status == "member":
        if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}'):
           return await m.reply(e.format(m.from_user.mention))
        else:
           r.set(f'{m.chat.id}:disableYT:{Dev_Zaid}',1)
           return await m.reply(d.format(m.from_user.mention))
     else:
        return await m.reply("هذ الأمر يخص ( المشرف وفوق ) بس")
        
@client.on_message(filters.regex("^تفعيل اليوتيوب$") & filters.group)
async def ena_yt(c,m):
     e = "• من {}\n• تم تفعيل اليوتيوب مسبقاً"
     d = "• من {}\n• ابشر فعلت اليوتيوب"
     if m.from_user.id == ZAID:
        if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}'):
           return await m.reply(e.format(m.from_user.mention))
        else:
           r.set(f'{m.chat.id}:disableYT:{Dev_Zaid}',1)
           return await m.reply(d.format(m.from_user.mention))
     member = await m.chat.get_member(m.from_user.id)
     if not member.status == "member":
        if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}'):
           return await m.reply(e.format(m.from_user.mention))
        else:
           r.set(f'{m.chat.id}:disableYT:{Dev_Zaid}',1)
           return await m.reply(d.format(m.from_user.mention))
     else:
        return await m.reply("هذ الأمر يخص ( المشرف وفوق ) بس")
     
@client.on_message(filters.text & filters.group, group=1)
async def ytdownloaderHandler(c,m):
    k = "⇜"
    channel = "RaaD"
    await yt_func(c,m,k,channel)
    
async def yt_func(c,m,k,channel):
   text = m.text   
   rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url='https://t.me/NGD_1')
     ]]
   )
   
   
   if text == "نسخة اليوتيوب" and m.from_user.id == ZAID:
     if not ytdb.keys(): return await m.reply("تخزين اليوتيوب فاضي")
     else:
        videos = []
        audios = []
        for key in ytdb.keys():
           get = {"key":key[0],"value":ytdb.get(key[0])}
           if get["value"]["type"] == "audio":
             audios.append(get)
           if get["value"]["type"] == "video":
             videos.append(get)
        id = random.randint(1,10000)
        if audios:
          with open(f"audios-{id}.json","w+") as f:
            f.write(json.dumps(audios, indent=4, ensure_ascii=False))
          await m.reply_document(f"audios-{id}.json")
          os.remove(f"audios-{id}.json")
        if videos:
          with open(f"videos-{id}.json","w+") as f:
            f.write(json.dumps(videos, indent=4, ensure_ascii=False))
          await m.reply_document(f"videos-{id}.json")
          os.remove(f"videos-{id}.json")
        return True

   if re.match("^يوت ", text):
     if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}'):  return False
     query = text.split(None,1)[1]
     keyboard= []
     results=Y88F8(query,max_results=4).to_dict()
     for res in results:
       title = res['title']
       id = res['id']
       keyboard.append([InlineKeyboardButton (title, callback_data=f'{m.from_user.id}AUDIO{id}')])     
     a = await m.reply(f'{k} البحث ~ {query}',reply_markup=InlineKeyboardMarkup (keyboard), disable_web_page_preview=True)
     r.set(f'{a.id}:one_minute:{m.from_user.id}', 1, ex=60)
     return True
     
   if re.match("^بحث ", text) or re.match("^yt ", text):
     if r.get(f'{m.chat.id}:disableYT:{Dev_Zaid}'):  return
     query = text.split(None,1)[1]
     results=Y88F8(query,max_results=1).to_dict()
     res = results[0]
     title = res['title']
     duration= int(time_to_seconds(res['duration']))
     duration_string = time.strftime('%M:%S', time.gmtime(duration))
     if ytdb.get(f'ytvideo{res["id"]}'):
        aud = ytdb.get(f'ytvideo{res["id"]}')
        duration_string = time.strftime('%M:%S', time.gmtime(aud["duration"]))
        return await m.reply_audio(aud["audio"],caption=f' @E_K_Q ~ {duration_string} ⏳',reply_markup=rep)
     url = f'https://youtu.be/{res["id"]}'
     if duration > 99999999999999:
         return await m.reply("صوت فوق 25 دقيقة ما اقدر انزله",reply_markup=rep)
     else:
         duration_string = time.strftime('%M:%S', time.gmtime(duration))
         ydl_ops = {"format": "bestaudio[ext=m4a]"}
         with yt_dlp.YoutubeDL(ydl_ops) as ydl:
           info = ydl.extract_info(url, download=False)
           audio_file = ydl.prepare_filename(info)
           ydl.process_info(info)
         a = await m.reply_audio(
         audio_file,
         title=title,
         duration=duration,
         caption=f' @NGD_1 ~ {duration_string} ⏳',
         performer=info["channel"],reply_markup=rep)
         b = await a.copy(YTchannel)
         ytdb.set(f'ytvideo{res["id"]}',{"type":"audio","audio":b.link,"duration":a.audio.duration,"id":res["id"]})
         os.remove(audio_file)
         return True

@client.on_callback_query(filters.regex("GET"))
async def get_info(c,query):
    await getInfo(c,query)
async def getInfo(c, query):
    user_id = query.data.split("GET")[0]
    vid_id = query.data.split("GET")[1]
    if not query.from_user.id == int(user_id):
      return False
    if not r.get(f'{query.message.id}:one_minute:{user_id}'):
      k = "⇜"
      await query.answer(f'{k} مر على البحث اكثر من دقيقة ابحث مرة ثانية',show_alert=True)
      return await query.message.delete()
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return False
    url = f'https://youtu.be/{vid_id}'
    reply_markup = InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton ("♫ ملف صوتي", callback_data=f'{user_id}AUDIO{vid_id}'),
          InlineKeyboardButton ("❖ فيديو", callback_data=f'{user_id}VIDEO{vid_id}'),
        ],
        [
          InlineKeyboardButton ('🧚‍♀️', url='https://t.me/NGD_1')
        ]
      ]
    )
    return await query.message.edit(
       f'~ {url}',
       reply_markup=reply_markup, disable_web_page_preview=True
    )
    
@client.on_callback_query(filters.regex("AUDIO"))
async def get_audii(c, query):
    await audio_down(c,query)
async def audio_down(c, query):
    user_id = query.data.split("AUDIO")[0]
    vid_id = query.data.split("AUDIO")[1]
    if not query.from_user.id == int(user_id):
      return False
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return False
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url='https://t.me/NGD_1')
     ]]
    )
    if ytdb.get(f'ytvideo{vid_id}'):
       aud = ytdb.get(f'ytvideo{vid_id}')
       await query.edit_message_text(" :)", reply_markup=rep)
       duration= aud["duration"]
       sec = time.strftime('%M:%S', time.gmtime(duration))
       return await query.message.reply_audio(aud["audio"],caption=f' ~ ⏳ {sec}')       
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_text("جاري التحميل ..", reply_markup=rep)
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    with yt_dlp.YoutubeDL(ydl_ops) as ydl:
        info = ydl.extract_info(url, download=False)
        if int(info['duration']) > 1505:
          return await query.edit_message_text("صوت اكثر من 25 دقيقة مقدر انزله",reply_markup=rep)
        audio_file = ydl.prepare_filename(info)
        ydl.process_info(info)
    await query.edit_message_text("✈️✈️✈️✈️✈️", reply_markup=rep)
    duration= int(info['duration'])
    sec = time.strftime('%M:%S', time.gmtime(duration))
    a = await query.message.reply_audio(
      audio_file,
      title=info['title'],
      duration=int(info['duration']),
      performer=info['channel'],
      caption=f' @NGD_1 ~ ⏳ {sec}',
    )
    await query.edit_message_text(f":)", reply_markup=rep)
    b = await a.copy(YTchannel)
    ytdb.set(f'ytvideo{vid_id}',{"type":"audio","audio":b.link,"duration":a.audio.duration,"id":vid_id})
    os.remove(audio_file)
    
@client.on_callback_query(filters.regex("VIDEO"))
async def get_video(c, query):
   await video_down(c,query)
async def video_down(c, query):
    user_id = query.data.split("VIDEO")[0]
    vid_id = query.data.split("VIDEO")[1]
    if not query.from_user.id == int(user_id):
      return False
    if r.get(f'{query.message.chat.id}:disableYT:{Dev_Zaid}'):  return False
    rep = InlineKeyboardMarkup (
     [[
       InlineKeyboardButton ('🧚‍♀️', url='https://t.me/NGD_1')
     ]]
    )
    if ytdb.get(f'ytvideoV{vid_id}'):
       vid = ytdb.get(f'ytvideoV{vid_id}')
       await query.edit_message_text(f":)", reply_markup=rep)
       duration=vid["duration"]
       sec = time.strftime('%M:%S', time.gmtime(duration))
       return await query.message.reply_video(vid["video"],caption=f' @E_K_Q ~ ⏳ {sec}')
    url = f'https://youtu.be/{vid_id}'
    await query.edit_message_text("جاري التحميل ..", reply_markup=rep)
    with yt_dlp.YoutubeDL({}) as ydl:
        info = ydl.extract_info(url, download=False)
        if int(info['duration']) > 6855888888:
          return await query.edit_message_text("فيديو اكثر من 25 دقيقة مقدر انزله",reply_markup=rep)
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    with YoutubeDL(ydl_opts) as ytdl:
        ytdl_data = ytdl.extract_info(url, download=True)
        file_name = ytdl.prepare_filename(ytdl_data)
    await query.edit_message_text("✈️✈️✈️✈️✈️", reply_markup=rep)
    duration= int(info['duration'])
    sec = time.strftime('%M:%S', time.gmtime(duration))
    a = await query.message.reply_video(
      file_name,
      duration=int(info['duration']),
      caption=f' @NGD_1 ~ ⏳ {sec}',
    )
    await query.edit_message_text(f":)", reply_markup=rep)
    b = await a.copy(YTchannel)
    ytdb.set(f'ytvideoV{vid_id}',{"type":"video","video":b.link,"duration":a.video.duration,"id":vid_id})
    os.remove(file_name)
 
if __name__ == "__main__":
     idle()
