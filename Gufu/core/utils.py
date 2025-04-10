import os
import importlib.util

from core.loader import loader

def register_module(module):
    if isinstance(module, type) and issubclass(module, loader.Module):
        loader.modules[module.__name__] = {"module": module, "type": "module", "commands": []}
        
        for item_name in dir(module):
            item = getattr(module, item_name)
            if callable(item) and hasattr(item, '__name__') and item.__name__.endswith('cmd'):
                loader.modules[module.__name__]["commands"].append(item.__name__.removesuffix('cmd'))


def load_modules():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    modules_dir = os.path.join(project_dir, 'modules')
    loaded_modules = []

    for filename in os.listdir(modules_dir):
        if filename.endswith(".py"):
            module_name = filename[:-3]
            try:
                spec = importlib.util.spec_from_file_location(module_name, os.path.join(modules_dir, filename))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, loader.Module):
                        register_module(item)
                loaded_modules.append(module_name)
            except Exception as e:
                print(f"Ошибка при загрузке модуля {module_name}: {e}")

    print("Загруженные модули:")
    for module in loaded_modules:
        print(module)


async def answer(message, text, parse_mode="HTML"):
    await message.edit(text, parse_mode=parse_mode)