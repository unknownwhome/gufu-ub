from ..core import loader, utils
import time

class GofuPing(loader.Module):
    strings = {
        "ping_check": "Проверка пинга...",
        "ping_result": "<b>Пинг: <code>{ping_time}</code> мс</b>"
    }

    @loader.command()
    async def pingcmd(self, message):
        """описание команды текст"""
        start_time = time.time()
        await message.edit(self.strings["ping_check"])
        end_time = time.time()
        ping_time = round((end_time - start_time) * 1000)
        await utils.answer(message, self.strings["ping_result"].format(ping_time=ping_time))
