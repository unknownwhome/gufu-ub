from telethon import TelegramClient

from config import load_config, save_config

def get_config():
    config = load_config()
    if config:
        return config['api_id'], config['api_hash'], 'gofu_session'
    else:
        api_id = input("Please enter your api_id: ")
        api_hash = input("Please enter your api_hash: ")
        save_config(api_id, api_hash)
        return api_id, api_hash, 'gofu_session'

api_id, api_hash, session_name = get_config()
client = TelegramClient(session_name, api_id, api_hash)

class UserBot:
    def __init__(self, client):
        self.client = client

    async def start(self):
        await self.client.start()

    async def run(self):
        await self.start()
        await self.client.run_until_disconnected()

async def main_userbot():
    userbot = UserBot(client)
    await userbot.run()
