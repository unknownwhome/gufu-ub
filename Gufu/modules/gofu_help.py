from ..core import loader, utils

class GofuHelp(loader.Module):
    strings = {
        "help_header": "<b>{shown_count} модулей доступно, {hidden_count} скрыто:</b>\n\n",
        "module_item": "{module_type}<code>{module_name}:</code> <b>({commands})</b>",
        "module_not_found": "❌ Модуль <code>{module_name}</code> не найден",
        "module_commands_header": "<b>Команды модуля <code>{module_name}</code></b>\n\n",
        "no_commands": "Команды не найдены",
        "no_command_description": "Описание не найдено"
    }

    @loader.command()
    async def helpcmd(self, message):
        args = utils.get_args_raw(message).strip()

        all_modules = {**loader.userbot_modules, **loader.modules}

        if args:
            module_info = all_modules.get(args)
            if not module_info:
                await utils.answer(message, self.strings["module_not_found"].format(module_name=args))
                return

            commands = module_info.get("commands", [])
            if not commands:
                commands_text = self.strings["no_commands"]
            else:
                instance = module_info.get("instance")
                commands_list = []
                for cmd_name in commands:
                    cmd_func = getattr(instance, cmd_name + "cmd", None)
                    doc = cmd_func.__doc__ if cmd_func and cmd_func.__doc__ else self.strings["no_command_description"]
                    commands_list.append(f"<code>.{cmd_name}</code> | {doc.strip()}")

                commands_text = "\n".join(commands_list)

            text = self.strings["module_commands_header"].format(module_name=args) + commands_text
            await utils.answer(message, text)
        else:
            module_names = list(all_modules.keys())
            shown_count = len(module_names)
            hidden_count = 0

            module_list = []
            for name in module_names:
                module_type = "🔹" if name in loader.userbot_modules else "▪️"
                commands = all_modules[name].get("commands", [])
                module_list.append(
                    self.strings["module_item"].format(
                        module_type=module_type,
                        module_name=name,
                        commands=' | '.join(commands) if commands else "нет команд"
                    )
                )

            module_list_text = "\n".join(module_list)

            header_text = self.strings["help_header"].format(
                shown_count=shown_count,
                hidden_count=hidden_count
            )

            response_text = header_text + module_list_text

            await utils.answer(message, response_text)
