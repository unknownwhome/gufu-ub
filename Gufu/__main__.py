import asyncio

from core.userbot import UserBot, client
from core.utils import load_modules


async def main():
    userbot = UserBot(client)
    await userbot.start()
    load_modules()
    await userbot.run()

if __name__ == "__main__":
    asyncio.run(main())
