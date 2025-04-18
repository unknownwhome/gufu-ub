import os
from ..core import loader, utils

class GofuLM(loader.Module):
    strings = {
        "reply_file": "❌ Ответьте на файл модуля который хотите скачать",
        "downloading": "Скачивание файла...",
        "only_py_txt": "Поддерживаются только файлы с расширением .py или .txt",
        "module_loaded": "Модуль <code>{module_name}</code> уже загружен",
        "module_loaded_success": (
            "Модуль <code>{module_name}</code> успешно загружен и зарегистрирован\n\n"
            "<b>Команды:</b>\n{commands}"
        ),
        "module_load_error": "❌ Ошибка при загрузке модуля <code>{module_name}</code>",
        "no_module_name": "❌ Укажите название модуля для удаления\nПример: <code>.ulm ModuleName</code>",
        "module_unload_result": "{result}",
        "no_commands": "Описание команд не найдено",
        "reply_lm": "❗ Чтобы скачать модуль, ответьте на это сообщение командой <code>.lm</code>",
        "module_not_found": "❌ Модуль <code>{module_name}</code> не найден",
        "module_file_sent": "📤 Модуль <code>{module_name}</code> отправлен",
        "developer_label": "\n\n<b>Разработчик:</b> {developer}"
    }

    @loader.command()
    async def lmcmd(self, message):
        if not message.is_reply:
            await utils.answer(message, self.strings["reply_file"])
            return

        reply_message = await message.get_reply_message()

        loaded_modules_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'loaded_modules')
        if not os.path.exists(loaded_modules_dir):
            os.makedirs(loaded_modules_dir)

        await utils.answer(message, self.strings["downloading"])

        file_path = await reply_message.download_media(loaded_modules_dir)

        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.txt':
            py_file_path = file_path.replace('.txt', '.py')
            with open(file_path, 'r', encoding='utf-8') as txt_file, open(py_file_path, 'w', encoding='utf-8') as py_file:
                py_file.write(txt_file.read())
            os.remove(file_path)
            file_path = py_file_path
        elif file_extension != '.py':
            os.remove(file_path)
            await utils.answer(message, self.strings["only_py_txt"])
            return

        developer = None
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line.lower().startswith("#meta_developer:"):
                    developer = line.split(":", 1)[1].strip()
                    break

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            class_name = None
            for line in content.split('\n'):
                if line.startswith('class'):
                    class_name = line.split()[1].split('(')[0]
                    break

        if class_name in loader.modules:
            os.remove(file_path)
            await utils.answer(message, self.strings["module_loaded"].format(module_name=class_name))
            return

        module_name, commands = utils.load_module(loader, file_path)
        if module_name:
            if commands:
                commands_text = "\n".join(
                    f"<code>.{cmd.split(' | ')[0]}</code> | {cmd.split(' | ')[1]}"
                    for cmd in commands
                )
            else:
                commands_text = self.strings["no_commands"]

            developer_text = ""
            if developer:
                developer_text = self.strings["developer_label"].format(developer=developer)

            text = self.strings["module_loaded_success"].format(
                module_name=module_name,
                commands=commands_text
            ) + developer_text

            await utils.answer(message, text)
        else:
            os.remove(file_path)
            await utils.answer(message, self.strings["module_load_error"].format(module_name=class_name))


    @loader.command()
    async def ulmcmd(self, message):
        args = utils.get_args_raw(message)
        if not args:
            await utils.answer(message, self.strings["no_module_name"])
            return

        result = utils.unload_module(loader, args)
        await utils.answer(message, self.strings["module_unload_result"].format(result=result))

    @loader.command()
    async def mlcmd(self, message):
        args = utils.get_args_raw(message).strip()
        if not args:
            await utils.answer(message, self.strings["no_module_name"])
            return

        module_info = loader.modules.get(args)
        if not module_info:
            module_info = loader.userbot_modules.get(args)

        if not module_info:
            await utils.answer(message, self.strings["module_not_found"].format(module_name=args))
            return

        module_class = module_info.get("module")
        full_module_name = module_class.__module__

        import importlib.util
        spec = importlib.util.find_spec(full_module_name)
        if not spec or not spec.origin or not spec.origin.endswith('.py'):
            await utils.answer(message, self.strings["module_not_found"].format(module_name=args))
            return

        file_path = spec.origin

        commands = module_info.get("commands", [])
        instance = module_info.get("instance")
        if commands:
            commands_text = []
            for cmd_name in commands:
                cmd_func = getattr(instance, cmd_name + "cmd", None)
                doc = cmd_func.__doc__ if cmd_func and cmd_func.__doc__ else self.strings["no_commands"]
                commands_text.append(f"<code>.{cmd_name}</code> | {doc.strip()}")
            commands_text = "\n".join(commands_text)
        else:
            commands_text = self.strings["no_commands"]

        description_text = (
            f"📦 Модуль <code>{args}</code>\n\n"
            f"<b>Команды:</b>\n{commands_text}\n\n"
            f"{self.strings['reply_lm']}"
        )

        await utils.send_file(
            message,
            file_path,
            caption=description_text,
            reply_to=message.id
        )
