from core.loader import loader
from core import utils

class GufuHelp(loader.Module):
    @loader.command()
    async def helpcmd(message):
        module_names = [name for name, value in loader.modules.items() if value.get("type") == "module"]
        shown_count = len(module_names)
        hidden_count = 0
        module_list = "\n".join(
            f"▪️<code>{name}:</code> <b>({ ' | '.join(cmd for cmd in loader.modules[name]['commands']) })</b>" 
            for name in module_names
        )
        await utils.answer(message, f"<b>{shown_count} модулей доступно, {hidden_count} скрыто:</b>\n\n{module_list}")
