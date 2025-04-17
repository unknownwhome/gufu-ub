import os
from ..core import loader, utils

class LMModule(loader.Module):
    @loader.command()
    async def lmcmd(self, message):
        if not message.is_reply:
            await utils.answer(message, "Ответьте на файл")
            return
        
        reply_message = await message.get_reply_message()
        
        loaded_modules_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'loaded_modules')
        if not os.path.exists(loaded_modules_dir):
            os.makedirs(loaded_modules_dir)
        
        await utils.answer(message, "Скачивание файла...")
        
        file_path = await reply_message.download_media(loaded_modules_dir)
        
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.txt':
            py_file_path = file_path.replace('.txt', '.py')
            with open(file_path, 'r') as txt_file, open(py_file_path, 'w') as py_file:
                py_file.write(txt_file.read())
            os.remove(file_path)
            file_path = py_file_path
        elif file_extension != '.py':
            os.remove(file_path)
            await utils.answer(message, "Поддерживаются только файлы с расширением .py или .txt")
            return
        
        with open(file_path, 'r') as file:
            content = file.read()
            class_name = None
            for line in content.split('\n'):
                if line.startswith('class'):
                    class_name = line.split()[1].split('(')[0]
                    break
        
        if class_name in loader.modules:
            os.remove(file_path)
            await utils.answer(message, f"✅ Модуль <code>{class_name}</code> уже загружен")
            return
        
        if utils.load_module(loader, file_path):
            await utils.answer(message, f"✅ Модуль <code>{class_name}</code> успешно загружен и зарегистрирован")
        else:
            os.remove(file_path)
            await utils.answer(message, f"❌ Ошибка при загрузке модуля <code>{class_name}</code>")

    @loader.command()
    async def ulmcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, "❌ Укажите название модуля для удаления\nПример: <code>.ulmcmd ModuleName</code>")
            return
        
        result = utils.unload_module(loader, args)
        await utils.answer(message, result)