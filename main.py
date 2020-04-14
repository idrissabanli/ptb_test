from time import sleep
import telegram
from telegram.error import NetworkError, Unauthorized
import requests
import os


class TBot():
    update_id = None

    def __init__(self):
        token = os.environ.get('bot_token')
        self.bot = telegram.Bot(token)
        try:
            bot_update = self.bot.get_updates()
            self.update_id = bot_update[0].update_id
        except IndexError:
            self.update_id = None
        while True:
            try:
                self.echo()
            except NetworkError:
                sleep(1)
            except Unauthorized:
                # The user has removed or blocked the bot.
                self.update_id += 1
    
    def find_type(self, user):
        return user['type']
    
    def search_file(self, word):
        with open('responses.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                line_data = line.split(':=')
                print(line_data)
                if word == line_data[0]:
                    return line_data[1]
            return "miaaaaaaau!!!"

    def echo(self):
        """Echo the message the user sent."""

        for update in self.bot.get_updates(offset=self.update_id, timeout=10):
            self.update_id = update.update_id + 1
            if update.message:  # your bot can receive updates without messages
                main_type = self.find_type(update.message['chat'])
                message_text = update.message.text
                if message_text:
                    
                    if 'cat' in message_text.lower():
                        print(update.message.chat_id)
                        sticker = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
                        self.bot.send_sticker(chat_id=update.message.chat_id, sticker=sticker)
                    elif 'bot' in message_text.lower():
                        update.message.reply_text(self.search_file(message_text.lower().replace('bot', '').strip(' ')))
                        # sticker = telegram.StickerSet(name="MemePack")
                        
                        # update.message.reply_sticker(sticker)
                        # self.bot.sendSticker(self.bot.getChat)

if __name__ == '__main__':
    TBot()