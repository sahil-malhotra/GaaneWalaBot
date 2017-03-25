from __future__ import unicode_literals
import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import youtube_dl
import lyricwikia

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def main():
    if not os.path.exists('temp_folder'):
        os.makedirs('temp_folder')

    updater = Updater(token='323089477:AAGb9nhYKPZFtb_Q-l2Wbh7KDG6ASc0KMMQ')
    disp = updater.dispatcher

    # register handlers in dispatcher

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(MessageHandler(Filters.text, getMusic))
    disp.add_handler(CommandHandler("random", getRan))

    updater.start_polling()
    updater.idle()


def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Welcome to GaaneWalaApp! Enter the name of the song or press /random to get a trending song "
                         "or to find the latest song by any artist just type 'artist [name of the artist]'")

def getRan(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Downloading popular song of this week")
    newtitle = looktrend()
    title, videoUrl = lookup(newtitle)
    song_dict = download(title, videoUrl)
    update.message.reply_audio(**song_dict)



def getMusic(bot, update):
    text = update.message.text.split(' ')
    newtext = ""
    if text[0] == 'artist':
        text.pop(0)
        newtext = " ".join(text)
        title, videoUrl = lookup(newtext + " latest song")
        song_dict = download(title, videoUrl)
        update.message.reply_audio(**song_dict)

    elif text[0] == 'lyrics':
        text.pop(0)
        newtext = " ".join(text)

        newarr = newtext.split(',')
        print(newarr[1], newarr[0])
        lyrics = lyricwikia.get_lyrics(newarr[1], newarr[0])
        update.message.reply_text(lyrics)

    else:
        newtext = update.message.text
        title, videoUrl = lookup(newtext)
        song_dict = download(title, videoUrl)
        update.message.reply_audio(**song_dict)


def looktrend():
    url = 'http://www.billboard.com/charts/youtube'
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    tag = soup.find('h2', {"class":"chart-row__song"})
    title = tag.text
    return title


def lookup(text):
    url = 'https://www.youtube.com'
    req = requests.get(url + '/results', params={'search_query': text})
    soup = BeautifulSoup(req.content, 'html.parser')
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    title, videoUrl = tag.text, url + tag['href']
    return title, videoUrl

def lookart(text):
    url = 'https://www.youtube.com'
    req = requests.get(url + '/results', params={'search_query': text})
    soup = BeautifulSoup(req.content, 'html.parser')
    tag = soup.find('a', {'rel': 'spf-prefetch'})
    title, videoUrl = tag.text, url + tag['href']
    return title, videoUrl



def download(title, videoUrl):
    ydl_opts = {
        'outtmpl': 'temp_folder/{}.%(ext)s'.format(title),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoUrl])

    song_dict = {
        'audio': open('temp_folder/{}.mp3'.format(title), 'rb'),
        'title': title,
    }

    return song_dict


if __name__ == '__main__':
    main()
