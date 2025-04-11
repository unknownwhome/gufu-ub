from telethon import events

from .client import client

class Loader:
    modules = {}

    class Module:
        def __init__(self):
            self.name = self.__class__.__name__

    @staticmethod
    def is_module_loaded(command_name):
        for module_info in Loader.modules.values():
            if module_info.get("type") == "module":
                if command_name in module_info.get("commands", []):
                    return True
        return False

    def command(self, module_name=None, new=True, edited=True):
        def decorator(func):
            Loader.modules[func.__name__] = {"func": func, "type": "command", "module_name": module_name}
            func_name_without_cmd = func.__name__.removesuffix('cmd')
            
            async def wrapper(event):
                command = event.text.split()[0][1:]
                if command.endswith('cmd'):
                    return
                
                check_module_name = module_name if module_name else func_name_without_cmd
                
                if not Loader.is_module_loaded(check_module_name):
                    return
                
                if hasattr(func, '__self__') or (func.__code__.co_argcount > 0 and func.__code__.co_varnames[0] == 'self'):
                    await func(self, event)
                else:
                    await func(event)
            
            if func.__name__.endswith('cmd'):
                if new:
                    client.add_event_handler(wrapper, events.NewMessage(pattern=f"^\.{func_name_without_cmd}"))
                if edited:
                    client.add_event_handler(wrapper, events.MessageEdited(pattern=f"^\.{func_name_without_cmd}"))
            return func
        return decorator

loader = Loader()
