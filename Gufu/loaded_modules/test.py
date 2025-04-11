from ..core import loader, utils


class Test(loader.Module):
    @loader.command()
    async def testcmd(message):
        await utils.answer(message, "Тест комманда")