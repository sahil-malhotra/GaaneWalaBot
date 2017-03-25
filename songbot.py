from __future__ import unicode_literals
import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
from bs4 import BeautifulSoup
import youtube_dl





logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def main():
    if not os.path.exists('temp_folder'):
        os.makedirs('temp_folder')

    updater = Updater(token =  '323089477:AAGb9nhYKPZFtb_Q-l2Wbh7KDG6ASc0KMMQ')
    disp = updater.dispatcher

    # register handlers in dispatcher

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(MessageHandler(Filters.text, getMusic))
    

    updater.start_polling()
    updater.idle()

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Welcome to GaaneWalaApp! Enter the name of the song or press /random to get a trending song")

def getMusic(bot, update):
    title, videoUrl = lookup(update.message.text)
    song_dict = download(title, videoUrl)
    update.message.reply_audio(**song_dict)

def lookup(text):
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
