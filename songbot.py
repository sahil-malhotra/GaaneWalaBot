import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def main():
    if not os.path.exists('temp_folder'):
        os.makedirs('temp_folder')

    updater = Updater(token =  '323089477:AAGb9nhYKPZFtb_Q-l2Wbh7KDG6ASc0KMMQ')
    disp = updater.dispatcher

    # register handlers in dispatcher

    disp.add_handler(CommandHandler("start", initiate))




if __name__ == '__main__':
    main()
