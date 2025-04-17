from ..core import loader, utils

class GufuHelp(loader.Module):
    @loader.command()
    async def helpcmd(self, message):
        all_modules = {**loader.userbot_modules, **loader.modules}
        
        module_names = list(all_modules.keys())
        shown_count = len(module_names)
        hidden_count = 0
        
        module_list = []
        for name in module_names:
            module_type = "🔹" if name in loader.userbot_modules else "▪️"
            commands = all_modules[name].get("commands", [])
            module_list.append(
                f"{module_type}<code>{name}:</code> <b>({ ' | '.join(cmd for cmd in commands) })</b>"
            )
        
        module_list_text = "\n".join(module_list)
        await utils.answer(
            message, 
            f"<b>{shown_count} модулей доступно, {hidden_count} скрыто:</b>\n\n{module_list_text}"
        )