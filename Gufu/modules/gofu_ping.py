from ..core import loader, utils
import time


class GofuPing(loader.Module):
    @loader.command()
    async def pingcmd(self, message):
        start_time = time.time()
        await message.edit("Проверка пинга...")
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000)
        await utils.answer(message, f"<b>Пинг: <code>{ping_time}</code> мс</b>")
