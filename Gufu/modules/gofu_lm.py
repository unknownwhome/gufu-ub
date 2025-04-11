import os
from ..core import loader
from ..core.utils import load_module

class LMModule(loader.Module):
    @loader.command()
    async def lmcmd(self, message):
        if not message.is_reply:
            await message.edit("Ответьте на файл")
            return
        
        reply_message = await message.get_reply_message()
        
        if not reply_message.media:
            await message.edit("Файл не найден")
            return
        
        loaded_modules_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'loaded_modules')
        if not os.path.exists(loaded_modules_dir):
            os.makedirs(loaded_modules_dir)
        
        await message.edit("Скачивание файла...")
        
        file_path = await reply_message.download_media(loaded_modules_dir)
        
        await message.edit(f"Файл успешно загружен в папку loaded_modules: {os.path.basename(file_path)}")
        
        if load_module(loader, file_path):
            await message.edit(f"Модуль успешно загружен и зарегистрирован.")
        else:
            os.remove(file_path)
            await message.edit(f"Ошибка при загрузке модуля. Файл удален.")
