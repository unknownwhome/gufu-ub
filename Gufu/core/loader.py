import inspect

from telethon import events

from .client import client

class Loader:
    userbot_modules = {}
    modules = {}
    commands = {}

    class Module:
        def __init__(self):
            self.name = self.__class__.__name__
            self.strings = getattr(self.__class__, "strings", {})

    @staticmethod
    def is_module_loaded(command_name):
        for module_info in list(Loader.modules.values()) + list(Loader.userbot_modules.values()):
            if command_name in module_info.get("commands", []):
                return True
        return False

    def command(self, new=True, edited=True):
        def decorator(func):
            doc = inspect.getdoc(func)
            Loader.commands[func.__name__] = {
                "func": func,
                "description": doc if doc else None
            }
            func_name_without_cmd = func.__name__.removesuffix('cmd')

            async def wrapper(event):
                command = event.text.split()[0][1:]
                if command.endswith('cmd'):
                    return

                if not Loader.is_module_loaded(func_name_without_cmd):
                    return

                for mod_info in list(self.modules.values()) + list(self.userbot_modules.values()):
                    if func_name_without_cmd in mod_info.get("commands", []):
                        await func(mod_info.get("instance"), event)
                        break

            if func.__name__.endswith('cmd'):
                if new:
                    client.add_event_handler(wrapper, events.NewMessage(pattern=f"^\.{func_name_without_cmd}"))
                if edited:
                    client.add_event_handler(wrapper, events.MessageEdited(pattern=f"^\.{func_name_without_cmd}"))
            return func
        return decorator


loader = Loader()
