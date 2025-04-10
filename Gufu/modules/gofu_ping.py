from core.loader import loader
from core import utils
import time

@loader.command()
async def pingcmd(message):
    start_time = time.time()
    await message.edit("Проверка пинга...")
    end_time = time.time()
    ping_time = round((end_time - start_time) * 1000)
    await utils.answer(message, f"<b>Пинг: <code>{ping_time}</code> мс</b>")

class Test(loader.Module):
    @loader.command()
    async def testcmd(message):
        await utils.answer(message, "Тест комманда")
