import asyncio

from ..core import client

async def answer(username, message, delay=2):
    await asyncio.sleep(delay)
    await client.send_message(username, message)

async def create_bot():
    await answer('@BotFather', '/start')
    await answer('@BotFather', '/newbot')
    await answer('@BotFather', 'Gufu UserBot')
