import asyncio

from .core import UserBot, client, loader
from .core.utils import register_and_load_modules
from .core.bot import create_bot


async def main():
    userbot = UserBot(client)
    await userbot.start()
    register_and_load_modules(loader)
    #await create_bot()
    await userbot.run()

if __name__ == "__main__":
    asyncio.run(main())
