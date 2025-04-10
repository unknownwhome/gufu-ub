from telethon import events

from core.userbot import client

class Loader:
    modules = {}

    class Module:
        def __init__(self):
            self.name = self.__class__.__name__

    def command(self, new=True, edited=True):
        def decorator(func):
            Loader.modules[func.__name__] = {"func": func, "type": "command"}
            func_name_without_cmd = func.__name__.removesuffix('cmd')
            async def wrapper(event):
                command = event.text.split()[0][1:]
                if command.endswith('cmd'):
                    return
                await func(event)
            if func.__name__.endswith('cmd'):
                if new:
                    client.add_event_handler(wrapper, events.NewMessage(pattern=f"^\.{func_name_without_cmd}"))
                if edited:
                    client.add_event_handler(wrapper, events.MessageEdited(pattern=f"^\.{func_name_without_cmd}"))
            return func
        return decorator



loader = Loader()
